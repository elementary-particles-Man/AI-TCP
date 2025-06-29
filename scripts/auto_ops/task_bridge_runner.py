import os
import time
import shutil
from datetime import datetime
import subprocess
from pathlib import Path

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
NEW_TASK_JSON = Path("cli_instruction") / "new_task.json"
COMPLETE_FLAG = Path("cli_instruction") / "complete.flag"
ARCHIVE_DIR = Path("cli_archives")
ARCHIVE_LOG = ARCHIVE_DIR / "archive_log.txt"

# === ディレクトリ準備 ===
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

# === 常駐ループ ===
try:
    while True:
        if NEW_TASK_JSON.exists():
            print("[INFO] new_task.json を検知しました。Gemini CUI を起動します。")

            if COMPLETE_FLAG.exists():
                COMPLETE_FLAG.unlink()
                print(f"[INFO] 古い complete.flag を削除しました: {COMPLETE_FLAG}")

            # === JSON をそのまま読み込む ===
            with NEW_TASK_JSON.open('r', encoding='utf-8') as f:
                json_content = f.read()
            print("[INFO] new_task.json をそのまま Gemini CLI に渡します。")

            subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", CLI_PATH, "-y"],
                input=json_content.encode("utf-8"),
                check=False
            )

            print("[INFO] Gemini CUI 実行中... complete.flag の完了を監視します。")

            while True:
                if COMPLETE_FLAG.exists():
                    print("[INFO] complete.flag を検知しました。")

                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

                    dest_json = ARCHIVE_DIR / f"new_task_{ts}.json"
                    dest_flag = ARCHIVE_DIR / f"complete_{ts}.flag"

                    preview_json = json_content[:200]
                    flag_preview = COMPLETE_FLAG.read_text(encoding='utf-8', errors='ignore')[:200]

                    shutil.move(str(NEW_TASK_JSON), dest_json)
                    print(f"[INFO] new_task.json をアーカイブしました: {dest_json.name}")

                    try:
                        shutil.move(str(COMPLETE_FLAG), dest_flag)
                    except Exception as e:
                        raise RuntimeError(f"Failed to move {COMPLETE_FLAG}") from e
                    print(f"[INFO] complete.flag をアーカイブしました: {dest_flag.name}")

                    with ARCHIVE_LOG.open('a', encoding='utf-8') as log:
                        log.write(f"[{ts}] Archived {dest_json.name}\n")
                        log.write(preview_json + "\n")
                        log.write(f"[{ts}] Archived {dest_flag.name}\n")
                        if flag_preview:
                            log.write(flag_preview + "\n")

                    break

                time.sleep(5)

        else:
            print(".")
            time.sleep(90)

except KeyboardInterrupt:
    print("\n[INFO] ユーザーによって停止されました。")
