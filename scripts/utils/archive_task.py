# scripts/utils/archive_task.py
import os
import sys
import shutil
from datetime import datetime


def main():
    repo_root = os.environ.get("REPO_ROOT")
    if not repo_root:
        print("REPO_ROOT environment variable not set")
        sys.exit(1)
    os.chdir(repo_root)

    src_dir = os.path.join(repo_root, "cli_instruction")
    dest_root = os.path.join(repo_root, "cli_archives")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_dir = os.path.join(dest_root, timestamp)
    os.makedirs(dest_dir, exist_ok=True)

    for name in ["new_task.json", "complete.flag"]:
        src = os.path.join(src_dir, name)
        if os.path.exists(src):
            shutil.move(src, os.path.join(dest_dir, name))
            print(f"Moved {src} -> {dest_dir}")
        else:
            print(f"{src} not found")


if __name__ == "__main__":
    main()
