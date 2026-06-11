use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Snapshot {
    pub id: String,

    pub repo_path: String,

    pub branch: String,

    pub timestamp: DateTime<Utc>,

    pub description: String,

    pub open_files: Vec<String>,

    pub storage_method: StorageMethod,

    pub patch_sha256: Option<String>,

    pub detected_editor: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum StorageMethod {
    GitStash { stash_index: usize },
    PatchFile { patch_filename: String },
    Clean,
}

impl Snapshot {
    pub fn new(
        repo_path: String,
        branch: String,
        description: String,
        open_files: Vec<String>,
        storage_method: StorageMethod,
        patch_sha256: Option<String>,
        detected_editor: Option<String>,
    ) -> Self {
        Self {
            id: Uuid::new_v4().to_string(),
            repo_path,
            branch,
            timestamp: Utc::now(),
            description,
            open_files,
            storage_method,
            patch_sha256,
            detected_editor,
        }
    }

    pub fn short_id(&self) -> &str {
        &self.id[..8]
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct StorageRoot {
    pub schema_version: u32,
    pub snapshots: Vec<Snapshot>,
}
