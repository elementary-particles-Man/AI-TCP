import subprocess
import sys
import os

validate_script = os.path.abspath("D:/My Data/Develop/Project INFINITY/AI-TCP/validate_yaml.py")
input_file = os.path.abspath("D:/My Data/Develop/Project INFINITY/AI-TCP/cli_instruction/new_task.json")
output_file = os.path.abspath("D:/My Data/Develop/Project INFINITY/AI-TCP/cli_logs/TaskValidation.txt")

# Construct the command as a list of arguments
# The validate_yaml.py script expects the input file path and output file path as command-line arguments
command = [sys.executable, validate_script, input_file, output_file]

try:
    # Run the validation script and capture its stdout and stderr
    # shell=False is important here to let subprocess handle argument parsing
    result = subprocess.run(command, capture_output=True, text=True, check=False, shell=False)

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