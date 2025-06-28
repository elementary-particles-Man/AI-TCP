# ----------------------------------------------------------------
# start_all_watchers.ps1
# AI-TCP 自動運用：全ウォッチャーを並列で非同期起動するランチャー
# パス統一版（scripts/auto_ops/ に集約）
# ----------------------------------------------------------------

# === 設定 ===
$baseDir = "D:\My Data\Develop\Project INFINITY\AI-TCP\scripts\auto_ops"

Write-Host "✅ AI-TCP: 全ウォッチャー起動開始 ------------------------------------------------"

# === Python: task_bridge_runner.py ===
Start-Process -WindowStyle Minimized -FilePath "python.exe" -ArgumentList "$baseDir\task_bridge_runner.py"
Write-Host "✅ Python : task_bridge_runner.py started."

# === Python: output_watcher.py ===
Start-Process -WindowStyle Minimized -FilePath "python.exe" -ArgumentList "$baseDir\output_watcher.py"
Write-Host "✅ Python : output_watcher.py started."

# === PowerShell: watch_and_execute.ps1 ===
Start-Process -WindowStyle Minimized -FilePath "powershell.exe" -ArgumentList "-ExecutionPolicy Bypass -File `"$baseDir\watch_and_execute.ps1`""
Write-Host "✅ PowerShell : watch_and_execute.ps1 started."

# === PowerShell: task_bridge_runner.ps1 (Gemini CLI 用) ===
Start-Process -WindowStyle Minimized -FilePath "powershell.exe" -ArgumentList "-ExecutionPolicy Bypass -File `"$baseDir\task_bridge_runner.ps1`""
Write-Host "✅ PowerShell : task_bridge_runner.ps1 (Gemini CLI) started."

Write-Host "--------------------------------------------------------"
Write-Host "✅ 全ウォッチャーがバックグラウンドで起動しました。"
Write-Host "   必要に応じてタスクマネージャーで確認して下さい。"
Write-Host "--------------------------------------------------------"
