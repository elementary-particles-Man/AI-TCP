# scripts/utils/update_env.py
import os
from pathlib import Path
from shutil import copy2


def main() -> None:
    repo_root = os.environ.get("REPO_ROOT")
    if not repo_root:
        print("REPO_ROOT environment variable not set")
        return
    os.chdir(repo_root)

    env_path = Path(".env")
    backup_path = env_path.with_suffix(env_path.suffix + ".bak")

    if env_path.exists():
        current = env_path.read_text(encoding="utf-8")
        line = next((l for l in current.splitlines() if l.startswith("REPO_ROOT=")), "")
        if line:
            print(f"Current {line}")
        ans = input("Update REPO_ROOT in .env? (y/n): ")
        if ans.lower() != "y":
            print("Abort")
            return
        copy2(env_path, backup_path)
        print(f"Backup created at {backup_path}")

    env_path.write_text(f"REPO_ROOT={repo_root}\n", encoding="utf-8")
    print(".env updated successfully.")


if __name__ == "__main__":
    main()
