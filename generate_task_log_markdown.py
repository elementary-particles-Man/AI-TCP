import os
import shutil
from datetime import datetime
from pathlib import Path

def generate_task_log_markdown(source_path, destination_dir):
    if not os.path.exists(source_path):
        print(f"Error: Source file not found at {source_path}")
        return

    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    markdown_content = "# Task Validation Log\n\n" + content.replace("\n", "\n\n")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"TaskValidation_{timestamp}.md"
    output_path = os.path.join(destination_dir, output_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"Formatted log saved to {output_path}")

    # Move the original file to cli_archives
    shutil.move(source_path, os.path.join(destination_dir, os.path.basename(source_path)))
    print(f"Original log moved to {destination_dir}")

if __name__ == "__main__":
    repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd()))
    source_log_path = repo_root / "logs" / "TaskValidation.txt"
    archive_dir = repo_root / "cli_archives"
    generate_task_log_markdown(str(source_log_path), str(archive_dir))
