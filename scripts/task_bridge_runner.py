import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
import shutil
import os

NEW_TASK_FILE = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/AI-TCP_Structure/task_bridge/cli_instructions/new_task.json")
OUTPUT_FILE = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/cli_logs/output.json")
TASK_VALIDATION_LOG = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/logs/TaskValidation.txt")
CLI_ARCHIVES_DIR = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/cli_archives")

def load_tasks():
    if not NEW_TASK_FILE.exists():
        return {"tasks": []}
    with NEW_TASK_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_output(data):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def archive_logs():
    CLI_ARCHIVES_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Archive TaskValidation.txt
    if TASK_VALIDATION_LOG.exists():
        shutil.copy(TASK_VALIDATION_LOG, CLI_ARCHIVES_DIR / f"TaskValidation_{timestamp}.txt")
        TASK_VALIDATION_LOG.unlink() # Clear current log after archiving

    # Archive output.json
    if OUTPUT_FILE.exists():
        shutil.copy(OUTPUT_FILE, CLI_ARCHIVES_DIR / f"output_{timestamp}.json")
        OUTPUT_FILE.unlink() # Clear current output after archiving

def execute_validate_files_task(task_config):
    files_to_check = task_config["execution_target"]["files_to_check"]
    
    # Set environment variable to allow validate_task.py to run
    env = os.environ.copy()
    env["AI_TCP_AGENT_CALL"] = "true"

    command = [
        "python",
        "D:/My Data/Develop/Project INFINITY/AI-TCP/scripts/auto_ops/validate_task.py"
    ]
    
    # For now, validate_task.py reads new_task.json directly.
    # In the future, we might pass arguments directly if the script changes.
    
    result = subprocess.run(command, capture_output=True, text=True, env=env)
    
    return {
        "task_type": "validate_files",
        "status": "completed" if result.returncode == 0 else "failed",
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
        "timestamp": datetime.now().isoformat()
    }

def main():
    print(f"Monitoring {NEW_TASK_FILE} for new tasks...")
    last_modified = None
    
    while True:
        current_modified = NEW_TASK_FILE.stat().st_mtime if NEW_TASK_FILE.exists() else None

        if current_modified and current_modified != last_modified:
            print(f"Detected change in {NEW_TASK_FILE}. Processing tasks...")
            last_modified = current_modified
            
            tasks_config = load_tasks()
            results = []
            
            for task in tasks_config.get("tasks", []):
                if task["task_type"] == "validate_files":
                    print(f"Executing validate_files task: {task}")
                    result = execute_validate_files_task(task)
                    results.append(result)
                elif task["task_type"] == "generate_documentation":
                    print(f"Executing generate_documentation task: {task}")
                    doc_command = [
                        "python",
                        "D:/My Data/Develop/Project INFINITY/AI-TCP/pytools/generate_cli_docs.py"
                    ]
                    doc_result = subprocess.run(doc_command, capture_output=True, text=True)
                    results.append({
                        "task_type": "generate_documentation",
                        "status": "completed" if doc_result.returncode == 0 else "failed",
                        "stdout": doc_result.stdout,
                        "stderr": doc_result.stderr,
                        "returncode": doc_result.returncode,
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    print(f"Unknown task type: {task['task_type']}")
                    results.append({
                        "task_type": task["task_type"],
                        "status": "skipped",
                        "message": "Unknown task type",
                        "timestamp": datetime.now().isoformat()
                    })
            
            save_output({"results": results})
            print("Tasks processed. Generating log report...")
            # Call the log parser after task execution and before archiving
            parser_command = [
                "python",
                "D:/My Data/Develop/Project INFINITY/AI-TCP/pytools/task_log_parser.py"
            ]
            parser_result = subprocess.run(parser_command, capture_output=True, text=True)
            if parser_result.returncode != 0:
                print(f"Error running log parser: {parser_result.stderr}")
            else:
                print(f"Log parser output: {parser_result.stdout}")
            
            print("Archiving logs...")
            archive_logs()
            print("Logs archived. Waiting for next change...")
            
        time.sleep(5) # Check every 5 seconds

if __name__ == "__main__":
    main()
