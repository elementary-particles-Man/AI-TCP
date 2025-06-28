 
# ================================
# validate_task.ps1
# ================================
# AI-TCP タスク検証と構造検証をワンコマンドで実行
# ================================

# ログファイル
$logPath = "X:\work\TaskValidation.txt"

# 開始メッセージ
"=== ✅ タスク検証開始 ===" | Out-File -FilePath $logPath -Encoding UTF8

# pytest 実行
"=== ⚡ pytest 実行 ===" | Out-File -Append -FilePath $logPath
pytest tests/test_validator_git_commit.py | Out-File -Append -FilePath $logPath

# check_repo.py 実行
"=== 📂 リポジトリ構造チェック ===" | Out-File -Append -FilePath $logPath
python scripts/auto_ops/check_repo.py | Out-File -Append -FilePath $logPath

# 完了メッセージ
"=== ✅ タスク検証終了 ===" | Out-File -Append -FilePath $logPath

Write-Host "✅ 全ての検証結果が $logPath に保存されました。"
