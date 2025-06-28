import sys
from pathlib import Path

# ルートパスを追加
sys.path.append(str(Path(__file__).resolve().parents[1]))

from validator import validate_git_commit_task, ALLOWED_BASE_PATH

def test_valid_git_commit():
    task = {
        "task_type": "git_commit",
        "execution_target": {"path": ALLOWED_BASE_PATH},
        "task_payload": {
            "commit_message": "Test commit",
            "files": ["README.md"]
        }
    }
    validate_git_commit_task(task)
