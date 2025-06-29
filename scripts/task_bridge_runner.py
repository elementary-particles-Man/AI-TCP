import os
import json
import time
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# === 必須環境変数 ===
REPO_ROOT = os.environ.get("REPO_ROOT")
if not REPO_ROOT:
    raise EnvironmentError("REPO_ROOT 環境変数が設定されていません。")

# === パス設定 ===
NEW_TASK_FILE = Path(REPO_ROOT) / "AI-TCP_Structure/task_bridge/cli_instructions/new_task.json"
OUTPUT_FILE = Path(REPO_ROOT) / "cli_logs/output.json"
TASK_VALIDATION_LOG = Path(REPO_ROOT) / "logs/TaskValidation.txt"
CLI_ARCHIVES_DIR = Path(REPO_ROOT) / "cli_archives"

TASK_LOG_PARSER = Path(REPO_ROOT) / "pytools/task_log_parser.py"
GENERATE_CLI_DOCS = Path(REPO_ROOT) / "pytools/generate_cli_docs.py"
VALIDATE_TASK_SCRIPT = Path(REPO_ROOT) / "scripts/auto_ops/validate_task.py"

# === タスクロード ===
def load_tasks():
    if not NEW_TASK_FILE.exists():
        return {"tasks": []}
    with NEW_TASK_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

# === 出力保存 ===
def save_output(data):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# === ログアーカイブ ===
def archive_logs():
    CLI_ARCHIVES_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    if TASK_VALIDATION_LOG.exists():
        shutil.move(TASK_VALIDATION_LOG, CLI_ARCHIVES_DIR / f"TaskValidation_{ts}.txt")
    if OUTPUT_FILE.exists():
        shutil.move(OUTPUT_FILE, CLI_ARCHIVES_DIR / f"output_{ts}.json")

# === validate_files タスク ===
def execute_validate_files_task(task):
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
        "timestamp": datetime.now().isoformat()
    }

# === メイン監視ループ ===
def main():
    print(f"[INFO] Monitoring: {NEW_TASK_FILE}")
    last_mtime = None
    while True:
        current_mtime = NEW_TASK_FILE.stat().st_mtime if NEW_TASK_FILE.exists() else None
        if current_mtime and current_mtime != last_mtime:
            print("[INFO] Detected new task. Executing...")
            last_mtime = current_mtime

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
                        str(GENERATE_CLI_DOCS)
                    ], capture_output=True, text=True)
                    status = "completed" if proc.returncode == 0 else "failed"
                    results.append({
                        "task_type": "generate_documentation",
                        "status": status,
                        "returncode": proc.returncode,
                        "stdout": proc.stdout,
                        "stderr": proc.stderr,
                        "timestamp": datetime.now().isoformat()
                    })
                    run_parser = True
                else:
                    results.append({
                        "task_type": ttype,
                        "status": "unknown",
                        "timestamp": datetime.now().isoformat()
                    })

            save_output({"results": results})

            if run_parser:
                subprocess.run(["python", str(TASK_LOG_PARSER)], capture_output=True, text=True)

            archive_logs()
            print("[INFO] Task processing completed and logs archived.")

        time.sleep(5)

if __name__ == "__main__":
    main()
