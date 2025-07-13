import time
from pathlib import Path
import os

# This comment is added for Git commit verification. (3rd time)

repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd()))
OUTPUT_LOG = repo_root / "cli_logs" / "output.json"

print(f"✅ Watching output.json: {OUTPUT_LOG}")

while True:
    if OUTPUT_LOG.exists():
        print(f"✅ Detected: {OUTPUT_LOG}")
        with open(OUTPUT_LOG, 'r') as f:
            content = f.read()
            print("----- OUTPUT START -----")
            print(content)
            print("----- OUTPUT END -----")
        OUTPUT_LOG.unlink()
        print("✅ output.json deleted.")
    time.sleep(3)
