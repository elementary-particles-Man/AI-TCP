import subprocess
import datetime
import os
import sys

# Set stdout encoding to UTF-8 for proper display of emojis and special characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_git_command(args):
    """Gitコマンドを安全に実行して結果を返す"""
    result = subprocess.run(["git"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
    if result.returncode != 0:
        print(f"[ERROR] {' '.join(args)}\n{result.stderr}")
    return result.stdout.strip() if result.stdout else ""

def main():
    # タイムスタンプ付きログファイル名
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"repo_check_{timestamp}.txt")

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("=== 📂 リポジトリ ファイル構造 ===\n")
        ls_files = run_git_command(["ls-tree", "-r", "main"])
        f.write(ls_files + "\n\n")

        f.write("=== ✅ 最新コミット ===\n")
        last_commit = run_git_command(["log", "-1", "--pretty=format:%s%n%ci%n%an%n%H"])
        f.write(last_commit + "\n\n")

        f.write("=== 🔀 プルリクエスト一覧 ===\n")
        prs = run_git_command(["log", "--merges", "--pretty=format:%s"])
        if prs:
            for pr in prs.splitlines():
                f.write(f"- {pr}\n")
        else:
            f.write("(No merge commits found)\n")

    print(f"✅ リポジトリ検証ログを書き出しました: {log_file}")

if __name__ == "__main__":
    main()
