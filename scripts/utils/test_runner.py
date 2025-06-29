# scripts/utils/test_runner.py
import os
import subprocess
from datetime import datetime
from pathlib import Path


def main() -> None:
    repo_root = os.environ.get("REPO_ROOT")
    if not repo_root:
        print("REPO_ROOT environment variable not set")
        return
    os.chdir(repo_root)

    result = subprocess.run(["pytest", "-q"], capture_output=True, text=True)

    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "TaskValidation.txt"
    log_file.write_text(result.stdout + result.stderr, encoding="utf-8")
    print(f"Saved results to {log_file}")

    archive_dir = Path("cli_archives")
    archive_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = archive_dir / f"TaskValidation_{ts}.txt"
    archive_path.write_text(log_file.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Archived to {archive_path}")


if __name__ == "__main__":
    main()
