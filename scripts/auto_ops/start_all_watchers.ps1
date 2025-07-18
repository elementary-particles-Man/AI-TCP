# ===============================================
# start_all_watchers.ps1
# AI-TCP タスクブリッジ自動運用: 全Watcherを並列起動
# ===============================================

Write-Host "============================="
Write-Host "  AI-TCP 自動運用 起動開始"
Write-Host "============================="

# 作業ディレクトリ
$baseDir = "D:\My Data\Develop\Project INFINITY\AI-TCP"
$scriptDir = "D:\My Data\Develop\Project INFINITY\AI-TCP\scripts\auto_ops"

# Python 環境の起動
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location `"$scriptDir`"; python task_bridge_runner.py" -WindowStyle Normal
Write-Host "✅ Python: task_bridge_runner.py を起動しました"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location `"$scriptDir`"; python output_watcher.py" -WindowStyle Normal
Write-Host "✅ Python: output_watcher.py を起動しました"

# PowerShell Gemini CLI版 (別Window)
Start-Process powershell -ArgumentList "-NoExit", "-File", "$scriptDir\task_bridge_runner.ps1" -WindowStyle Normal
Write-Host "✅ PowerShell: Gemini CLI版 task_bridge_runner.ps1 を起動しました"

Write-Host "============================="
Write-Host "  AI-TCP 自動運用 全Watcher起動完了"
Write-Host "============================="
