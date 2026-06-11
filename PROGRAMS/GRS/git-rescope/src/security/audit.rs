use anyhow::{Context, Result};
use chrono::Utc;
use std::fs::OpenOptions;
use std::io::Write;

use crate::storage::config::AppConfig;

pub struct AuditLog {
    path: std::path::PathBuf,
    enabled: bool,
}

impl AuditLog {
    pub fn new(config: &AppConfig) -> Result<Self> {
        Ok(Self {
            path: config.audit_log_path(),
            enabled: config.audit_logging,
        })
    }

    pub fn record(&self, cmd: &str) -> Result<()> {
        if !self.enabled {
            return Ok(());
        }
        let user = std::env::var("USER")
            .or_else(|_| std::env::var("USERNAME"))
            .unwrap_or_else(|_| "unknown".into());
        let ts = Utc::now().format("%Y-%m-%dT%H:%M:%SZ");
        let line = format!("[{ts}] user={user} cmd={cmd}\n");

        let mut file = OpenOptions::new()
            .create(true)
            .append(true)
            .open(&self.path)
            .context("Cannot open audit log")?;

        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            let _ = std::fs::set_permissions(&self.path, std::fs::Permissions::from_mode(0o640));
        }

        file.write_all(line.as_bytes()).context("Cannot write audit log")?;
        Ok(())
    }

    pub fn print_recent(&self, n: usize) -> Result<()> {
        if !self.path.exists() {
            println!("No audit log found.");
            return Ok(());
        }
        let content = std::fs::read_to_string(&self.path).context("Cannot read audit log")?;
        let lines: Vec<&str> = content.lines().collect();
        let start = lines.len().saturating_sub(n);
        for line in &lines[start..] {
            println!("{}", line);
        }
        Ok(())
    }
}
