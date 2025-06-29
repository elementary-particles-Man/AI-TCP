#!/usr/bin/env python3
"""Generate a new_task.json file from stdin.

This script reads JSON content from standard input and saves it to
`cli_instructions/new_task.json` using an absolute path. If a previous
`new_task.json` exists, it will be moved to `cli_archives/` with a
timestamp before being overwritten.
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
import sys


def main() -> None:
    task_data_raw = sys.stdin.read().strip()
    if not task_data_raw:
        print("No task data provided", file=sys.stderr)
        sys.exit(1)

    try:
        task_data = json.loads(task_data_raw)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    repo_root = Path(__file__).resolve().parent
    instructions_dir = (repo_root / "cli_instructions").resolve()
    archive_dir = (repo_root / "cli_archives").resolve()

    instructions_dir.mkdir(parents=True, exist_ok=True)
    archive_dir.mkdir(parents=True, exist_ok=True)

    new_task_path = instructions_dir / "new_task.json"

    if new_task_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archived = archive_dir / f"new_task_{timestamp}.json"
        shutil.move(str(new_task_path), archived)
        print(f"Archived previous task to {archived}")

    with new_task_path.open("w", encoding="utf-8") as f:
        json.dump(task_data, f, indent=2, ensure_ascii=False)

    print(f"Saved new task to {new_task_path}")


if __name__ == "__main__":
    main()
