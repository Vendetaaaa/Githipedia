# LYU — License Year Updater

Update copyright years in `LICENSE` files. One command, no setup beyond Python.

Part of [Githipedia](https://github.com/Vendetaaaa/Githipedia/tree/main/PROGRAMS/LYU).

## Install

```bash
pip install "git+https://github.com/Vendetaaaa/Githipedia.git#subdirectory=PROGRAMS/LYU"
```

Requires Python 3.7+ and Git installed and on PATH.

PyPI release (`pip install lyu`) coming soon.

## Usage

```bash
lyu [--dir PATH] [--action auto|add|subtract] [--all] [--dry-run]
```

## Flags

| Flag | Description | Default |
|---|---|---|
| `--dir` | Target directory | `.` |
| `--action` | `auto` = current year, `add` = +1, `subtract` = -1 | `auto` |
| `--all` | Scan subfolders with a `.git` folder as separate repos | off |
| `--dry-run` | Preview changes, don't write files | off |

## Examples

```bash
# Preview update in current folder
lyu --dry-run

# Update all repos in ~/projects to current year
lyu --dir ~/projects --all

# Roll back one year
lyu --action subtract
```

## How it works

- Looks for `LICENSE`, `LICENSE.md`, `LICENSE.txt`, `COPYING`.
- **Year range** (`2021-2025`): only the end year updates → `2021-2026`.
- **Single year** (`2025`): becomes a range on `auto`/`add` → `2025-2026`.
- Already up to date? File is skipped.

## Output

```
[CHANGE] 2021-2025 -> 2021-2026
[SUCCESS] Updated ./LICENSE
```

Use `--dry-run` to see `[DRY-RUN]` instead of `[SUCCESS]` — nothing is written.

## Uninstall

```bash
pip uninstall lyu
```
