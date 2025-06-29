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
    parser.add_argument("--keep", type=int, default=10, help="number of task entries to keep")
    args = parser.parse_args()

    archive_dir = Path("cli_archives")
    archive_dir.mkdir(parents=True, exist_ok=True)

    tasks = {}
    for f in archive_dir.glob("new_task_*.json"):
        ts = f.stem[len("new_task_") :]
        tasks[ts] = f.stat().st_mtime

    sorted_ts = sorted(tasks.items(), key=lambda x: x[1], reverse=True)
    remove_ts = [ts for ts, _ in sorted_ts[args.keep:]]

    for ts in remove_ts:
        for file in archive_dir.glob(f"*{ts}*"):
            print(f"Removing {file}")
            file.unlink()

    print(f"Cleanup complete. Kept {args.keep} tasks.")


if __name__ == "__main__":
    main()
