import pytest
import json
import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime

# Adjust the import path based on your project structure
# Assuming task_bridge_runner.py is in scripts/
import sys
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

import task_bridge_runner

import task_bridge_runner



load_tasks = task_bridge_runner.load_tasks
save_output = task_bridge_runner.save_output
archive_logs = task_bridge_runner.archive_logs
execute_validate_files_task = task_bridge_runner.execute_validate_files_task
main = task_bridge_runner.main

# Fixture to set up a temporary directory for testing
@pytest.fixture
def temp_dirs(tmp_path, monkeypatch):
    # Create necessary directories within the temporary path
    (tmp_path / "AI-TCP_Structure" / "task_bridge" / "cli_instructions").mkdir(parents=True)
    (tmp_path / "cli_logs").mkdir(parents=True)
    (tmp_path / "logs").mkdir(parents=True)
    (tmp_path / "cli_archives").mkdir(parents=True)
    (tmp_path / "scripts" / "auto_ops").mkdir(parents=True)
    (tmp_path / "pytools").mkdir(parents=True)

    # Override global paths for testing using monkeypatch
    monkeypatch.setattr(task_bridge_runner, 'NEW_TASK_FILE', tmp_path / "AI-TCP_Structure" / "task_bridge" / "cli_instructions" / "new_task.json")
    monkeypatch.setattr(task_bridge_runner, 'OUTPUT_FILE', tmp_path / "cli_logs" / "output.json")
    monkeypatch.setattr(task_bridge_runner, 'TASK_VALIDATION_LOG', tmp_path / "logs" / "TaskValidation.txt")
    monkeypatch.setattr(task_bridge_runner, 'CLI_ARCHIVES_DIR', tmp_path / "cli_archives")
    yield tmp_path

# Test load_tasks function
def test_load_tasks_empty_file(temp_dirs):
    # Ensure the file doesn't exist initially
    assert not task_bridge_runner.NEW_TASK_FILE.exists()
    tasks = load_tasks()
    assert tasks == {"tasks": []}

def test_load_tasks_valid_json(temp_dirs):
    task_data = {"tasks": [{"task_type": "test"}]}
    with open(task_bridge_runner.NEW_TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(task_data, f)
    tasks = load_tasks()
    assert tasks == task_data

# Test save_output function
def test_save_output(temp_dirs):
    data = {"result": "success"}
    save_output(data)
    assert task_bridge_runner.OUTPUT_FILE.exists()
    with open(task_bridge_runner.OUTPUT_FILE, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    assert loaded_data == data

# Test archive_logs function
def test_archive_logs(temp_dirs):
    # Create dummy log files
    with open(task_bridge_runner.TASK_VALIDATION_LOG, "w", encoding="utf-8") as f:
        f.write("test log")
    with open(task_bridge_runner.OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"test": "output"}, f)

    archive_logs()

    # Check if originals are unlinked
    assert not task_bridge_runner.TASK_VALIDATION_LOG.exists()
    assert not task_bridge_runner.OUTPUT_FILE.exists()

    # Check if archived files exist with timestamp
    archived_logs = list(task_bridge_runner.CLI_ARCHIVES_DIR.glob("TaskValidation_*.txt"))
    archived_outputs = list(task_bridge_runner.CLI_ARCHIVES_DIR.glob("output_*.json"))
    assert len(archived_logs) == 1
    assert len(archived_outputs) == 1
    assert archived_logs[0].read_text() == "test log"
    assert json.load(archived_outputs[0].open(encoding="utf-8")) == {"test": "output"}

# Test execute_validate_files_task function
@patch('subprocess.run')
def test_execute_validate_files_task_success(mock_run, temp_dirs):
    mock_run.return_value = MagicMock(returncode=0, stdout="Pytest output", stderr="")
    task_config = {"execution_target": {"files_to_check": "file1.py;file2.py"}}
    result = execute_validate_files_task(task_config)

    mock_run.assert_called_once()
    assert result["status"] == "completed"
    assert result["returncode"] == 0
    assert "stdout" in result

@patch('subprocess.run')
def test_execute_validate_files_task_failure(mock_run, temp_dirs):
    mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="Error")
    task_config = {"execution_target": {"files_to_check": "file1.py"}}
    result = execute_validate_files_task(task_config)

    assert result["status"] == "failed"
    assert result["returncode"] == 1
    assert "stderr" in result

# Test main function (integration-like test)
@patch('time.sleep', return_value=None) # Prevent actual sleep during test
@patch('task_bridge_runner.execute_validate_files_task')
@patch('task_bridge_runner.archive_logs')
@patch('task_bridge_runner.save_output')
@patch('task_bridge_runner.subprocess.run') # For task_log_parser.py call
def test_main_function_validate_files(mock_subprocess_run, mock_save_output, mock_archive_logs, mock_execute_task, mock_sleep, temp_dirs):
    # Simulate new_task.json content
    task_data = {"tasks": [
        {"task_type": "validate_files", "execution_target": {"files_to_check": "file.py"}}
    ]}
    with open(task_bridge_runner.NEW_TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(task_data, f)

    initial_mtime = task_bridge_runner.NEW_TASK_FILE.stat().st_mtime

    # Mock execute_validate_files_task to return a successful result
    mock_execute_task.return_value = {"task_type": "validate_files", "status": "completed", "returncode": 0}
    mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="Parser output", stderr="")

    # Run main for a short period to allow one loop iteration
    with patch('task_bridge_runner.Path.stat') as mock_stat:
        mock_stat.return_value.st_mtime = initial_mtime # First check, no change
        main() # This will run the loop once
        
        # Simulate a change in new_task.json
        task_bridge_runner.NEW_TASK_FILE.touch() # Update modification time
        mock_stat.return_value.st_mtime = task_bridge_runner.NEW_TASK_FILE.stat().st_mtime # Second check, change detected
        main() # This will run the loop again, processing the task

    mock_execute_task.assert_called_once()
    mock_save_output.assert_called_once()
    mock_archive_logs.assert_called_once()
    mock_subprocess_run.assert_called_once_with([
        "python",
        "D:/My Data/Develop/Project INFINITY/AI-TCP/pytools/task_log_parser.py"
    ], capture_output=True, text=True)

@patch('time.sleep', return_value=None)
@patch('task_bridge_runner.execute_validate_files_task')
@patch('task_bridge_runner.archive_logs')
@patch('task_bridge_runner.save_output')
@patch('task_bridge_runner.subprocess.run')
def test_main_function_unknown_task(mock_subprocess_run, mock_save_output, mock_archive_logs, mock_execute_task, mock_sleep, temp_dirs):
    task_data = {"tasks": [
        {"task_type": "unknown_task", "execution_target": {}}
    ]}
    with open(task_bridge_runner.NEW_TASK_FILE, "w") as f:
        json.dump(task_data, f)

    initial_mtime = NEW_TASK_FILE.stat().st_mtime

    with patch('task_bridge_runner.Path.stat') as mock_stat:
        mock_stat.return_value.st_mtime = initial_mtime
        main()
        NEW_TASK_FILE.touch()
        mock_stat.return_value.st_mtime = NEW_TASK_FILE.stat().st_mtime
        main()

    mock_execute_task.assert_not_called() # Should not call execute_validate_files_task for unknown type
    mock_save_output.assert_called_once()
    mock_archive_logs.assert_called_once()
    mock_subprocess_run.assert_called_once() # Still calls parser


@patch('time.sleep', return_value=None)
@patch('task_bridge_runner.execute_validate_files_task')
@patch('task_bridge_runner.archive_logs')
@patch('task_bridge_runner.save_output')
@patch('task_bridge_runner.subprocess.run')
def test_main_function_generate_documentation(mock_subprocess_run, mock_save_output, mock_archive_logs, mock_execute_task, mock_sleep, temp_dirs):
    task_data = {"tasks": [
        {"task_type": "generate_documentation", "execution_target": {"output_path": "docs/test.md"}}
    ]}
    with open(task_bridge_runner.NEW_TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(task_data, f)

    initial_mtime = task_bridge_runner.NEW_TASK_FILE.stat().st_mtime

    with patch('task_bridge_runner.Path.stat') as mock_stat:
        mock_stat.return_value.st_mtime = initial_mtime
        main()
        NEW_TASK_FILE.touch()
        mock_stat.return_value.st_mtime = NEW_TASK_FILE.stat().st_mtime
        main()

    mock_execute_task.assert_not_called() # Should not call execute_validate_files_task
    mock_save_output.assert_called_once()
    mock_archive_logs.assert_called_once()
    mock_subprocess_run.assert_called_once_with([
        "python",
        "D:/My Data/Develop/Project INFINITY/AI-TCP/pytools/generate_cli_docs.py"
    ], capture_output=True, text=True)
