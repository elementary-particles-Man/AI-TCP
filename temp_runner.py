import subprocess
import sys
import os

validate_script = os.path.abspath("D:/My Data/Develop/Project INFINITY/AI-TCP/validate_yaml.py")
input_file = os.path.abspath("D:/My Data/Develop/Project INFINITY/AI-TCP/cli_instruction/new_task.json")
output_file = os.path.abspath("D:/My Data/Develop/Project INFINITY/AI-TCP/cli_logs/TaskValidation.txt")

command = [sys.executable, validate_script, input_file, output_file]

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
