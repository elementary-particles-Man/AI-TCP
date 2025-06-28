import os

ALLOWED_BASE_PATH = os.path.abspath("D:/My Data/Develop/Project INFINITY/AI-TCP")

def validate_git_commit_task(task: dict) -> None:
    if "execution_target" not in task:
        raise ValueError("Missing 'execution_target' in task.")
    payload = task["execution_target"]

    if "path" not in payload or not isinstance(payload["path"], str):
        raise ValueError("'execution_target.path' must be a string.")

    repo_path_abs = os.path.abspath(payload["path"])
    if not repo_path_abs.startswith(ALLOWED_BASE_PATH):
        raise ValueError(
            f"Security Error: Path '{repo_path_abs}' is outside the allowed sandbox directory ('{ALLOWED_BASE_PATH}')."
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
        raise ValueError(f"Unsupported task_type: '{task_type}'")
