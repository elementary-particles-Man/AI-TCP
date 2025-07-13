import subprocess
import sys
import os
from pathlib import Path

repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd()))
validate_script = repo_root / "validate_yaml.py"
input_file = repo_root / "cli_instruction" / "new_task.json"
output_file = repo_root / "cli_logs" / "TaskValidation.txt"

# Construct the command as a list of arguments
# The validate_yaml.py script expects the input file path as a command-line argument
command = [sys.executable, str(validate_script), str(input_file)]

try:
    # Run the validation script and capture its stdout and stderr
    # shell=False is important here to let subprocess handle argument parsing
    result = subprocess.run(command, capture_output=True, text=True, check=False, shell=False)

    # Write the combined output to the specified output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result.stdout)
        f.write(result.stderr)

    # Append "[Task Completed]" to the output file
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write("\n[Task Completed]\n")

    # Print a message to the console indicating success or failure
    if result.returncode == 0:
        print(f"Validation successful. Output written to {output_file}")
    else:
        print(f"Validation failed. Output written to {output_file}")

except FileNotFoundError:
    print(f"Error: Python interpreter or script not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")