// what is this

use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppConfig {
    pub schema_version: u32,

    pub data_dir: PathBuf,

    #[serde(default = "default_true")]
    pub integrity_checks: bool,

    #[serde(default = "default_true")]
    pub audit_logging: bool,
}

fn default_true() -> bool {
    true
}

impl AppConfig {
    pub fn default_data_dir() -> Result<PathBuf> {
        let base = dirs::config_dir()
            .context("Cannot determine home/config directory")?;
        Ok(base.join("git-rescope"))
    }

    pub fn load_or_create() -> Result<Self> {
        let data_dir = Self::default_data_dir()?;
        std::fs::create_dir_all(&data_dir)
            .with_context(|| format!("Cannot create data dir: {}", data_dir.display()))?;

        let config_path = data_dir.join("config.json");
        if config_path.exists() {
            let raw = std::fs::read_to_string(&config_path)
                .context("Failed to read config.json")?;
            let cfg: AppConfig = serde_json::from_str(&raw)
                .context("config.json is malformed — delete it to reset")?;
            return Ok(cfg);
        }

        let cfg = AppConfig {
            schema_version: 1,
            data_dir: data_dir.clone(),
            integrity_checks: true,
            audit_logging: true,
        };
        let serialised = serde_json::to_string_pretty(&cfg)?;
        std::fs::write(&config_path, serialised)
            .context("Failed to write config.json")?;
        Ok(cfg)
    }

    pub fn data_dir(&self) -> &Path {
        &self.data_dir
    }

    pub fn storage_path(&self) -> PathBuf {
        self.data_dir.join("storage.json")
    }

    pub fn storage_sig_path(&self) -> PathBuf {
        self.data_dir.join("storage.json.sig")
    }

    pub fn audit_log_path(&self) -> PathBuf {
        self.data_dir.join("audit.log")
    }

    pub fn patches_dir(&self) -> PathBuf {
        self.data_dir.join("patches")
    }
}
