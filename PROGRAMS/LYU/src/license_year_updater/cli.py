import os
import sys
import argparse
import datetime

from license_year_updater.core import (
    find_repositories,
    process_directory,
)


def main():
    parser = argparse.ArgumentParser(
        prog="lyu",
        description="Update copyright years in LICENSE files.",
    )
    parser.add_argument("--dir", default=".", help="Target directory path.")
    parser.add_argument(
        "--action",
        choices=["auto", "add", "subtract"],
        default="auto",
        help="auto: set to current year, add: increment by 1, subtract: decrement by 1.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Scan subdirectories containing a .git folder as individual repositories.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes without modifying files.",
    )
    args = parser.parse_args()

    target_dir = os.path.abspath(args.dir)
    current_year = datetime.datetime.now().year

    if not os.path.isdir(target_dir):
        print(f"[ERROR] Directory not found: {target_dir}")
        sys.exit(1)

    print(f"[INFO] Target directory: {target_dir}")
    print(f"[INFO] Action: {args.action}")
    print(f"[INFO] Dry run: {args.dry_run}")
    print(f"[INFO] Current year: {current_year}")

    if args.all:
        repos = find_repositories(target_dir)
        if not repos:
            print(f"[INFO] No repositories (with .git) found in {target_dir}")
            return
        for repo_path in repos:
            print(f"[REPO] Checking repository: {repo_path}")
            process_directory(repo_path, args.action, current_year, args.dry_run)
    else:
        process_directory(target_dir, args.action, current_year, args.dry_run)


if __name__ == "__main__":
    main()
