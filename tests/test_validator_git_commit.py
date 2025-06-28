import pytest
import os
from validator import validate_git_commit_task, ALLOWED_BASE_PATH

# This comment is added for Git commit verification. (5th time)

def test_valid_git_commit():
    task = {
        "task_type": "git_commit",
        "execution_target": {
            "path": os.path.join(ALLOWED_BASE_PATH, "subdir")
        },
        "task_payload": {
            "commit_message": "test commit",
            "files": ["file1.txt", "file2.txt"]
        }
    }
    validate_git_commit_task(task)

def test_missing_files():
    task = {
        "task_type": "git_commit",
        "execution_target": {
            "path": os.path.join(ALLOWED_BASE_PATH, "repo")
        },
        "task_payload": {
            "commit_message": "test commit"
        }
    }
    with pytest.raises(ValueError, match="files"):
        validate_git_commit_task(task)

def test_invalid_path_type():
    task = {
        "task_type": "git_commit",
        "execution_target": {
            "path": 12345
        },
        "task_payload": {
            "files": ["a.txt"]
        }
    }
    with pytest.raises(ValueError, match="path"):
        validate_git_commit_task(task)

def test_sandbox_violation():
    task = {
        "task_type": "git_commit",
        "execution_target": {
            "path": "C:/Windows/System32"
        },
        "task_payload": {
            "files": ["a.txt"]
        }
    }
    with pytest.raises(ValueError, match="outside the allowed sandbox"):
        validate_git_commit_task(task)
