# Python系スクリプトを /pytools に整理
if (-Not (Test-Path "./pytools")) {
    New-Item -ItemType Directory -Path "./pytools"
}
Get-ChildItem -Path "./tools" -Filter "*.py" | ForEach-Object {
    Move-Item $_.FullName -Destination "./pytools/$($_.Name)"
}

# tools ディレクトリが空なら削除（必要であれば）
if ((Get-ChildItem -Path "./tools").Count -eq 0) {
    Remove-Item -Path "./tools" -Recurse -Force
}

Write-Output "✅ Python: ./tools/*.py → ./pytools/ に整理完了"
Write-Output "✅ Go: AI-TCP_Structure/tools/ にて運用継続"
