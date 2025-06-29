import json
import subprocess
from pathlib import Path
from datetime import datetime
import os

REPO_ROOT = Path(__file__).resolve().parents[2]
NEW_TASK_FILE = REPO_ROOT / "new_task.json"


def _normalize_path(raw: str) -> Path:
    """Convert windows-style path under the AI-TCP repo to a local Path."""
    lower = raw.lower()
    idx = lower.find("ai-tcp")
    if idx != -1:
        rel = raw[idx + len("ai-tcp"):].lstrip("/\\")
        return REPO_ROOT / rel.replace("\\", "/")
    return Path(raw)


def run_validate_files(task: dict) -> None:
    exec_target = task.get("execution_target", {})
    payload = task.get("task_payload", {})
    command = exec_target.get("command", "")
    log_path = _normalize_path(payload.get("log_path", "logs/TaskValidation.txt"))
    pytest_target = _normalize_path(payload.get("pytest_target", "tests/test_validator_git_commit.py"))

    parts = command.split()
    if len(parts) < 3:
        raise ValueError("Invalid command for validate_files")

    files_str = parts[2]
    files = [_normalize_path(p.strip()) for p in files_str.split(',') if p.strip()]

    log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(msg: str) -> None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")

    log("=== ファイル存在チェック ===")
    all_ok = True
    for fp in files:
        if fp.exists():
            size = fp.stat().st_size
            log(f"[OK] {fp} (Size: {size} bytes)")
        else:
            log(f"[NG] {fp} (NOT FOUND)")
            all_ok = False

    log("\n=== pytest 実行 ===")
    cmd = ["pytest", str(pytest_target), f"--files-to-check={';'.join(map(str, files))}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    log(result.stdout)
    log(f"Pytest Exit Code: {result.returncode}")
    log("=== Validation Completed ===")
    log("[Task Completed]")


def main() -> None:
    if not NEW_TASK_FILE.exists():
        print("new_task.json not found")
        return
    with NEW_TASK_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    task_type = data.get("task_type")
    if task_type == "validate_files":
        run_validate_files(data)
    else:
        print(f"Unsupported task_type: {task_type}")


if __name__ == "__main__":
    main()
