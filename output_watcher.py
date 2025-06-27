# --- output_watcher.py ---
import time
import json
import shutil
from pathlib import Path
from datetime import datetime

# === 設定 ===
OUTPUT_PATH = Path("F:/マイドライブ/AI-TCP_Task/cli_logs/output.json")
INSTRUCTION_PATH = Path("F:/マイドライブ/AI-TCP_Task/cli_instructions/new_task.json")
ARCHIVE_DIR = Path("F:/マイドライブ/AI-TCP_Task/cli_archives/")

# === メインループ ===
print(f"✅ Watching: {OUTPUT_PATH}")

while True:
    if OUTPUT_PATH.exists():
        print(f"\n{datetime.now()}: Detected output.json")

        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            result = json.load(f)

        if result.get("execution_status") == "success":
            # 必要に応じて PRタスク用の new_task.json を組み立て
            task_json = {
                "task_type": "git_commit",
                "execution_target": {
                    "path": "F:/マイドライブ/AI-TCP_Task",
                    "branch": "main",
                    "commit_message": f"[AI-TCP] Auto-PR {datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "files": result.get("details", {}).get("added_files", [])
                }
            }

            # Codex用に cli_instructions に投入
            with open(INSTRUCTION_PATH, "w", encoding="utf-8") as f:
                json.dump(task_json, f, indent=2, ensure_ascii=False)
            print(f"✅ new_task.json created for Codex: {INSTRUCTION_PATH}")

        else:
            print("⚠️  output.json indicates error or unexpected result. Skipping Codex PR creation.")

        # output.json をアーカイブ
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = f"{timestamp}_output.json"
        shutil.move(str(OUTPUT_PATH), str(ARCHIVE_DIR / archive_name))
        print(f"✅ Archived output.json as: {archive_name}")

    else:
        print(".", end="", flush=True)

    time.sleep(5)
