import os
import time
import shutil
from datetime import datetime
import subprocess

# === 設定 ===
NEW_TASK_JSON = r"D:\My Data\Develop\Project INFINITY\AI-TCP\cli_instructions\new_task.json"
LOG_FILE = r"D:\My Data\Develop\Project INFINITY\AI-TCP\cli_logs\TaskValidation.txt"
ARCHIVE_DIR = r"D:\My Data\Develop\Project INFINITY\AI-TCP\cli_archives"

PROMPT = (
    "new_task.json（フルパス: D:\\My Data\\Develop\\Project INFINITY\\AI-TCP\\cli_instructions\\new_task.json）を確認し、"
    "内容に従ってタスクを完了して下さい。\n"
    "作業ログは \"D:\\My Data\\Develop\\Project INFINITY\\AI-TCP\\cli_logs\\TaskValidation.txt\" に記載して下さい。\n"
    "全てのタスクが完了したら、必ずログファイルの末尾に [Task Completed] を追記して下さい。\n"
)

# === ディレクトリ準備 ===
if not os.path.exists(ARCHIVE_DIR):
    os.makedirs(ARCHIVE_DIR)

# === 常駐ループ ===
while True:
    if os.path.exists(NEW_TASK_JSON):
        print("[INFO] new_task.json を検知しました。Gemini CUI を起動します。")

        # 既存ログをアーカイブ or 削除
        if os.path.exists(LOG_FILE):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.move(LOG_FILE, os.path.join(ARCHIVE_DIR, f"TaskValidation_{ts}.txt"))
            print(f"[INFO] 古いログをアーカイブしました: TaskValidation_{ts}.txt")

        # Gemini CUI を起動（プロンプトを標準入力で渡す、-y 付与）
        subprocess.run(
            ["gemini-cui", "-y"],
            input=PROMPT.encode("utf-8"),
            check=False
        )

        print("[INFO] Gemini CUI 実行中... ログファイルの完了を監視します。")

        # 完了検知: [Task Completed] が書かれるまで監視
        while True:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, encoding="utf-8") as f:
                    if "[Task Completed]" in f.read():
                        print("[INFO] タスク完了を検知しました。")

                        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

                        # new_task.json をアーカイブ
                        shutil.move(NEW_TASK_JSON, os.path.join(ARCHIVE_DIR, f"new_task_{ts}.json"))
                        print(f"[INFO] new_task.json をアーカイブしました: new_task_{ts}.json")

                        # ログファイルをアーカイブ
                        shutil.move(LOG_FILE, os.path.join(ARCHIVE_DIR, f"TaskValidation_{ts}.txt"))
                        print(f"[INFO] ログファイルをアーカイブしました: TaskValidation_{ts}.txt")

                        break
            time.sleep(5)

    else:
        print(".")
        time.sleep(90)
