import time
from pathlib import Path
from validator import main_validator
from dispatcher import dispatch_task
from utils import load_json_safely, write_log, archive_task

# ✅ リネーム後のパスに合わせる！
INSTRUCTION_PATH = Path("F:/マイドライブ/AI-TCP_Task/cli_instructions/new_task.json")
OUTPUT_LOG = Path("F:/マイドライブ/AI-TCP_Task/cli_logs/output.json")
ARCHIVE_DIR = Path("F:/マイドライブ/AI-TCP_Task/cli_archives/")

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
