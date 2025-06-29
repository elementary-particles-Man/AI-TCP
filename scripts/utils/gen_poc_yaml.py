# scripts/utils/gen_poc_yaml.py
import os
from pathlib import Path
import yaml


def main() -> None:
    repo_root = os.environ.get("REPO_ROOT")
    if not repo_root:
        print("REPO_ROOT environment variable not set")
        return
    os.chdir(repo_root)

    poc_tasks = {
        "tasks": [
            {
                "task_type": "validate_files",
                "execution_target": {
                    "files_to_check": "scripts/auto_ops/validate_task.py;scripts/task_bridge_runner.py"
                },
                "description": "必須ファイル群の存在確認"
            },
            {
                "task_type": "generate_documentation",
                "execution_target": {
                    "output_path": "docs/CLI_AutoDocs.md"
                },
                "description": "CLIの動作確認用ドキュメント生成"
            },
            {
                "task_type": "generate_complete_flag",
                "execution_target": {
                    "path": "AI-TCP_Structure/task_bridge/cli_instructions/complete.flag"
                },
                "description": "全タスク完了後のフラグ生成"
            }
        ]
    }

    output_dir = Path("ai_tcp_tasks")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "poc_phase.yaml"
    with output_path.open("w", encoding="utf-8") as f:
        yaml.dump(poc_tasks, f, allow_unicode=True)
    print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
