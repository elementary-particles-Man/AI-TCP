import time
from pathlib import Path
import sys
import subprocess
import os

# Set stdout encoding to UTF-8 for proper display of emojis and special characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from validator import main_validator
from dispatcher import dispatch_task
from utils import load_json_safely, write_log, archive_task

# This comment is added for Git commit verification. (5th time)

INSTRUCTION_PATH = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/AI-TCP_Structure/task_bridge/cli_instructions/new_task.json")
OUTPUT_LOG = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/cli_logs/output.json")
ARCHIVE_DIR = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/cli_archives/")

print(f"✅ Watching: {INSTRUCTION_PATH}")

while True:
    if INSTRUCTION_PATH.exists():
        try:
            task_config = load_json_safely(INSTRUCTION_PATH)
            for task in task_config.get("tasks", []):
                if task.get("task_type") == "validate_files":
                    # Set environment variable to indicate agent call
                    os.environ["AI_TCP_AGENT_CALL"] = "true"
                    # Execute validate_task.py
                    files_to_check_str = task["execution_target"]["files_to_check"]
                    subprocess.run(["python", "scripts/auto_ops/validate_task.py", files_to_check_str], check=True)
                    del os.environ["AI_TCP_AGENT_CALL"]
                # Add other task types here as needed

            # Original task dispatching logic (if still needed for other task types)
            # main_validator(task)
            # result = dispatch_task(task)
            # write_log(result, OUTPUT_LOG)
            archive_task(INSTRUCTION_PATH, ARCHIVE_DIR)
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            # Ensure environment variable is cleaned up
            if "AI_TCP_AGENT_CALL" in os.environ:
                del os.environ["AI_TCP_AGENT_CALL"]
    time.sleep(3)
