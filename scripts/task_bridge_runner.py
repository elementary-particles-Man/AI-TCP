import time
import json
import subprocess
import os
from pathlib import Path
from datetime import datetime
import shutil

REPO_ROOT = Path("D:/Dev/AI-TCP") # Assuming this is the junction path

NEW_TASK_FILE = REPO_ROOT / "cli_instruction" / "new_task.json"
COMPLETE_FLAG_FILE = REPO_ROOT / "cli_instruction" / "complete.flag"
TASK_VALIDATION_LOG = REPO_ROOT / "cli_logs" / "TaskValidation.txt"
CLI_ARCHIVES_DIR = REPO_ROOT / "cli_archives"

def log_message(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def archive_logs():
    if not CLI_ARCHIVES_DIR.exists():
        CLI_ARCHIVES_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Archive new_task.json
    if NEW_TASK_FILE.exists():
        shutil.copy(NEW_TASK_FILE, CLI_ARCHIVES_DIR / f"new_task_{timestamp}.json")
        log_message(f"Archived {NEW_TASK_FILE.name} to {CLI_ARCHIVES_DIR}")

    # Archive TaskValidation.txt
    if TASK_VALIDATION_LOG.exists():
        shutil.copy(TASK_VALIDATION_LOG, CLI_ARCHIVES_DIR / f"TaskValidation_{timestamp}.txt")
        log_message(f"Archived {TASK_VALIDATION_LOG.name} to {CLI_ARCHIVES_DIR}")

def run_command_with_retry(command, retries=5, delay=5):
    for i in range(retries):
        try:
            log_message(f"Attempt {i+1}/{retries}: Running command: {' '.join(command)}")
            process = subprocess.run(command, check=True, capture_output=True, text=True, cwd=REPO_ROOT)
            log_message(f"Command stdout:\n{process.stdout}")
            if process.stderr:
                log_message(f"Command stderr:\n{process.stderr}", level="WARNING")
            return process
        except subprocess.CalledProcessError as e:
            log_message(f"Command failed with exit code {e.returncode}: {e.stderr}", level="ERROR")
            if i < retries - 1:
                log_message(f"Retrying in {delay} seconds...", level="INFO")
                time.sleep(delay)
            else:
                log_message("Max retries reached. Command failed.", level="CRITICAL")
                raise
        except OSError as e: # Catches WinError32 and other OS errors
            log_message(f"OS Error during command execution: {e}", level="ERROR")
            if i < retries - 1:
                log_message(f"Retrying in {delay} seconds...", level="INFO")
                time.sleep(delay)
            else:
                log_message("Max retries reached. OS Error.", level="CRITICAL")
                raise

def main():
    last_modified_time = None
    log_message("Task Bridge Runner started. Monitoring new_task.json...")

    while True:
        current_modified_time = None
        if NEW_TASK_FILE.exists():
            current_modified_time = NEW_TASK_FILE.stat().st_mtime

        if current_modified_time and current_modified_time != last_modified_time:
            log_message(f"Detected change in {NEW_TASK_FILE.name}. Processing new task...")
            last_modified_time = current_modified_time

            archive_logs() # Archive logs before starting new task

            # Clear complete.flag if it exists
            if COMPLETE_FLAG_FILE.exists():
                COMPLETE_FLAG_FILE.unlink()
                log_message(f"Removed existing {COMPLETE_FLAG_FILE.name}")

            try:
                # Placeholder for launching Gemini CUI
                # You need to replace this with the actual command to launch your Gemini CUI
                # Example: ["python", "path/to/your/gemini_cui_script.py"]
                # Or if it's an executable: ["gemini_cui.exe"]
                # Ensure the command is correct for your environment.
                gemini_cui_command = ["python", str(REPO_ROOT / "dispatcher.py")] # Assuming dispatcher.py is the entry point for Gemini CUI
                
                # Set environment variable for the agent call
                os.environ["AI_TCP_AGENT_CALL"] = "true"
                
                log_message(f"Launching Gemini CUI with command: {' '.join(gemini_cui_command)}")
                run_command_with_retry(gemini_cui_command)
                log_message("Gemini CUI execution completed (or exited).")

                # Monitor for complete.flag or log message
                task_completed = False
                start_time = time.time()
                timeout = 3600 # 1 hour timeout for task completion

                while not task_completed and (time.time() - start_time) < timeout:
                    if COMPLETE_FLAG_FILE.exists():
                        log_message(f"Detected {COMPLETE_FLAG_FILE.name}. Task completed.")
                        task_completed = True
                        break
                    
                    # Check for "[Task Completed]" in the log file
                    if TASK_VALIDATION_LOG.exists():
                        with open(TASK_VALIDATION_LOG, "r", encoding="utf-8", errors="ignore") as f:
                            if "[Task Completed]" in f.read():
                                log_message("Detected '[Task Completed]' in log. Task completed.")
                                task_completed = True
                                break
                    
                    time.sleep(5) # Check every 5 seconds

                if not task_completed:
                    log_message("Task timed out or did not complete within the expected time.", level="WARNING")

            except Exception as e:
                log_message(f"An error occurred during task processing: {e}", level="CRITICAL")
            finally:
                # Unset environment variable
                if "AI_TCP_AGENT_CALL" in os.environ:
                    del os.environ["AI_TCP_AGENT_CALL"]
                
                # Ensure complete.flag is created if task finished successfully
                if task_completed and not COMPLETE_FLAG_FILE.exists():
                    COMPLETE_FLAG_FILE.touch()
                    log_message(f"Created {COMPLETE_FLAG_FILE.name} as a fallback.")

        time.sleep(90) # Check every 90 seconds

if __name__ == "__main__":
    main()
