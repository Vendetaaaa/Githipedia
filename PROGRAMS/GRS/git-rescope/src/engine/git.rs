 
use anyhow::{bail, Context, Result};
use git2::{Repository, StashApplyOptions, StashFlags, StatusOptions};
use sha2::{Digest, Sha256};
use std::path::{Path, PathBuf};

use crate::storage::schema::StorageMethod;

 
pub fn open_repo(start: &Path) -> Result<Repository> {
    Repository::discover(start)
        .context("Not inside a Git repository. Run grs from within a repo.")
}

 
pub fn current_branch(repo: &Repository) -> Result<String> {
    let head = repo.head().context("Cannot read HEAD")?;
    if head.is_branch() {
        Ok(head.shorthand().unwrap_or("HEAD").to_owned())
    } else {
        Ok("(detached HEAD)".to_owned())
    }
}

 
pub fn repo_root(repo: &Repository) -> Result<PathBuf> {
    repo.workdir()
        .context("Bare repositories are not supported")?
        .canonicalize()
        .context("Cannot canonicalise workdir path")
}

 
pub fn has_modifications(repo: &Repository) -> Result<bool> {
    let mut opts = StatusOptions::new();
    opts.include_untracked(true)
        .recurse_untracked_dirs(false)
        .include_ignored(false);
    let statuses = repo.statuses(Some(&mut opts))
        .context("Cannot read repository status")?;
    Ok(!statuses.is_empty())
}

 
pub fn capture_changes(
    repo: &Repository,
    description: &str,
    _patches_dir: &Path,
) -> Result<(StorageMethod, Option<String>)> {
    let mut opts = StatusOptions::new();
    opts.include_untracked(true)
        .recurse_untracked_dirs(false)
        .include_ignored(false);
    let statuses = repo.statuses(Some(&mut opts))?;

    if statuses.is_empty() {
        return Ok((StorageMethod::Clean, None));
    }

    let diff_sha = compute_diff_sha(repo)?;

    let sig = repo
        .signature()
        .or_else(|_| git2::Signature::now("git-rescope", "grs@localhost"))
        .context("Cannot create Git signature")?;

    let stash_msg = format!("grs: {description}");
    let flags = StashFlags::INCLUDE_UNTRACKED | StashFlags::KEEP_INDEX;

    let repo_ptr = repo as *const Repository as *mut Repository;
    let stash_oid = unsafe {
        (*repo_ptr).stash_save(&sig, &stash_msg, Some(flags))
    }
    .context("Failed to create git stash — is the repository in a valid state?")?;

    
    let stash_index = 0usize;

    tracing::info!("Created stash {} (oid={})", stash_index, stash_oid);

    Ok((
        StorageMethod::GitStash { stash_index },
        Some(diff_sha),
    ))
}

 
pub fn restore_changes(
    repo: &Repository,
    method: &StorageMethod,
    _patches_dir: &Path,
    _patch_sha256: Option<&str>,
) -> Result<()> {
    match method {
        StorageMethod::Clean => Ok(()),
        StorageMethod::GitStash { stash_index } => {
            let mut apply_opts = StashApplyOptions::new();
            apply_opts.reinstantiate_index();

            let repo_ptr = repo as *const Repository as *mut Repository;
            unsafe {
                (*repo_ptr).stash_pop(*stash_index, Some(&mut apply_opts))
            }
            .context("Failed to restore stash — manual `git stash pop` may be needed")?;
            Ok(())
        }
        StorageMethod::PatchFile { patch_filename } => {
            
            let path = _patches_dir.join(patch_filename);
            if !path.exists() {
                bail!("Patch file not found: {}", path.display());
            }
            
            if let Some(expected_sha) = _patch_sha256 {
                let content = std::fs::read(&path)
                    .context("Cannot read patch file")?;
                let actual_sha = hex::encode(Sha256::digest(&content));
                if actual_sha != expected_sha {
                    bail!(
                        "Patch file integrity check FAILED.\n\
                         Expected: {expected_sha}\n\
                         Actual:   {actual_sha}\n\
                         The patch may have been tampered with. Aborting restore."
                    );
                }
            }
            
            let content = std::fs::read_to_string(&path)
                .context("Cannot read patch file")?;
            let diff = git2::Diff::from_buffer(content.as_bytes())
                .context("Cannot parse patch file as unified diff")?;
            repo.apply(&diff, git2::ApplyLocation::WorkDir, None)
                .context("Failed to apply patch file")?;
            Ok(())
        }
    }
}

 
pub fn checkout_branch(repo: &Repository, branch_name: &str) -> Result<()> {
    
    if has_modifications(repo)? {
        bail!(
            "Working tree has uncommitted changes that are NOT part of this snapshot.\n\
             Please run `grs save` first or manually commit/stash your changes.\n\
             Use --force to override (data loss risk)."
        );
    }

    let branch = repo
        .find_branch(branch_name, git2::BranchType::Local)
        .with_context(|| format!("Branch '{branch_name}' not found"))?;
    let branch_ref = branch.get().name()
        .context("Invalid branch reference")?;

    let obj = repo
        .revparse_single(branch_ref)
        .with_context(|| format!("Cannot resolve branch '{branch_name}'"))?;

    repo.checkout_tree(&obj, None)
        .with_context(|| format!("Cannot checkout tree for '{branch_name}'"))?;

    repo.set_head(branch_ref)
        .with_context(|| format!("Cannot set HEAD to '{branch_name}'"))?;

    Ok(())
}

 
fn compute_diff_sha(repo: &Repository) -> Result<String> {
    let head = repo.head().ok().and_then(|h| h.peel_to_tree().ok());
    let diff = match head {
        Some(tree) => repo
            .diff_tree_to_workdir_with_index(Some(&tree), None)
            .context("Cannot compute diff")?,
        None => repo
            .diff_index_to_workdir(None, None)
            .context("Cannot compute diff (no HEAD)")?,
    };
    let mut content: Vec<u8> = Vec::new();
    diff.print(git2::DiffFormat::Patch, |_, _, line| {
        content.extend_from_slice(line.content());
        true
    })
    .ok();

    let hash = Sha256::digest(&content);
    Ok(hex::encode(hash))
}
