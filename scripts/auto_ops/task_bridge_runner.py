import os
import time
import shutil
from datetime import datetime
import subprocess

# === 環境変数からリポジトリルートを取得（ジャンクション経由で空白なし） ===
REPO_ROOT = os.environ.get("REPO_ROOT")
if not REPO_ROOT:
    raise EnvironmentError("REPO_ROOT 環境変数が設定されていません。")
print(f"[INFO] リポジトリルート: {REPO_ROOT}")

# === Get-Command gemini ===
try:
    result = subprocess.run(
        ["powershell", "-Command", "Get-Command gemini | Select-Object -ExpandProperty Source"],
        capture_output=True,
        text=True,
        check=True
    )
    CLI_PATH = result.stdout.strip()
    if not CLI_PATH:
        raise FileNotFoundError("gemini コマンドが見つかりません。")
except subprocess.CalledProcessError as e:
    raise RuntimeError(f"Get-Command gemini 実行に失敗: {e}")

print(f"[INFO] CLI_PATH: {CLI_PATH}")

# === カレントディレクトリ固定 ===
os.chdir(REPO_ROOT)

# === パス設定（相対） ===
NEW_TASK_JSON = ".\\cli_instruction\\new_task.json"
LOG_FILE = ".\\cli_logs\\TaskValidation.txt"
ARCHIVE_DIR = ".\\cli_archives"

# === プロンプト ===
PROMPT = (
    f"new_task.json（パス: {NEW_TASK_JSON}）を確認し、"
    "内容に従ってタスクを完了して下さい。\n"
    f"作業ログは \"{LOG_FILE}\" に記載して下さい。\n"
    "全てのタスクが完了したら、必ずログファイルの末尾に [Task Completed] を追記して下さい。\n"
)

# === ディレクトリ準備 ===
if not os.path.exists(ARCHIVE_DIR):
    os.makedirs(ARCHIVE_DIR)

# === 常駐ループ ===
try:
    while True:
        if os.path.exists(NEW_TASK_JSON):
            print("[INFO] new_task.json を検知しました。Gemini CUI を起動します。")

            # 既存ログアーカイブ
            if os.path.exists(LOG_FILE):
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_path = os.path.join(ARCHIVE_DIR, f"TaskValidation_{ts}.txt")
                try_count = 0
                while try_count < 5:
                    try:
                        shutil.copy(LOG_FILE, archive_path)
                        os.remove(LOG_FILE)
                        print(f"[INFO] 古いログをアーカイブしました: {archive_path}")
                        break
                    except PermissionError as e:
                        try_count += 1
                        print(f"[WARN] {e} リトライ: {try_count}/5")
                        time.sleep(3)

            # Gemini CLI 実行
            subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", CLI_PATH, "-y"],
                input=PROMPT.encode("utf-8"),
                check=False
            )

            print("[INFO] Gemini CUI 実行中... ログの完了を監視します。")

            while True:
                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, encoding="utf-8") as f:
                        if "[Task Completed]" in f.read():
                            print("[INFO] タスク完了検知。")

                            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                            shutil.move(NEW_TASK_JSON, os.path.join(ARCHIVE_DIR, f"new_task_{ts}.json"))
                            print(f"[INFO] new_task.json をアーカイブしました。")

                            archive_path = os.path.join(ARCHIVE_DIR, f"TaskValidation_{ts}.txt")
                            try_count = 0
                            while try_count < 5:
                                try:
                                    shutil.copy(LOG_FILE, archive_path)
                                    os.remove(LOG_FILE)
                                    print(f"[INFO] ログをアーカイブしました: {archive_path}")
                                    break
                                except PermissionError as e:
                                    try_count += 1
                                    print(f"[WARN] {e} リトライ: {try_count}/5")
                                    time.sleep(3)
                            break
                time.sleep(5)
        else:
            print(".")
            time.sleep(90)
except KeyboardInterrupt:
    print("\n[INFO] ユーザーが停止しました。")

