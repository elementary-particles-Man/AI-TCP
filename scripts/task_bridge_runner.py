import json
import os
import shutil
from datetime import datetime
from pathlib import Path
import os.path
import builtins


class _PathProxy:
    def _current(self) -> Path:
        return globals()["NEW_TASK_FILE"]

    def __getattr__(self, name):
        return getattr(self._current(), name)

    def __fspath__(self):
        return os.fspath(self._current())

    def __repr__(self) -> str:  # pragma: no cover - simple delegate
        return repr(self._current())
import subprocess

NEW_TASK_FILE = Path("AI-TCP_Structure/task_bridge/cli_instructions/new_task.json")
OUTPUT_FILE = Path("cli_logs/output.json")
TASK_VALIDATION_LOG = Path("logs/TaskValidation.txt")
CLI_ARCHIVES_DIR = Path("cli_archives")

# Paths for additional tools
TASK_LOG_PARSER = "D:/My Data/Develop/Project INFINITY/AI-TCP/pytools/task_log_parser.py"
GENERATE_CLI_DOCS = "D:/My Data/Develop/Project INFINITY/AI-TCP/pytools/generate_cli_docs.py"
VALIDATE_TASK_SCRIPT = Path("scripts/auto_ops/validate_task.py")

# Provide unqualified access for legacy tests
builtins.NEW_TASK_FILE = _PathProxy()

LAST_MTIME = None

def load_tasks() -> dict:
    if not NEW_TASK_FILE.exists():
        return {"tasks": []}
    with NEW_TASK_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_output(data: dict) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def archive_logs() -> None:
    CLI_ARCHIVES_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if TASK_VALIDATION_LOG.exists():
        shutil.move(TASK_VALIDATION_LOG, CLI_ARCHIVES_DIR / f"TaskValidation_{timestamp}.txt")
    if OUTPUT_FILE.exists():
        shutil.move(OUTPUT_FILE, CLI_ARCHIVES_DIR / f"output_{timestamp}.json")

def execute_validate_files_task(task: dict) -> dict:
    files = task.get("execution_target", {}).get("files_to_check", "")
    env = os.environ.copy()
    env["AI_TCP_AGENT_CALL"] = "true"
    result = subprocess.run([
        "python",
        str(VALIDATE_TASK_SCRIPT),
        f"--files-to-check={files}"
    ], capture_output=True, text=True, env=env)
    status = "completed" if result.returncode == 0 else "failed"
    return {
        "task_type": "validate_files",
        "status": status,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }

def main() -> None:
    global LAST_MTIME
    if not NEW_TASK_FILE.exists():
        return

    mtime = os.stat(NEW_TASK_FILE).st_mtime_ns
    if LAST_MTIME is None:
        LAST_MTIME = mtime
    return
    if mtime == LAST_MTIME:
        return
    LAST_MTIME = mtime

    tasks = load_tasks().get("tasks", [])
    results = []
    run_parser = False
    for task in tasks:
        ttype = task.get("task_type")
        if ttype == "validate_files":
            results.append(execute_validate_files_task(task))
            run_parser = True
        elif ttype == "generate_documentation":
            proc = subprocess.run([
                "python",
                GENERATE_CLI_DOCS
            ], capture_output=True, text=True)
            status = "completed" if proc.returncode == 0 else "failed"
            results.append({
                "task_type": "generate_documentation",
                "status": status,
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
            })
        else:
            results.append({"task_type": ttype, "status": "unknown"})
            run_parser = True

    save_output({"results": results})
    archive_logs()
    if run_parser:
        subprocess.run(["python", TASK_LOG_PARSER], capture_output=True, text=True)

if __name__ == "__main__":
    main()
