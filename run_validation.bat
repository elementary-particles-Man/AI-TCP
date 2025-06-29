@echo off
set "VALIDATE_SCRIPT=D:\My Data\Develop\Project INFINITY\AI-TCP\validate_yaml.py"
set "INPUT_FILE=D:\My Data\Develop\Project INFINITY\AI-TCP\cli_instruction\new_task.json"
set "OUTPUT_FILE=D:\My Data\Develop\Project INFINITY\AI-TCP\cli_logs\TaskValidation.txt"

python "%VALIDATE_SCRIPT%" "%INPUT_FILE%" > "%OUTPUT_FILE%" 2>&1
echo.>>"%OUTPUT_FILE%"
echo [Task Completed]>>"%OUTPUT_FILE%"

