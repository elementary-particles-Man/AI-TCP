# scripts/utils/clean_archives.py
import os
import argparse
from pathlib import Path


def main() -> None:
    repo_root = os.environ.get("REPO_ROOT")
    if not repo_root:
        print("REPO_ROOT environment variable not set")
        return
    os.chdir(repo_root)

    parser = argparse.ArgumentParser(description="Clean old archives")
    parser.add_argument("--keep", type=int, default=50, help="number of files to keep")
    args = parser.parse_args()

    archive_dir = Path("cli_archives")
    archive_dir.mkdir(parents=True, exist_ok=True)

    files = [f for f in archive_dir.iterdir() if f.is_file()]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    for f in files[args.keep:]:
        f.unlink()
        print(f"Removed {f}")


if __name__ == "__main__":
    main()
