import re
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/logs/TaskValidation.txt")
OUTPUT_DIR = Path("D:/My Data/Develop/Project INFINITY/AI-TCP/vault_output")

def parse_task_validation_log(log_path):
    file_check_results = []
    pytest_output = []
    pytest_exit_code = None
    
    with log_path.open("r", encoding="utf-8") as f:
        content = f.read()

    # Parse file existence checks
    file_check_section_match = re.search(r"=== ファイル存在チェック ===\n(.*?)(?=\n=== pytest 実行 ===)", content, re.DOTALL)
    if file_check_section_match:
        for line in file_check_section_match.group(1).strip().split('\n'):
            if line.strip():
                file_check_results.append(line.strip())

    # Parse pytest output and exit code
    pytest_section_match = re.search(r"=== pytest 実行 ===\n(.*?)(?=\n=== Validation Completed ===)", content, re.DOTALL)
    if pytest_section_match:
        pytest_raw_output = pytest_section_match.group(1).strip()
        
        exit_code_match = re.search(r"Pytest Exit Code: (\d+)", pytest_raw_output)
        if exit_code_match:
            pytest_exit_code = int(exit_code_match.group(1))
            # Remove the exit code line from the pytest_output
            pytest_output = [line for line in pytest_raw_output.split('\n') if not line.startswith("Pytest Exit Code:")]
        else:
            pytest_output = pytest_raw_output.split('\n')

    return file_check_results, pytest_output, pytest_exit_code

def format_as_markdown(file_check_results, pytest_output, pytest_exit_code):
    markdown_output = "# Task Validation Report\n\n"
    markdown_output += f"**Generated At:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    markdown_output += "## File Existence Check\n"
    if file_check_results:
        for line in file_check_results:
            markdown_output += f"- {line}\n"
    else:
        markdown_output += "No file existence check results found.\n"
    markdown_output += "\n"

    markdown_output += "## Pytest Execution Results\n"
    if pytest_output:
        markdown_output += "```\n"
        markdown_output += "\n".join(pytest_output)
        markdown_output += "\n```\n"
    else:
        markdown_output += "No pytest output found.\n"
    markdown_output += "\n"

    if pytest_exit_code is not None:
        markdown_output += f"**Pytest Exit Code:** {pytest_exit_code}\n"
        if pytest_exit_code == 0:
            markdown_output += "**Status:** ✅ All tests passed.\n"
        else:
            markdown_output += "**Status:** ❌ Some tests failed or an error occurred.\n"
    else:
        markdown_output += "**Pytest Exit Code:** Not found.\n"

    return markdown_output

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file_path = OUTPUT_DIR / f"task_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    if not LOG_FILE.exists():
        print(f"Error: Log file not found at {LOG_FILE}")
        return

    file_check_results, pytest_output, pytest_exit_code = parse_task_validation_log(LOG_FILE)
    markdown_report = format_as_markdown(file_check_results, pytest_output, pytest_exit_code)

    with output_file_path.open("w", encoding="utf-8") as f:
        f.write(markdown_report)
    print(f"Task validation report generated at {output_file_path}")

if __name__ == "__main__":
    main()
