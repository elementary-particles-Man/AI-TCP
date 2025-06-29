import os
import shutil
import subprocess
import datetime

def run_task_workflow():
    cli_instruction_dir = "D:/Dev/AI-TCP/cli_instruction"
    cli_archives_dir = "D:/Dev/AI-TCP/cli_archives"
    new_task_json_source = os.path.join(cli_instruction_dir, "new_task.json")

    # 1. Check for and delete complete.flag
    complete_flag_path = os.path.join(cli_archives_dir, "complete.flag")
    if os.path.exists(complete_flag_path):
        print(f"Deleting existing complete.flag: {complete_flag_path}")
        os.remove(complete_flag_path)
    else:
        print(f"complete.flag not found at {complete_flag_path}. No deletion needed.")

    # 2. Move new_task.json
    if os.path.exists(new_task_json_source):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        new_task_json_dest_name = f"new_task_{timestamp}.json"
        new_task_json_dest = os.path.join(cli_archives_dir, new_task_json_dest_name)
        print(f"Moving {new_task_json_source} to {new_task_json_dest}")
        shutil.move(new_task_json_source, new_task_json_dest)
    else:
        print(f"Error: {new_task_json_source} not found. Cannot move.")
        return # Exit if the source file doesn't exist

    # 3. Execute task_bridge_runner.py
    task_bridge_runner_path = "D:/Dev/AI-TCP/task_bridge_runner.py"
    if os.path.exists(task_bridge_runner_path):
        print(f"Executing {task_bridge_runner_path}...")
        try:
            result = subprocess.run(
                ["python", task_bridge_runner_path],
                capture_output=True,
                text=True,
                check=True
            )
            print("task_bridge_runner.py executed successfully.")
            print("Stdout:", result.stdout)
            if result.stderr:
                print("Stderr:", result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Error executing {task_bridge_runner_path}: {e}")
            print("Stdout:", e.stdout)
            print("Stderr:", e.stderr)
        except FileNotFoundError:
            print("Error: 'python' command not found. Ensure Python is in your PATH.")
    else:
        print(f"Error: {task_bridge_runner_path} not found. Cannot execute.")

if __name__ == "__main__":
    run_task_workflow()
