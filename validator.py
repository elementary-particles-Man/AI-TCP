import os

ALLOWED_BASE_PATH = os.path.abspath("D:/MyData/AI-TCP-Repo/")

def validate_git_commit_task(task: dict) -> None:
    if "execution_target" not in task:
        raise ValueError("Missing 'execution_target' in task.")
    if "task_payload" not in task:
        raise ValueError("Missing 'task_payload' in task.")

    target = task["execution_target"]
    payload = task["task_payload"]

    if "path" not in target or not isinstance(target["path"], str):
        raise ValueError("'execution_target.path' must be a string.")

    repo_path_abs = os.path.abspath(target["path"])
    if not repo_path_abs.startswith(ALLOWED_BASE_PATH):
        raise ValueError(
            f"Security Error: Path '{target['path']}' is outside the allowed sandbox directory ('{ALLOWED_BASE_PATH}')."
        )

    if "files" not in payload or not isinstance(payload["files"], list) or not payload["files"]:
        raise ValueError("'task_payload.files' must be a non-empty list.")

    if "commit_message" in payload and not isinstance(payload["commit_message"], str):
        raise ValueError("'task_payload.commit_message' must be a string if provided.")


def main_validator(task: dict) -> None:
    task_type = task.get("task_type")
    if not task_type:
        raise ValueError("Missing 'task_type' in task.")
    if task_type == "git_commit":
        validate_git_commit_task(task)
    else:
        raise ValueError(f"Unsupported task_type: {task_type}")
