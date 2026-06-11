use anyhow::{bail, Result};
use std::path::{Path, PathBuf};

pub fn validate_repo_path(path: &Path) -> Result<PathBuf> {
    if !path.is_absolute() {
        bail!("Repository path must be absolute: {}", path.display());
    }
    let canonical = path
        .canonicalize()
        .map_err(|e| anyhow::anyhow!("Cannot canonicalise path {}: {}", path.display(), e))?;
    if !canonical.is_dir() {
        bail!("Path is not a directory: {}", canonical.display());
    }
    Ok(canonical)
}

pub fn validate_description(desc: &str) -> Result<()> {
    if desc.is_empty() {
        bail!("Description cannot be empty");
    }
    if desc.len() > 256 {
        bail!("Description is too long (max 256 chars)");
    }
    let bad_chars = ['/', '\\', '\0', '\n', '\r', '`', '$', '|', ';', '&', '>', '<'];
    for c in bad_chars {
        if desc.contains(c) {
            bail!("Description contains invalid character: '{c}'");
        }
    }
    Ok(())
}

pub fn validate_open_file_path(path: &str) -> bool {
    let p = Path::new(path);
    p.is_absolute() && !path.contains("..") && !path.contains('\0')
}

pub fn sanitise_open_files(paths: &[String]) -> Vec<String> {
    paths
        .iter()
        .filter(|p| validate_open_file_path(p))
        .cloned()
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_description_rejects_shell_chars() {
        assert!(validate_description("fix $(rm -rf /)").is_err());
        assert!(validate_description("ok description").is_ok());
    }

    #[test]
    fn test_open_file_rejects_traversal() {
        assert!(!validate_open_file_path("/home/user/../etc/passwd"));
        assert!(validate_open_file_path("/home/user/project/main.rs"));
    }
}
