 
use anyhow::{bail, Result};

use crate::engine::{editor, git};
use crate::storage::{config::AppConfig, store::{find_snapshot, load_store}};

pub fn cmd_restore(
    config: &AppConfig,
    query: &str,
    force: bool,
    quiet: bool,
) -> Result<()> {
    
    let store = load_store(config)?;
    let snapshot = find_snapshot(&store, query)
        .ok_or_else(|| anyhow::anyhow!("No snapshot found matching '{query}'"))?
        .clone();

    if !quiet {
        println!(
            "Restoring snapshot '{}' (id={})  branch='{}'",
            snapshot.description,
            snapshot.short_id(),
            snapshot.branch,
        );
    }

    
    let cwd = std::env::current_dir()?;
    let repo = git::open_repo(&cwd)?;

    
    if !force && git::has_modifications(&repo)? {
        bail!(
            "Your working tree has uncommitted changes.\n\
             Please commit, stash, or save them with `grs save` before restoring.\n\
             (Use --force to bypass — DATA LOSS RISK)"
        );
    }

    
    if !quiet {
        print!(
            "This will checkout branch '{}' and restore working tree changes. Continue? [y/N] ",
            snapshot.branch
        );
        use std::io::Write;
        let _ = std::io::stdout().flush();
        let mut line = String::new();
        std::io::stdin().read_line(&mut line)?;
        if !line.trim().eq_ignore_ascii_case("y") {
            bail!("Aborted.");
        }
    }

    
    let current_branch = git::current_branch(&repo)?;
    if current_branch != snapshot.branch {
        // Checkout: we use a relaxed version since we already checked dirty
        let branch = repo
            .find_branch(&snapshot.branch, git2::BranchType::Local)
            .map_err(|_| {
                anyhow::anyhow!(
                    "Branch '{}' not found locally. \
                     It may need to be fetched from remote.",
                    snapshot.branch
                )
            })?;
        let branch_ref = branch.get().name().unwrap();
        let obj = repo.revparse_single(branch_ref)?;
        repo.checkout_tree(&obj, None)?;
        repo.set_head(branch_ref)?;
        if !quiet {
            println!("  ✓ Checked out branch '{}'", snapshot.branch);
        }
    }

    
    let patches_dir = config.patches_dir();
    git::restore_changes(
        &repo,
        &snapshot.storage_method,
        &patches_dir,
        snapshot.patch_sha256.as_deref(),
    )?;

    if !quiet {
        println!("  ✓ Working tree changes restored");
    }

    
    if !snapshot.open_files.is_empty() {
        let editor_name = snapshot
            .detected_editor
            .as_deref()
            .unwrap_or("vscode");
        editor::reopen_files(editor_name, &snapshot.open_files)?;
        if !quiet {
            println!(
                "  ✓ Reopened {} file(s) in editor",
                snapshot.open_files.len()
            );
        }
    }

    if !quiet {
        println!("\n✓ Context restored successfully.");
    }

    Ok(())
}
