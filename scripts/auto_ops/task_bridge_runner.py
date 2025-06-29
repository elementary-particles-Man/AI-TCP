import os
import time
import shutil
from datetime import datetime
import subprocess
import sys

# === Configuration for WinError32 Retries ===
MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 1

# === 環境変数からジャンクションパスを取得 ===
REPO_ROOT = os.environ.get("REPO_ROOT")
if not REPO_ROOT:
    raise EnvironmentError("REPO_ROOT 環境変数が設定されていません。")
print(f"[INFO] リポジトリルート: {REPO_ROOT}")

# === CLI_PATH Resolution ===
def resolve_cli_path():
    # 1. Check GEMINI_CLI_PATH environment variable
    gemini_cli_path_env = os.environ.get("GEMINI_CLI_PATH")
    if gemini_cli_path_env and os.path.exists(gemini_cli_path_env):
        print(f"[INFO] GEMINI_CLI_PATH 環境変数からCLIパスを解決しました: {gemini_cli_path_env}")
        return gemini_cli_path_env

    # 2. Search in common PATH directories
    path_env = os.environ.get("PATH", "").split(os.pathsep)
    for p in path_env:
        gemini_cmd_path = os.path.join(p, "gemini.cmd")
        gemini_exe_path = os.path.join(p, "gemini.exe")
        if os.path.exists(gemini_cmd_path):
            print(f"[INFO] PATHからCLIパスを解決しました: {gemini_cmd_path}")
            return gemini_cmd_path
        if os.path.exists(gemini_exe_path):
            print(f"[INFO] PATHからCLIパスを解決しました: {gemini_exe_path}")
            return gemini_exe_path

    # 3. Fallback to PowerShell Get-Command (Windows specific)
    if sys.platform == "win32":
        try:
            result = subprocess.run(
                ["powershell", "-Command", "Get-Command gemini | Select-Object -ExpandProperty Source"],
                capture_output=True,
                text=True,
                check=True
            )
            cli_path_ps = result.stdout.strip()
            if cli_path_ps:
                print(f"[INFO] PowerShell Get-CommandからCLIパスを解決しました: {cli_path_ps}")
                return cli_path_ps
        except subprocess.CalledProcessError as e:
            print(f"[WARNING] PowerShell Get-Command gemini 実行に失敗: {e}")
            pass # Continue to raise error if no path found

    raise FileNotFoundError("gemini CLI コマンドが見つかりません。GEMINI_CLI_PATH 環境変数を設定するか、PATHに追加してください。")

CLI_PATH = resolve_cli_path()
print(f"[INFO] CLI_PATH: {CLI_PATH}")

def robust_file_operation(func, *args, operation_name="操作", **kwargs):
    for i in range(MAX_RETRIES):
        try:
            func(*args, **kwargs)
            return True
        except OSError as e:
            print(f"[WARNING] {operation_name}失敗 (試行 {i+1}/{MAX_RETRIES}): {e}")
            time.sleep(RETRY_DELAY_SECONDS)
    print(f"[ERROR] {operation_name}が {MAX_RETRIES} 回試行しても失敗しました。")
    return False

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
            robust_file_operation(shutil.copy2, NEW_TASK_JSON, TMP_TASK_JSON, "複製")
            print(f"[INFO] new_task.json を tmp に複製しました: {TMP_TASK_JSON}")

            # === tmp を物理的に immutable にする ===
            subprocess.run(["attrib", "+R", TMP_TASK_JSON], check=False)
            print(f"[INFO] tmp ファイルを読み取り専用に設定しました: {TMP_TASK_JSON}")

            # 既存フラグが残っていたら削除
            if os.path.exists(COMPLETE_FLAG):
                robust_file_operation(os.remove, COMPLETE_FLAG, "削除")
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

                    robust_file_operation(shutil.move, NEW_TASK_JSON, os.path.join(ARCHIVE_DIR, f"new_task_{ts}.json"), "アーカイブ")
                    print(f"[INFO] new_task.json をアーカイブしました: new_task_{ts}.json")

                    robust_file_operation(shutil.move, COMPLETE_FLAG, os.path.join(ARCHIVE_DIR, f"complete_{ts}.flag"), "アーカイブ")
                    print(f"[INFO] complete.flag をアーカイブしました: complete_{ts}.flag")

                    if os.path.exists(TMP_TASK_JSON):
                        robust_file_operation(os.remove, TMP_TASK_JSON, "削除")
                        print(f"[INFO] tmp タスクを削除しました: {TMP_TASK_JSON}")

                    break

                time.sleep(5)

        else:
            print(".")
            time.sleep(90)

except KeyboardInterrupt:
    print("\n[INFO] ユーザーによって停止されました。")
