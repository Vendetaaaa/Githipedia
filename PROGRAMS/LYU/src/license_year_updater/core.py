import os
import re

LICENSE_FILENAMES = ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"]

YEAR_RANGE_PATTERN = re.compile(r"(?P<start>\d{4})\s*-\s*(?P<end>\d{4})")
SINGLE_YEAR_PATTERN = re.compile(r"\d{4}")


def compute_new_year(year, action, current_year):
    if action == "auto":
        return current_year
    if action == "add":
        return year + 1
    if action == "subtract":
        return year - 1
    return year


def find_license_files(directory):
    found = []
    try:
        entries = os.listdir(directory)
    except OSError as e:
        print(f"[ERROR] Could not read directory {directory}: {e}")
        return found
    for name in entries:
        if name in LICENSE_FILENAMES:
            full_path = os.path.join(directory, name)
            if os.path.isfile(full_path):
                found.append(full_path)
    return found


def find_repositories(directory):
    repos = []
    try:
        entries = os.listdir(directory)
    except OSError as e:
        print(f"[ERROR] Could not read directory {directory}: {e}")
        return repos
    for name in sorted(entries):
        full_path = os.path.join(directory, name)
        if os.path.isdir(full_path):
            git_path = os.path.join(full_path, ".git")
            if os.path.isdir(git_path):
                repos.append(full_path)
    return repos


def process_license_file(file_path, action, current_year, dry_run):
    print(f"[CHECK] Scanning license file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        print(f"[ERROR] Could not read file {file_path}: {e}")
        return

    range_match = YEAR_RANGE_PATTERN.search(content)
    if range_match:
        start_year = int(range_match.group("start"))
        end_year = int(range_match.group("end"))
        new_end_year = compute_new_year(end_year, action, current_year)
        original_str = range_match.group(0)
        new_str = f"{start_year}-{new_end_year}"

        if new_end_year == end_year:
            print(f"[SKIP] {file_path}: year already up to date ({original_str})")
            return

        new_content = content[: range_match.start()] + new_str + content[range_match.end() :]
        apply_change(file_path, original_str, new_str, new_content, dry_run)
        return

    single_match = SINGLE_YEAR_PATTERN.search(content)
    if single_match:
        old_year = int(single_match.group(0))
        original_str = single_match.group(0)

        if action == "subtract":
            new_year = compute_new_year(old_year, action, current_year)
            new_str = str(new_year)
        else:
            new_year = compute_new_year(old_year, action, current_year)
            if new_year == old_year:
                print(f"[SKIP] {file_path}: year already up to date ({original_str})")
                return
            new_str = f"{old_year}-{new_year}"

        if new_str == original_str:
            print(f"[SKIP] {file_path}: year already up to date ({original_str})")
            return

        new_content = content[: single_match.start()] + new_str + content[single_match.end() :]
        apply_change(file_path, original_str, new_str, new_content, dry_run)
        return

    print(f"[SKIP] {file_path}: no year pattern found")


def apply_change(file_path, original_str, new_str, new_content, dry_run):
    print(f"[CHANGE] {original_str} -> {new_str}")
    if dry_run:
        print(f"[DRY-RUN] Would update {file_path}")
        return
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[SUCCESS] Updated {file_path}")
    except OSError as e:
        print(f"[ERROR] Could not write file {file_path}: {e}")


def process_directory(directory, action, current_year, dry_run):
    license_files = find_license_files(directory)
    if not license_files:
        print(f"[INFO] No license files found in {directory}")
        return
    for file_path in license_files:
        process_license_file(file_path, action, current_year, dry_run)
