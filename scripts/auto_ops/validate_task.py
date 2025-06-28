import sys
from pathlib import Path
import subprocess
import json

# This script is designed to be called by the AI-TCP agent
# It reads its configuration from a JSON file (new_task.json) for files_to_check, log_path, and pytest_target

def main():
    # Assuming new_task.json is located at a known path relative to the project root
    # For this example, we'll hardcode the path as it's provided in the context
    new_task_json_path = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/AI-TCP_Structure/task_bridge/cli_instructions/new_task.json")

    if not new_task_json_path.exists():
        print(f"Error: new_task.json not found at {new_task_json_path}")
        sys.exit(1)

    with new_task_json_path.open("r", encoding="utf-8") as f:
        task_config = json.load(f)

    files_to_check = task_config["execution_target"]["files_to_check"]
    log_path_str = task_config["task_payload"]["log_path"]
    pytest_target = task_config["task_payload"]["pytest_target"]

    log_path = Path(log_path_str)
    with log_path.open("a", encoding="utf-8") as f:
        f.write("=== ファイル存在チェック ===\n")
        for file in files_to_check:
            path = Path(file.strip())
            if path.exists():
                f.write(f"[OK] {path}\n")
            else:
                f.write(f"[NG] {path} (NOT FOUND)\n")

        f.write("\n=== pytest 実行 ===\n")
        result = subprocess.run(["pytest", pytest_target], capture_output=True, text=True)
        f.write(result.stdout)
        f.write("\n=== Validation Completed ===\n")

if __name__ == "__main__":
    main()