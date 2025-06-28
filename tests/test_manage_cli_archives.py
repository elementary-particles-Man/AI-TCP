import os
from pathlib import Path
from datetime import datetime, timedelta

import importlib.util

spec = importlib.util.spec_from_file_location(
    "manage_cli_archives", Path(__file__).parent.parent / "scripts" / "manage_cli_archives.py"
)
manage_cli_archives = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manage_cli_archives)


def test_rename_and_move(tmp_path):
    archive = tmp_path / "cli_archives"
    archive.mkdir()

    # create target files
    for name in manage_cli_archives.TARGET_FILES:
        (archive / name).write_text("dummy")

    # create an old file
    old_file = archive / "old_file.txt"
    old_file.write_text("old")
    old_time = (datetime.now() - timedelta(days=31)).timestamp()
    os.utime(old_file, (old_time, old_time))

    # patch directories
    manage_cli_archives.ARCHIVE_DIR = archive
    manage_cli_archives.OLD_DIR = archive / "old"

    manage_cli_archives.main()

    # renamed files
    assert not (archive / "new_task.json").exists()
    assert not (archive / "TaskValidation.txt").exists()
    assert not (archive / "output.json").exists()
    assert len(list(archive.glob("new_task_*.json"))) == 1
    assert len(list(archive.glob("TaskValidation_*.txt"))) == 1
    assert len(list(archive.glob("output_*.json"))) == 1

    # moved old file
    moved = list((archive / "old").iterdir())
    assert len(moved) == 1
    assert moved[0].name == "old_file.txt"
