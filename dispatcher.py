import subprocess
import os
from datetime import datetime

def execute_git_commit(task: dict) -> dict:
    try:
        target = task.get("execution_target", {})
        payload = task.get("task_payload", {})

        repo_path = target.get("path")
        if not repo_path or not os.path.isdir(repo_path):
            raise FileNotFoundError(f"Invalid repository path: {repo_path}")

        commit_msg = payload.get("commit_message", "Auto-commit by AI-TCP Agent")
        files_to_add = payload.get("files", [])

        if not files_to_add:
            raise ValueError("'files' array in task_payload is empty or missing.")

        subprocess.run(["git", "add"] + files_to_add, cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_path, check=True)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        pr_name = f"{timestamp}_semantic.md"

        return {
            "execution_status": "success",
            "message": f"Committed {len(files_to_add)} file(s).",
            "details": {
                "task_type": "execute_git_commit",
                "commit_hash": "dummy_hash_for_now",
                "added_files": files_to_add,
                "pr_name": pr_name
            }
        }

    except subprocess.CalledProcessError as e:
        return {
            "execution_status": "error",
            "message": f"Git command failed: {str(e)}",
            "details": {}
        }

    except Exception as e:
        return {
            "execution_status": "error",
            "message": f"Unexpected error: {str(e)}",
            "details": {}
        }


def dispatch_task(task: dict) -> dict:
    task_type = task.get("task_type")
    if task_type == "git_commit":
        return execute_git_commit(task)
    else:
        return {
            "execution_status": "error",
            "message": f"Unsupported task_type: {task_type}",
            "details": {}
        }
