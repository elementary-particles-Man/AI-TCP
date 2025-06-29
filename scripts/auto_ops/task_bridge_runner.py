import os
import time
import shutil
from datetime import datetime
from pathlib import Path

SCRIPT_VERSION = "task_bridge_runner.py - Debug Last updated: 2025-06-30 02:55 JST"
print(f"=== {SCRIPT_VERSION} ===")

REPO_ROOT = os.environ.get("REPO_ROOT")
if not REPO_ROOT:
    raise EnvironmentError("REPO_ROOT 環境変数が設定されていません。")
print(f"[INFO] REPO_ROOT: {REPO_ROOT}")

# ✅ ディレクトリ名を単数形に合わせる
NEW_TASK_JSON = Path(REPO_ROOT) / "cli_instruction/new_task.json"
print(f"[INFO] NEW_TASK_JSON path: {NEW_TASK_JSON}")
print(f"[INFO] NEW_TASK_JSON exists?: {NEW_TASK_JSON.exists()}")

COMPLETE_FLAG = Path(REPO_ROOT) / "cli_instruction/complete.flag"
ARCHIVE_DIR = Path(REPO_ROOT) / "cli_archives"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

print(f"[INFO] 常駐監視開始...")

try:
    while True:
        if NEW_TASK_JSON.exists():
            print(f"[INFO] JSON検知: {NEW_TASK_JSON}")
            with NEW_TASK_JSON.open("r", encoding="utf-8") as f:
                content = f.read()
            print("===== JSON内容 =====")
            print(content)
            print("====================")
            print("[INFO] 完了フラグを監視します...")

            while not COMPLETE_FLAG.exists():
                time.sleep(3)

            print(f"[INFO] complete.flag を検知: {COMPLETE_FLAG}")
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")

            dest_json = ARCHIVE_DIR / f"new_task_{ts}.json"
            if NEW_TASK_JSON.exists():
                shutil.move(str(NEW_TASK_JSON), dest_json)
                print(f"[INFO] new_task.json をアーカイブ: {dest_json}")
            else:
                print("[WARN] new_task.json が存在しないためアーカイブをスキップしました")

            dest_flag = ARCHIVE_DIR / f"complete_{ts}.flag"
            shutil.move(str(COMPLETE_FLAG), dest_flag)
            print(f"[INFO] complete.flag をアーカイブ: {dest_flag}")

        else:
            print("[DEBUG] JSONファイルがまだ存在しません")
            time.sleep(3)

except KeyboardInterrupt:
    print("\n[INFO] ユーザー停止")
    print(f"=== {SCRIPT_VERSION} 終了 ===")
