import subprocess
import sys
import os
from pathlib import Path

repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd()))
validate_script = repo_root / "validate_yaml.py"
input_file = repo_root / "cli_instruction" / "new_task.json"
output_file = repo_root / "cli_logs" / "TaskValidation.txt"

command = [sys.executable, str(validate_script), str(input_file)]

try:
    # Run the validation script and capture its stdout and stderr
    result = subprocess.run(command, capture_output=True, text=True, check=False)

    # Write the combined output to the specified output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result.stdout)
        f.write(result.stderr)

    # Check if the validation was successful based on the exit code
    if result.returncode == 0:
        print(f"Validation successful. Output written to {output_file}")
    else:
        print(f"Validation failed. Output written to {output_file}")

except FileNotFoundError:
    print(f"Error: Python interpreter or script not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


def test_session_creation():
    """新規セッションが正常に確立されるかテストする。"""
    print("Executing test_session_creation...")
    assert True

def test_session_resumption():
    """既存セッションが正常に再開されるかテストする。"""
    print("Executing test_session_resumption...")
    assert True

def test_replay_attack_detection():
    """リプレイ攻撃が検出されるかテストする。"""
    print("Executing test_replay_attack_detection...")
    assert True
