use anyhow::{Context, Result};
use hmac::{Hmac, Mac};
use sha2::Sha256;

use super::config::AppConfig;
use super::schema::{Snapshot, StorageRoot};
use crate::security::keys::derive_machine_key;

type HmacSha256 = Hmac<Sha256>;

pub fn load_store(config: &AppConfig) -> Result<StorageRoot> {
    let path = config.storage_path();
    if !path.exists() {
        return Ok(StorageRoot {
            schema_version: 1,
            snapshots: Vec::new(),
        });
    }

    let raw = std::fs::read_to_string(&path)
        .context("Failed to read storage.json")?;

    if config.integrity_checks {
        verify_signature(config, raw.as_bytes())
            .context("storage.json integrity check FAILED — file may have been tampered with")?;
    }

    let store: StorageRoot = serde_json::from_str(&raw)
        .context("storage.json is malformed")?;
    Ok(store)
}

pub fn save_store(config: &AppConfig, store: &StorageRoot) -> Result<()> {
    let path = config.storage_path();
    std::fs::create_dir_all(path.parent().unwrap())?;

    let serialised = serde_json::to_string_pretty(store)
        .context("Failed to serialise store")?;

    let tmp = path.with_extension("json.tmp");
    std::fs::write(&tmp, &serialised)
        .context("Failed to write storage.json.tmp")?;
    std::fs::rename(&tmp, &path)
        .context("Failed to rename storage.json.tmp")?;

    if config.integrity_checks {
        write_signature(config, serialised.as_bytes())
            .context("Failed to write integrity signature")?;
    }

    Ok(())
}

pub fn add_snapshot(config: &AppConfig, snapshot: Snapshot) -> Result<()> {
    let mut store = load_store(config)?;
    store.snapshots.push(snapshot);
    save_store(config, &store)
}

pub fn remove_snapshot(config: &AppConfig, id: &str) -> Result<bool> {
    let mut store = load_store(config)?;
    let before = store.snapshots.len();
    store.snapshots.retain(|s| s.id != id && !s.id.starts_with(id));
    let removed = store.snapshots.len() < before;
    if removed {
        save_store(config, &store)?;
    }
    Ok(removed)
}

pub fn find_snapshot<'a>(
    store: &'a StorageRoot,
    query: &str,
) -> Option<&'a Snapshot> {
    if let Some(s) = store.snapshots.iter().find(|s| s.id == query) {
        return Some(s);
    }
    if let Some(s) = store.snapshots.iter().find(|s| s.id.starts_with(query)) {
        return Some(s);
    }
    let lower = query.to_lowercase();
    store
        .snapshots
        .iter()
        .find(|s| s.description.to_lowercase().contains(&lower))
}

fn write_signature(config: &AppConfig, data: &[u8]) -> Result<()> {
    let key = derive_machine_key()?;
    let mut mac = HmacSha256::new_from_slice(&key)
        .context("HMAC key error")?;
    mac.update(data);
    let result = mac.finalize().into_bytes();
    std::fs::write(config.storage_sig_path(), hex::encode(result))
        .context("Cannot write signature file")?;
    Ok(())
}

fn verify_signature(config: &AppConfig, data: &[u8]) -> Result<()> {
    let sig_path = config.storage_sig_path();
    if !sig_path.exists() {
        write_signature(config, data)?;
        return Ok(());
    }

    let stored_hex = std::fs::read_to_string(&sig_path)
        .context("Cannot read signature file")?;
    let stored_bytes = hex::decode(stored_hex.trim())
        .context("Corrupt signature file")?;

    let key = derive_machine_key()?;
    let mut mac = HmacSha256::new_from_slice(&key)
        .context("HMAC key error")?;
    mac.update(data);
    mac.verify_slice(&stored_bytes)
        .map_err(|_| anyhow::anyhow!(
            "HMAC mismatch — storage.json has been modified outside of grs. \
             If this is expected (e.g. manual edit), delete `storage.json.sig` to reset."
        ))
}
