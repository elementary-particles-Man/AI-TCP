import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

def archive_cli_files(cli_archives_dir, old_dir, days_threshold=7):
    if not os.path.exists(cli_archives_dir):
        print(f"Error: CLI archives directory not found at {cli_archives_dir}")
        return

    if not os.path.exists(old_dir):
        os.makedirs(old_dir)
        print(f"Created old archives directory: {old_dir}")

    now = datetime.now()

    for filename in os.listdir(cli_archives_dir):
        file_path = os.path.join(cli_archives_dir, filename)
        if os.path.isfile(file_path):
            try:
                # Get modification time of the file
                mod_timestamp = os.path.getmtime(file_path)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)

                # If file is older than the threshold, move it to 'old' directory
                if (now - mod_datetime).days > days_threshold:
                    shutil.move(file_path, os.path.join(old_dir, filename))
                    print(f"Archived old file: {filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

if __name__ == "__main__":
    repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd()))
    cli_archives_path = repo_root / "cli_archives"
    old_archives_path = cli_archives_path / "old"
    archive_cli_files(str(cli_archives_path), str(old_archives_path), days_threshold=0)
