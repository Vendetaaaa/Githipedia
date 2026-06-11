use anyhow::Result;
use serde::Deserialize;
use std::path::{Path, PathBuf};
use tracing::debug;

#[derive(Debug)]
pub struct EditorState {
    pub editor_name: String,
    pub open_files: Vec<String>,
}

pub fn detect_editor_state(repo_root: &Path) -> Result<Option<EditorState>> {
    if let Some(state) = detect_vscode(repo_root)? {
        return Ok(Some(state));
    }
    Ok(None)
}

fn detect_vscode(repo_root: &Path) -> Result<Option<EditorState>> {
    let mut open_files: Vec<String> = Vec::new();

    let vscode_dir = repo_root.join(".vscode");
    if vscode_dir.is_dir() {
        debug!(".vscode dir found at {}", vscode_dir.display());
    }

    let storage_files = find_workspace_storage_files(repo_root)?;
    for sf in &storage_files {
        if let Ok(files) = parse_workspace_storage(sf) {
            open_files.extend(files);
        }
    }

    if let Some(backup_dir) = vscode_backup_dir() {
        if let Ok(files) = scan_backup_dir(&backup_dir, repo_root) {
            open_files.extend(files);
        }
    }

    open_files.sort();
    open_files.dedup();
    let open_files: Vec<String> = open_files
        .into_iter()
        .filter(|p| {
            let path = Path::new(p);
            path.is_absolute() && path.exists()
        })
        .collect();

    if open_files.is_empty() {
        return Ok(None);
    }

    Ok(Some(EditorState {
        editor_name: "vscode".to_string(),
        open_files,
    }))
}

fn find_workspace_storage_files(repo_root: &Path) -> Result<Vec<PathBuf>> {
    let storage_base = vscode_workspace_storage_dir();
    let mut found = Vec::new();

    let Some(base) = storage_base else {
        return Ok(found);
    };

    if !base.is_dir() {
        return Ok(found);
    }

    if let Ok(entries) = std::fs::read_dir(&base) {
        for entry in entries.flatten() {
            let ws_json = entry.path().join("workspace.json");
            if !ws_json.exists() {
                continue;
            }
            if let Ok(content) = std::fs::read_to_string(&ws_json) {
                let repo_str = repo_root.to_string_lossy();
                if content.contains(repo_str.as_ref()) {
                    found.push(entry.path().join("backup"));
                }
            }
        }
    }

    Ok(found)
}

#[derive(Deserialize)]
struct VsCodeBackupEntry {
    #[serde(rename = "filePath")]
    file_path: Option<String>,
}

fn parse_workspace_storage(backup_dir: &Path) -> Result<Vec<String>> {
    let mut files = Vec::new();
    if !backup_dir.is_dir() {
        return Ok(files);
    }
    for entry in walkdir::WalkDir::new(backup_dir).max_depth(2) {
        let entry = entry?;
        if entry.file_type().is_file() {
            let path_str = entry.path().to_string_lossy();
            if let Ok(content) = std::fs::read_to_string(entry.path()) {
                if let Some(first_line) = content.lines().next() {
                    let p = Path::new(first_line);
                    if p.is_absolute() && p.exists() {
                        files.push(first_line.to_string());
                    }
                }
            }
        }
    }
    Ok(files)
}

fn scan_backup_dir(backup_dir: &Path, repo_root: &Path) -> Result<Vec<String>> {
    let mut files = Vec::new();
    let repo_str = repo_root.to_string_lossy();

    for entry in walkdir::WalkDir::new(backup_dir).max_depth(3) {
        let entry = entry?;
        if entry.file_type().is_file() {
            if let Ok(content) = std::fs::read_to_string(entry.path()) {
                if let Some(first_line) = content.lines().next() {
                    if first_line.starts_with(repo_str.as_ref()) {
                        let p = Path::new(first_line);
                        if p.exists() {
                            files.push(first_line.to_string());
                        }
                    }
                }
            }
        }
    }
    Ok(files)
}

fn vscode_workspace_storage_dir() -> Option<PathBuf> {
    let config = dirs::config_dir()?;
    for candidate in &["Code", "Code - Insiders", "VSCodium"] {
        let p = config.join(candidate).join("User").join("workspaceStorage");
        if p.is_dir() {
            return Some(p);
        }
    }
    None
}

fn vscode_backup_dir() -> Option<PathBuf> {
    let config = dirs::config_dir()?;
    for candidate in &["Code", "Code - Insiders", "VSCodium"] {
        let p = config.join(candidate).join("User").join("Backups");
        if p.is_dir() {
            return Some(p);
        }
    }
    None
}

pub fn reopen_files(editor_name: &str, files: &[String]) -> Result<()> {
    if files.is_empty() {
        return Ok(());
    }

    let valid_files: Vec<&str> = files
        .iter()
        .filter(|f| {
            let p = Path::new(f.as_str());
            p.is_absolute() && p.exists()
        })
        .map(String::as_str)
        .collect();

    if valid_files.is_empty() {
        tracing::warn!("No valid open files to restore in editor");
        return Ok(());
    }

    let editor_cmd = match editor_name {
        "vscode" => "code",
        "vscodium" => "codium",
        other => other,
    };

    let status = std::process::Command::new(editor_cmd)
        .args(&valid_files)
        .status();

    match status {
        Ok(s) if s.success() => Ok(()),
        Ok(s) => {
            tracing::warn!("Editor exited with status: {s}");
            Ok(())
        }
        Err(e) => {
            tracing::warn!("Could not launch editor '{editor_cmd}': {e}");
            Ok(())
        }
    }
}
