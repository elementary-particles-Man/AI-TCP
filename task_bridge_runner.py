import os
import time
import json
from dispatcher import dispatch_task
from validator import main_validator
from utils import write_log, archive_task, load_json_safely

INSTRUCTION_PATH = "cli_instructions/new_task.json"
OUTPUT_PATH = "cli_logs/output.json"
ARCHIVE_DIR = "cli_archives"


def task_bridge_runner():
    print("[AI-TCP] Task bridge runner started. Monitoring for tasks...")
    while True:
        if os.path.exists(INSTRUCTION_PATH):
            try:
                task = load_json_safely(INSTRUCTION_PATH)
                main_validator(task)
                result = dispatch_task(task)
                write_log(result, OUTPUT_PATH)
                archive_task(task, ARCHIVE_DIR)
            except Exception as e:
                error_result = {
                    "execution_status": "error",
                    "message": str(e),
                    "details": {}
                }
                write_log(error_result, OUTPUT_PATH)
            finally:
                try:
                    os.remove(INSTRUCTION_PATH)
                except Exception:
                    pass
        time.sleep(2)  # Polling interval


if __name__ == "__main__":
    task_bridge_runner()
