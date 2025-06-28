#!/usr/bin/env python3
"""Organize files in cli_archives.

This script renames old task files with a timestamp and moves
files older than 30 days into an ``old`` subdirectory.
"""
from __future__ import annotations
import shutil
from datetime import datetime, timedelta
from pathlib import Path

ARCHIVE_DIR = Path("cli_archives")
OLD_DIR = ARCHIVE_DIR / "old"
TARGET_FILES = [
    "new_task.json",
    "TaskValidation.txt",
    "output.json",
]


def _timestamped_name(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return path.with_name(f"{path.stem}_{stamp}{path.suffix}")


def rename_current_files() -> None:
    """Rename specific files in ``ARCHIVE_DIR`` with a timestamp."""
    for name in TARGET_FILES:
        file_path = ARCHIVE_DIR / name
        if file_path.exists():
            file_path.rename(_timestamped_name(file_path))


def move_old_files(days: int = 30) -> None:
    """Move files older than ``days`` days to ``OLD_DIR``."""
    threshold = datetime.now() - timedelta(days=days)
    OLD_DIR.mkdir(parents=True, exist_ok=True)
    for item in ARCHIVE_DIR.iterdir():
        if item.is_file() and item.parent != OLD_DIR:
            if datetime.fromtimestamp(item.stat().st_mtime) < threshold:
                shutil.move(str(item), str(OLD_DIR / item.name))


def main() -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    rename_current_files()
    move_old_files()


if __name__ == "__main__":
    main()
