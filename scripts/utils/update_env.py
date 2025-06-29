# scripts/utils/update_env.py
import os
from pathlib import Path


def main() -> None:
    repo_root = os.environ.get("REPO_ROOT")
    if not repo_root:
        print("REPO_ROOT environment variable not set")
        return
    os.chdir(repo_root)

    env_path = Path(".env")
    if env_path.exists():
        current = env_path.read_text(encoding="utf-8")
        line = next((l for l in current.splitlines() if l.startswith("REPO_ROOT")), "")
        if line:
            print(f"Current {line}")
        ans = input("Overwrite .env? (y/n): ")
        if ans.lower() != "y":
            print("Abort")
            return

    env_path.write_text(f"REPO_ROOT={repo_root}\n", encoding="utf-8")
    print(f"Updated {env_path}")


if __name__ == "__main__":
    main()
