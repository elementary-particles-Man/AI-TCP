import os
import time
import shutil
from datetime import datetime
import subprocess
from pathlib import Path

# === 設定 ===
NEW_TASK_JSON = Path(r"D:\My Data\Develop\Project INFINITY\AI-TCP\cli_instructions\new_task.json")
LOG_FILE = Path(r"D:\My Data\Develop\Project INFINITY\AI-TCP\cli_logs\TaskValidation.txt")
ARCHIVE_DIR = Path(r"D:\My Data\Develop\Project INFINITY\AI-TCP\cli_archives")
FLAG_FILE = NEW_TASK_JSON.with_suffix(".flag")

PROMPT_TEMPLATE = (
    "new_task.json（フルパス: {json_path}）を確認し、"
    "内容に従ってタスクを完了して下さい。\n"
    "作業ログは \"{log_path}\" に記載して下さい。\n"
    "全てのタスクが完了したら、必ずログファイルの末尾に [Task Completed] を追記して下さい。\n"
)

# === ディレクトリ準備 ===
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

print(f"[INFO] Watching task file: {NEW_TASK_JSON.resolve()}")
print(f"[INFO] Log will be written to: {LOG_FILE.resolve()}")
print(f"[INFO] Archive directory: {ARCHIVE_DIR.resolve()}")

# === 常駐ループ ===
while True:
    if NEW_TASK_JSON.exists():
        print("[INFO] new_task.json を検知しました。Gemini CUI を起動します。")

        # 既存ログをアーカイブ or 削除
        if LOG_FILE.exists():
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.move(LOG_FILE, ARCHIVE_DIR / f"TaskValidation_{ts}.txt")
            print(f"[INFO] 古いログをアーカイブしました: TaskValidation_{ts}.txt")

        # Gemini CUI を起動（プロンプトを標準入力で渡す、-y 付与）
        prompt = PROMPT_TEMPLATE.format(
            json_path=NEW_TASK_JSON.resolve(),
            log_path=LOG_FILE.resolve(),
        )
        subprocess.run([
            "gemini-cui",
            "-y",
        ], input=prompt.encode("utf-8"), check=False)

        print("[INFO] Gemini CUI 実行中... ログファイルの完了を監視します。")

        # 完了検知: [Task Completed] または .flag ファイルを監視
        while True:
            completed = False
            if LOG_FILE.exists():
                try:
                    with LOG_FILE.open(encoding="utf-8") as f:
                        for line in reversed(f.readlines()):
                            if "[Task Completed]" in line:
                                completed = True
                                break
                except Exception:
                    pass

            if not completed and FLAG_FILE.exists():
                completed = True

            if completed:
                print("[INFO] タスク完了を検知しました。")

                ts = datetime.now().strftime("%Y%m%d_%H%M%S")

                # new_task.json をアーカイブ
                shutil.move(NEW_TASK_JSON, ARCHIVE_DIR / f"new_task_{ts}.json")
                print(f"[INFO] new_task.json をアーカイブしました: new_task_{ts}.json")

                # ログファイルをアーカイブ
                if LOG_FILE.exists():
                    shutil.move(LOG_FILE, ARCHIVE_DIR / f"TaskValidation_{ts}.txt")
                    print(f"[INFO] ログファイルをアーカイブしました: TaskValidation_{ts}.txt")

                if FLAG_FILE.exists():
                    FLAG_FILE.unlink()

                break

            time.sleep(5)

    else:
        print(".")
        time.sleep(90)
