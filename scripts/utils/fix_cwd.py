# scripts/utils/fix_cwd.py
import os
import sys


def main():
    repo_root = os.environ.get("REPO_ROOT")
    if not repo_root:
        print("REPO_ROOT environment variable not set")
        sys.exit(1)
    if not os.path.exists(repo_root):
        print("REPO_ROOT path does not exist")
        sys.exit(1)
    os.chdir(repo_root)
    print("Current directory:", os.getcwd())


if __name__ == "__main__":
    main()
