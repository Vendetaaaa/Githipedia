<div align="center">

```
 ██████╗ ██████╗ ███████╗
██╔════╝ ██╔══██╗██╔════╝
██║  ███╗██████╔╝███████╗
██║   ██║██╔══██╗╚════██║
╚██████╔╝██║  ██║███████║
 ╚═════╝ ╚═╝  ╚═╝╚══════╝
  git-rescope  (grs)
```

</div>

<div align="center">

**Freeze your entire dev context in one command.**  
Switch tasks without losing your place. Restore everything exactly as you left it.

![License](https://img.shields.io/badge/license-MIT-green)
![Local](https://img.shields.io/badge/storage-100%25%20local-blue)

</div>

---

## What is it?

You're deep into fixing a bug, 8 files open, half-written code everywhere, sweat dripping (such a nightmare tbh) and suddenly you get pulled onto something urgent (ofc you do). `grs` lets you freeze that exact moment and come back to it later, perfectly intact.

```
grs save "fixing prod auth bug"    ← one command, everything frozen
... go handle the emergency ...
grs restore 17ca9f9a               ← back exactly where you left it
```

---

## Quick Start

```cmd
# Build
cargo build --release

# Add to PATH (Windows)
setx PATH "%PATH%;C:\path\to\git-rescope\target\release"

# Use it
grs save "my task description"
grs list
grs restore <id>
grs ui
```

---

## Commands

| Command | What it does |
|---|---|
| `grs save "description"` | Snapshot current branch, changes, and open files |
| `grs list` | List all snapshots for the current repo |
| `grs restore <id>` | Restore by ID prefix or description substring |
| `grs delete <id>` | Permanently delete a snapshot |
| `grs ui` | Open the interactive TUI dashboard |
| `grs terms` | Display full Terms of Service |
| `grs audit-log` | Show security audit log |

---

## How It Works

```
grs save
  1. Capture  — stashes your code via libgit2 (no git subprocess)
  2. Store    — saves branch, files, timestamp to local JSON
  3. Sign     — HMAC-SHA256 signs the snapshot against tampering

grs restore
  1. Verify   — checks HMAC signature, aborts if tampered
  2. Checkout — switches back to your saved branch
  3. Unstash  — your code changes reappear
  4. Reopen   — relaunches editor with your saved files
```

---

## Local Storage Layout

Everything lives on your machine only. Nothing is ever sent anywhere.

```
%APPDATA%\git-rescope\             (Windows)
~/.config/git-rescope/             (Linux/macOS)
  ├── storage.json                 ← snapshot metadata
  ├── storage.json.sig             ← HMAC-SHA256 tamper signature
  ├── machine.key                  ← per-device secret key (mode 600)
  ├── audit.log                    ← append-only invocation log
  └── logs\                        ← rolling debug logs
```

---

## Security

| Control | Detail |
|---|---|
| **HMAC integrity** | `storage.json` is signed on every write, verified on every read |
| **No shell injection** | All Git operations use native libgit2 — `git.exe` is never spawned |
| **Path validation** | All paths checked for traversal sequences (`..`) before use |
| **Input sanitisation** | Descriptions validated for length and forbidden shell characters |
| **Key zeroization** | HMAC key bytes zeroed from memory on drop via `zeroize` crate |
| **Audit logging** | Every CLI invocation logged with timestamp and username |
| **Dirty-tree guard** | Restore aborts if working tree has un-snapshotted changes |
| **100% local** | Zero network code — nothing ever leaves your machine |

---

## Editor Support

| Editor | Status |
|---|---|
| VS Code | ✅ Supported |
| VS Codium | ✅ Supported |
| VS Code Insiders | ✅ Supported |

---

## Built With

- **[git2](https://crates.io/crates/git2)** — Native libgit2 Rust bindings
- **[ratatui](https://crates.io/crates/ratatui)** — Terminal UI framework
- **[clap](https://crates.io/crates/clap)** — CLI argument parsing
- **[serde_json](https://crates.io/crates/serde_json)** — Snapshot serialisation
- **[sha2 + hmac](https://crates.io/crates/sha2)** — Storage integrity
- **[zeroize](https://crates.io/crates/zeroize)** — Secure key memory clearing

---

## Requirements

- Rust stable 1.75+
- Windows, Linux, or macOS
- libgit2 (vendored — no system install needed)

---

## Legal

Licensed under the [MIT License](LICENSE).  
Run `grs terms` for the full Terms of Service.

> ⚠️ **Warning:** Git operations modify your working tree. Always ensure your work
> is backed up. The authors accept no liability for data loss.

---

<div align="center">
  <sub>Built with Rust · 100% local · No telemetry · No network</sub>
</div>
