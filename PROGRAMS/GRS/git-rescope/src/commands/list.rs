 
use anyhow::Result;

use crate::storage::{config::AppConfig, store::load_store};

pub fn cmd_list(config: &AppConfig, all: bool) -> Result<()> {
    let store = load_store(config)?;

    if store.snapshots.is_empty() {
        println!("No snapshots found. Run `grs save \"description\"` to create one.");
        return Ok(());
    }

    let cwd = std::env::current_dir().ok();
    let current_repo = cwd.as_ref().and_then(|d| {
        git2::Repository::discover(d)
            .ok()
            .and_then(|r| r.workdir().and_then(|w| w.canonicalize().ok()))
            .map(|p| p.to_string_lossy().into_owned())
    });

    let snapshots: Vec<_> = store
        .snapshots
        .iter()
        .filter(|s| {
            if all {
                true
            } else if let Some(ref repo) = current_repo {
                &s.repo_path == repo
            } else {
                true
            }
        })
        .collect();

    if snapshots.is_empty() {
        println!(
            "No snapshots for this repository. Use --all to list all repos, \
             or run `grs save` to create one."
        );
        return Ok(());
    }

    
    println!(
        "{:<10} {:<22} {:<20} {:<8} {}",
        "ID", "TIMESTAMP", "BRANCH", "FILES", "DESCRIPTION"
    );
    println!("{}", "─".repeat(80));

    for s in &snapshots {
        println!(
            "{:<10} {:<22} {:<20} {:<8} {}",
            s.short_id(),
            s.timestamp.format("%Y-%m-%d %H:%M:%S"),
            truncate(&s.branch, 20),
            s.open_files.len(),
            truncate(&s.description, 40),
        );
    }

    println!("\n{} snapshot(s) listed.", snapshots.len());
    Ok(())
}

fn truncate(s: &str, max: usize) -> String {
    if s.len() <= max {
        s.to_string()
    } else {
        format!("{}…", &s[..max.saturating_sub(1)])
    }
}
