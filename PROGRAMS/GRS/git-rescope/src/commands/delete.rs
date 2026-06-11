 
use anyhow::{bail, Result};
use crate::storage::{config::AppConfig, store::{find_snapshot, load_store, remove_snapshot}};

pub fn cmd_delete(config: &AppConfig, query: &str, quiet: bool) -> Result<()> {
    let store = load_store(config)?;
    let snapshot = find_snapshot(&store, query)
        .ok_or_else(|| anyhow::anyhow!("No snapshot found matching '{query}'"))?
        .clone();

    if !quiet {
        print!(
            "Delete snapshot '{}' (id={})? This cannot be undone. [y/N] ",
            snapshot.description,
            snapshot.short_id()
        );
        use std::io::Write;
        let _ = std::io::stdout().flush();
        let mut line = String::new();
        std::io::stdin().read_line(&mut line)?;
        if !line.trim().eq_ignore_ascii_case("y") {
            bail!("Aborted.");
        }
    }

    let removed = remove_snapshot(config, &snapshot.id)?;
    if removed && !quiet {
        println!("✓ Snapshot {} deleted.", snapshot.short_id());
    }
    Ok(())
}
