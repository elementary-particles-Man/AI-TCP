# scripts/utils/cli_archive_checker.py
import os
from pathlib import Path


def main() -> None:
    repo_root = os.environ.get("REPO_ROOT")
    if not repo_root:
        print("REPO_ROOT environment variable not set")
        return
    os.chdir(repo_root)

    archive_dir = Path("cli_archives")
    archive_dir.mkdir(parents=True, exist_ok=True)

    print(f"Scanning {archive_dir} ...")
    files = [p for p in archive_dir.iterdir() if p.is_file()]
    complete = set()
    tasks = set()
    for f in files:
        name = f.name
        if name.startswith("complete_") and name.endswith(".flag"):
            ts = name[len("complete_"):-5]
            complete.add(ts)
            tasks.add(ts)
        elif name.startswith("new_task_") and name.endswith(".json"):
            ts = name[len("new_task_"):-5]
            tasks.add(ts)

    all_ok = True
    for ts in sorted(tasks):
        has_flag = ts in complete
        has_task = any(p.name == f"new_task_{ts}.json" for p in files)
        status = []
        if has_flag and has_task:
            status.append("OK")
        else:
            all_ok = False
            if not has_flag:
                status.append("missing complete.flag")
            if not has_task:
                status.append("missing new_task.json")
        print(f"{ts}: {', '.join(status)}")

    if all_ok:
        print("All flag/task pairs are present.")
    else:
        print("Some pairs are missing.")


if __name__ == "__main__":
    main()
