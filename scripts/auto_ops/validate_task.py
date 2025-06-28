import sys
from pathlib import Path
import subprocess
import json

# This script is designed to be called by the AI-TCP agent
# It reads its configuration from a JSON file (new_task.json) for log_path and pytest_target
# files_to_check are passed as command-line arguments

def main():
    # Ensure this script is only called by the agent via new_task.json
    # Manual execution is prohibited.
    if not os.environ.get("AI_TCP_AGENT_CALL", "false").lower() == "true":
        print("Error: This script must be launched by the AI-TCP agent via new_task.json.")
        sys.exit(1)

    # Assuming new_task.json is located at a known path relative to the project root
    # For this example, we'll hardcode the path as it's provided in the context
    new_task_json_path = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/AI-TCP_Structure/task_bridge/cli_instructions/new_task.json")

    if not new_task_json_path.exists():
        print(f"Error: new_task.json not found at {new_task_json_path}")
        sys.exit(1)

    with new_task_json_path.open("r", encoding="utf-8") as f:
        full_task_config = json.load(f)

    # Find the current task within the 'tasks' list
    current_task_config = None
    for task in full_task_config.get("tasks", []):
        if task.get("task_type") == "validate_files": # Assuming this is the task we are executing
            current_task_config = task
            break

    if current_task_config is None:
        print("Error: Could not find 'validate_files' task in new_task.json")
        sys.exit(1)

    files_to_check_str = current_task_config["execution_target"]["files_to_check"]
    files_to_check = [f.strip() for f in files_to_check_str.split(';') if f.strip()]

    log_path_str = current_task_config["execution_target"].get("log_path", "D:/My Data/Develop/Project INFINITY/AI-TCP/logs/TaskValidation.txt") # Default value
    pytest_target = current_task_config["execution_target"].get("pytest_target", "tests/test_validator_git_commit.py") # Default value

    log_path = Path(log_path_str)
    with log_path.open("a", encoding="utf-8") as f:
        f.write("=== ファイル存在チェック ===\n")
        all_files_exist = True
        for file in files_to_check:
            path = Path(file.strip())
            if path.exists():
                f.write(f"[OK] {path}\n")
            else:
                f.write(f"[NG] {path} (NOT FOUND)\n")
                all_files_exist = False

        f.write("\n=== pytest 実行 ===\n")
        files_to_check_arg = ";".join(files_to_check)
        pytest_command = ["pytest", pytest_target, f"--files-to-check={files_to_check_arg}"]
        result = subprocess.run(pytest_command, capture_output=True, text=True)
        f.write(result.stdout)
        f.write("\n=== Validation Completed ===\n")

    if not all_files_exist or result.returncode != 0:
        sys.exit(1) # Return non-zero exit code on error

if __name__ == "__main__":
    # This block is now primarily for agent-driven execution
    # Manual execution will be prevented by the check at the beginning of main()
    main()
