use anyhow::{Context, Result};
use sha2::{Digest, Sha256};
use std::path::PathBuf;
use zeroize::Zeroizing;

fn key_path() -> Result<PathBuf> {
    let base = dirs::config_dir().context("Cannot determine config dir")?;
    Ok(base.join("git-rescope").join("machine.key"))
}

pub fn derive_machine_key() -> Result<Zeroizing<Vec<u8>>> {
    let path = key_path()?;

    if path.exists() {
        let raw = std::fs::read(&path).context("Cannot read machine.key")?;
        if raw.len() < 32 {
            anyhow::bail!("machine.key is too short — delete it to regenerate");
        }
        return Ok(Zeroizing::new(raw));
    }

    let mut hasher = Sha256::new();
    hasher.update(b"git-rescope-v1");

    if let Ok(hostname) = std::env::var("HOSTNAME").or_else(|_| std::env::var("COMPUTERNAME")) {
        hasher.update(hostname.as_bytes());
    }

    if let Ok(user) = std::env::var("USER").or_else(|_| std::env::var("USERNAME")) {
        hasher.update(user.as_bytes());
    }

    let salt: [u8; 16] = {
        use std::time::{SystemTime, UNIX_EPOCH};
        let t = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .subsec_nanos()
            .to_le_bytes();
        let mut s = [0u8; 16];
        s[..4].copy_from_slice(&t);
        s[4..8].copy_from_slice(&t);
        s[8..12].copy_from_slice(&t);
        s[12..16].copy_from_slice(&t);
        s
    };
    hasher.update(salt);

    let key_bytes = hasher.finalize().to_vec();

    std::fs::create_dir_all(path.parent().unwrap())?;
    std::fs::write(&path, &key_bytes).context("Cannot write machine.key")?;

    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o600))?;
    }

    Ok(Zeroizing::new(key_bytes))
}
