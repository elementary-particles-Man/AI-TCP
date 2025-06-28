import time
from pathlib import Path
from validator import main_validator
from dispatcher import dispatch_task
from utils import load_json_safely, write_log, archive_task

# This comment is added for Git commit verification. (5th time)

INSTRUCTION_PATH = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/cli_instructions/new_task.json")
OUTPUT_LOG = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/cli_logs/output.json")
ARCHIVE_DIR = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/cli_archives/")

print(f"✅ Watching: {INSTRUCTION_PATH}")

while True:
    if INSTRUCTION_PATH.exists():
        try:
            task = load_json_safely(INSTRUCTION_PATH)
            main_validator(task)
            result = dispatch_task(task)
            write_log(result, OUTPUT_LOG)
            archive_task(INSTRUCTION_PATH, ARCHIVE_DIR)
        except Exception as e:
            print(f"Error: {str(e)}")
    time.sleep(3)
