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
TMP_TASK_JSON = ".\\cli_instruction\\new_task.tmp.json"
COMPLETE_FLAG = ".\\cli_instruction\\complete.flag"
ARCHIVE_DIR = ".\\cli_archives"

# === PROMPT ===
PROMPT = (
    "新しいタスク指示書（./cli_instruction/new_task.tmp.json）を受け取りました。\n"
    "・内容を理解しただけでは完了と見なしません。\n"
    "・貴方を呼び出した意味は「タスクの完了」であり、終了フラグファイルを作る意味ではありません。。\n"
    "・内容を理解したら、必ず順に全てのタスクを即座に処理を開始して下さい。\n"
    "・各タスクが終わるごとに進行状況を必ず日本語で出力し、全タスクを処理して下さい。\n"
    "・全タスクが完了してから、必ず ./cli_instruction/complete.flag を生成して下さい。\n"
    "・`complete.flag` は `new_task.tmp.json` を rename して作ってはいけません。\n"
    "・必ず `type nul > ./cli_instruction/complete.flag` のように空の新規ファイルとして生成して下さい。\n"
    "・`mv` や `ren` コマンドは禁止です。\n"
    "・`complete.flag` は最後の最後に物理的に生成しない限り、タスク完了と認めません。\n"
    "・`new_task.json` は自動運用スクリプトが処理します。人間もGeminiも削除・変更してはいけません。\n"
    "・質問や応答は全て日本語で出力して下さい。\n"
)

# === ディレクトリ準備 ===
if not os.path.exists(ARCHIVE_DIR):
    os.makedirs(ARCHIVE_DIR)

# === 常駐ループ ===
try:
    while True:
        if os.path.exists(NEW_TASK_JSON):
            print("[INFO] new_task.json を検知しました。Gemini CUI を起動します。")

            # tmp 複製
            shutil.copy2(NEW_TASK_JSON, TMP_TASK_JSON)
            print(f"[INFO] new_task.json を tmp に複製しました: {TMP_TASK_JSON}")

            # === tmp を物理的に immutable にする ===
            subprocess.run(["attrib", "+R", TMP_TASK_JSON], check=False)
            print(f"[INFO] tmp ファイルを読み取り専用に設定しました: {TMP_TASK_JSON}")

            # 既存フラグが残っていたら削除
            if os.path.exists(COMPLETE_FLAG):
                os.remove(COMPLETE_FLAG)
                print(f"[INFO] 古い complete.flag を削除しました: {COMPLETE_FLAG}")

            # Gemini CLI 起動
            subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", CLI_PATH, "-y"],
                input=PROMPT.encode("utf-8"),
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

                    if os.path.exists(TMP_TASK_JSON):
                        os.remove(TMP_TASK_JSON)
                        print(f"[INFO] tmp タスクを削除しました: {TMP_TASK_JSON}")

                    break

                time.sleep(5)

        else:
            print(".")
            time.sleep(90)

except KeyboardInterrupt:
    print("\n[INFO] ユーザーによって停止されました。")
