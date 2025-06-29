# scripts/utils/gen_settings.py
import os
import sys


def main():
    repo_root = os.environ.get("REPO_ROOT")
    if not repo_root:
        print("REPO_ROOT environment variable not set")
        sys.exit(1)
    os.chdir(repo_root)

    target = sys.argv[1] if len(sys.argv) > 1 else ".env"
    path = os.path.join(repo_root, target)
    if os.path.exists(path):
        ans = input(f"{path} exists. Overwrite? (y/n): ")
        if ans.lower() != 'y':
            print("Abort")
            return
    if target.endswith(('.yml', '.yaml')):
        content = f"REPO_ROOT: {repo_root}\n"
    else:
        content = f"REPO_ROOT={repo_root}\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Wrote", path)
    print(content)


if __name__ == "__main__":
    main()
