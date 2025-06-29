import os


def test_files_exist():
    files_to_check = [
        "scripts/auto_ops/validate_task.py",
        "scripts/auto_ops/task_bridge_runner.py",
    ]
    for file in files_to_check:
        assert os.path.exists(file), f"{file} が存在しません"

