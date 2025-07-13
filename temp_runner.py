import subprocess
import sys
import os
from pathlib import Path

repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd()))
validate_script = repo_root / "validate_yaml.py"
input_file = repo_root / "cli_instruction" / "new_task.json"
output_file = repo_root / "cli_logs" / "TaskValidation.txt"

command = [sys.executable, str(validate_script), str(input_file), str(output_file)]

try:
    result = subprocess.run(command, capture_output=True, text=True, check=False, shell=False)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result.stdout)
        f.write(result.stderr)

    with open(output_file, 'a', encoding='utf-8') as f:
        f.write("\n[Task Completed]\n")

    if result.returncode == 0:
        print(f"Validation successful. Output written to {output_file}")
    else:
        print(f"Validation failed. Output written to {output_file}")

except FileNotFoundError:
    print(f"Error: Python interpreter or script not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
