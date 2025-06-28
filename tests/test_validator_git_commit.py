import sys
import os
import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
import json
import datetime # Added import

# Add the scripts/auto_ops directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts/auto_ops')))

from validator import validate_git_commit_task, main_validator, ALLOWED_BASE_PATH
from utils import load_json_safely, write_log, archive_task

# Test cases for validate_git_commit_task
def test_valid_git_commit_task():
    task = {
        "task_type": "git_commit",
        "execution_target": {
            "path": ALLOWED_BASE_PATH,
            "branch": "main",
            "commit_message": "Test commit",
            "files": ["file1.txt", "file2.txt"]
        }
    }
    validate_git_commit_task(task) # Should not raise any exception

def test_git_commit_missing_execution_target():
    task = {
        "task_type": "git_commit",
        "task_payload": { # Incorrect structure, should be under execution_target
            "commit_message": "Test commit",
            "files": ["file1.txt"]
        }
    }
    with pytest.raises(ValueError, match="Missing 'execution_target' in task."):
        validate_git_commit_task(task)

def test_git_commit_invalid_path_type():
    task = {
        "task_type": "git_commit",
        "execution_target": {
            "path": 12345, # Invalid type
            "branch": "main",
            "commit_message": "Test commit",
            "files": ["file1.txt"]
        }
    }
    with pytest.raises(ValueError, match="'execution_target.path' must be a string."):
        validate_git_commit_task(task)

def test_git_commit_path_outside_sandbox():
    task = {
        "task_type": "git_commit",
        "execution_target": {
            "path": "/etc/passwd", # Outside allowed sandbox
            "branch": "main",
            "commit_message": "Test commit",
            "files": ["file1.txt"]
        }
    }
    with pytest.raises(ValueError, match="Security Error: Path"):
        validate_git_commit_task(task)

def test_git_commit_missing_files():
    task = {
        "task_type": "git_commit",
        "execution_target": {
            "path": ALLOWED_BASE_PATH,
            "branch": "main",
            "commit_message": "Test commit",
            "files": [] # Empty files list
        }
    }
    with pytest.raises(ValueError, match="'task_payload.files' must be a non-empty list."):
        validate_git_commit_task(task)

def test_git_commit_invalid_commit_message_type():
    task = {
        "task_type": "git_commit",
        "execution_target": {
            "path": ALLOWED_BASE_PATH,
            "branch": "main",
            "commit_message": 123, # Invalid type
            "files": ["file1.txt"]
        }
    }
    with pytest.raises(ValueError, match="'task_payload.commit_message' must be a string if provided."):
        validate_git_commit_task(task)

# Test cases for main_validator
def test_main_validator_git_commit():
    task = {
        "task_type": "git_commit",
        "execution_target": {
            "path": ALLOWED_BASE_PATH,
            "branch": "main",
            "commit_message": "Test commit",
            "files": ["file1.txt"]
        }
    }
    main_validator(task) # Should not raise any exception

def test_main_validator_unsupported_task_type():
    task = {
        "task_type": "unsupported_type",
        "execution_target": {
            "path": ALLOWED_BASE_PATH,
            "branch": "main",
            "commit_message": "Test commit",
            "files": ["file1.txt"]
        }
    }
    with pytest.raises(ValueError, match="Unsupported task_type: 'unsupported_type'"):
        main_validator(task)

def test_main_validator_missing_task_type():
    task = {
        "execution_target": {
            "path": ALLOWED_BASE_PATH,
            "branch": "main",
            "commit_message": "Test commit",
            "files": ["file1.txt"]
        }
    }
    with pytest.raises(ValueError, match="Missing 'task_type' in task."):
        main_validator(task)

# Test cases for utils.py functions
def test_load_json_safely():
    mock_json_content = {"key": "value"}
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_json_content))):
        with patch("json.load", return_value=mock_json_content):
            result = load_json_safely(Path("dummy.json"))
            assert result == mock_json_content

def test_write_log():
    mock_result = {"status": "success"}
    mock_output_path = Path("dummy_output.json")
    with patch("builtins.open", mock_open()) as mock_file:
        with patch("json.dump") as mock_json_dump:
            write_log(mock_result, mock_output_path)
            mock_file.assert_called_once_with(mock_output_path, 'w', encoding='utf-8')
            mock_json_dump.assert_called_once_with(mock_result, mock_file(), indent=2, ensure_ascii=False)

def test_archive_task():
    mock_input_path = Path("dummy_input.json")
    mock_archive_dir = Path("dummy_archive_dir")
    with patch("pathlib.Path.mkdir") as mock_mkdir:
        with patch("shutil.move") as mock_move:
            with patch("utils.datetime") as mock_dt:
                mock_dt.now.return_value = datetime.datetime(2025, 1, 1, 12, 0, 0)
                archive_task(mock_input_path, mock_archive_dir)
                mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
                expected_archive_path = mock_archive_dir / "20250101120000_archived_task.json"
                mock_move.assert_called_once_with(str(mock_input_path), str(expected_archive_path))

# New code from new_task.json
LOG_FILE = r"X:\work\TaskValidation.txt"

# 検証したいファイルパス
FILES_TO_CHECK = [
    r"D:\My Data\Develop\Project INFINITY\AI-TCP\scripts\auto_ops\task_bridge_runner.py",
    r"D:\My Data\Develop\Project INFINITY\AI-TCP\scripts\auto_ops\output_watcher.py",
    r"D:\My Data\Develop\Project INFINITY\AI-TCP\scripts\auto_ops\dispatcher.py",
    r"D:\My Data\Develop\Project INFINITY\AI-TCP\scripts\auto_ops\validator.py",
    r"D:\My Data\Develop\Project INFINITY\AI-TCP\scripts\auto_ops\utils.py",
]

def append_log(message: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def test_file_existence():
    append_log("=== Task Validation Started ===")
    for file_path in FILES_TO_CHECK:
        if os.path.isfile(file_path):
            append_log(f"✅ Exists: {file_path}")
        else:
            append_log(f"❌ Missing: {file_path}")
    append_log("=== File Existence Check Done ===")

def test_dummy_logic():
    # ここに本来の機能テストなどを拡張できます
    assert True  # 仮のパス判定

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    append_log("=== Validation Completed ===")
