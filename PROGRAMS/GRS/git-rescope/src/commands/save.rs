 
use anyhow::{bail, Result};
use std::time::Instant;

use crate::engine::{editor, git};
use crate::security::guard::{sanitise_open_files, validate_description};
use crate::storage::{
    config::AppConfig,
    schema::Snapshot,
    store::add_snapshot,
};

pub fn cmd_save(
    config: &AppConfig,
    description: &str,
    yes: bool,
    quiet: bool,
) -> Result<()> {
    let t0 = Instant::now();

    
    validate_description(description)?;

    
    let cwd = std::env::current_dir()?;
    let repo = git::open_repo(&cwd)?;
    let repo_root = git::repo_root(&repo)?;
    let branch = git::current_branch(&repo)?;

    
    if !yes && !quiet {
        println!(
            "Saving context on branch '{}' — this will stash any uncommitted changes.",
            branch
        );
        print!("Continue? [y/N] ");
        use std::io::Write;
        let _ = std::io::stdout().flush();
        let mut line = String::new();
        std::io::stdin().read_line(&mut line)?;
        if !line.trim().eq_ignore_ascii_case("y") {
            bail!("Aborted.");
        }
    }

    
    let editor_state = editor::detect_editor_state(&repo_root)
        .unwrap_or(None);
    let (editor_name, raw_open_files) = match editor_state {
        Some(s) => (Some(s.editor_name), s.open_files),
        None => (None, Vec::new()),
    };
    let open_files = sanitise_open_files(&raw_open_files);

    if !quiet && !open_files.is_empty() {
        println!("  Detected {} open file(s) in editor.", open_files.len());
    }

    
    let patches_dir = config.patches_dir();
    std::fs::create_dir_all(&patches_dir)?;

    let (storage_method, patch_sha256) =
        git::capture_changes(&repo, description, &patches_dir)?;

    
    let snapshot = Snapshot::new(
        repo_root.to_string_lossy().into_owned(),
        branch.clone(),
        description.to_owned(),
        open_files,
        storage_method,
        patch_sha256,
        editor_name,
    );

    let snap_id = snapshot.short_id().to_owned();
    let snap_full_id = snapshot.id.clone();
    add_snapshot(config, snapshot)?;

    let elapsed = t0.elapsed().as_millis();

    if !quiet {
        println!(
            "✓ Snapshot saved  id={snap_id}...  branch='{branch}'  ({elapsed}ms)\n\
             Full ID: {snap_full_id}"
        );
        if elapsed > 200 {
            eprintln!("⚠ Capture took {elapsed}ms (target: <200ms). Check repo size.");
        }
    }

    Ok(())
}
