import os
import time
import shutil
from datetime import datetime
import subprocess

# === 環境変数からジャンクションパスを取得 ===
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

# === カレントディレクトリをジャンクションで固定 ===
os.chdir(REPO_ROOT)

# === パス設定 ===
NEW_TASK_JSON = ".\\cli_instruction\\new_task.json"
COMPLETE_FLAG = ".\\cli_instruction\\complete.flag"
ARCHIVE_DIR = ".\\cli_archives"

# === ディレクトリ準備 ===
if not os.path.exists(ARCHIVE_DIR):
    os.makedirs(ARCHIVE_DIR)

# === 常駐ループ ===
try:
    while True:
        if os.path.exists(NEW_TASK_JSON):
            print("[INFO] new_task.json を検知しました。Gemini CUI を起動します。")

            if os.path.exists(COMPLETE_FLAG):
                os.remove(COMPLETE_FLAG)
                print(f"[INFO] 古い complete.flag を削除しました: {COMPLETE_FLAG}")

            # === JSON をそのまま読み込む ===
            with open(NEW_TASK_JSON, 'r', encoding='utf-8') as f:
                json_content = f.read()
            print("[INFO] new_task.json をそのまま Gemini CLI に渡します。")

            subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", CLI_PATH, "-y"],
                input=json_content.encode("utf-8"),
                check=False
            )

            print("[INFO] Gemini CUI 実行中... complete.flag の完了を監視します。")

            while True:
                if os.path.exists(COMPLETE_FLAG):
                    print("[INFO] complete.flag を検知しました。")

                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

                    shutil.move(NEW_TASK_JSON, os.path.join(ARCHIVE_DIR, f"new_task_{ts}.json"))
                    print(f"[INFO] new_task.json をアーカイブしました: new_task_{ts}.json")

                    shutil.move(COMPLETE_FLAG, os.path.join(ARCHIVE_DIR, f"complete_{ts}.flag"))
                    print(f"[INFO] complete.flag をアーカイブしました: complete_{ts}.flag")

                    break

                time.sleep(5)

        else:
            print(".")
            time.sleep(90)

except KeyboardInterrupt:
    print("\n[INFO] ユーザーによって停止されました。")
