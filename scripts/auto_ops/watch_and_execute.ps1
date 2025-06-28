# ----------------------------------------------------------------
# watch_and_execute.ps1 (PowerShell移植版)
# AI-TCP 自動運用用
# 1. new_task.json を監視
# 2. LM Studio にPOSTして output.json を生成
# 3. Task_archive にタイムスタンプ付きで保存
# ----------------------------------------------------------------

# This comment is added for Git commit verification.

# === 設定 ===
$instructionPath = "D:\My Data\Develop\Project INFINITY\AI-TCP\scripts\auto_ops\new_task.json"
$outputPath = "D:\My Data\Develop\Project INFINITY\AI-TCP\scripts\auto_ops\output.json"
$archiveDir = "D:\My Data\Develop\Project INFINITY\AI-TCP\scripts\auto_ops\Task_archive"

# === 無限ループ ===
while ($true) {
    if (Test-Path $instructionPath) {
        Write-Host "✅ new_task.json を検出、処理開始..."

        # curlでLM StudioにPOST
        $cmd = "curl -X POST http://localhost:1234/v1/chat/completions -H `"Content-Type: application/json`" -d @$instructionPath -o $outputPath"
        Invoke-Expression $cmd

        # アーカイブディレクトリが無ければ作成
        if (!(Test-Path $archiveDir)) {
            New-Item -ItemType Directory -Path $archiveDir | Out-Null
        }

        # タイムスタンプ付きでファイルを保存
        $timestamp = Get-Date -Format "yyyyMMddHHmmss"
        $archivePath = Join-Path $archiveDir "new_task_${timestamp}.json"

        Move-Item $instructionPath $archivePath -Force
        Write-Host "✅ Task completed: $timestamp"
    }

    Start-Sleep -Seconds 2
}
