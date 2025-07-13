import subprocess
import json
from pathlib import Path
import os

def invoke_go_module(module_path, input_data=None):
    """Goモジュールを呼び出し、JSONデータを連携する。"""
    command = ["go", "run", module_path]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if input_data:
        stdout, stderr = process.communicate(json.dumps(input_data))
    else:
        stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error invoking Go module: {stderr}")
        return None

    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from Go module: {stdout}")
        return None

if __name__ == "__main__":
    repo_root = Path(os.environ.get("REPO_ROOT", Path(__file__).resolve().parent))
    go_module_path = repo_root / "AI-TCP_Structure" / "tools" / "gen_link_map.go"

    # Goモジュールに渡す入力データ
    sample_input = {"key": "value", "number": 123}

    print(f"Invoking Go module: {go_module_path}")
    output = invoke_go_module(go_module_path, sample_input)

    if output:
        print("Received output from Go module:")
        print(json.dumps(output, indent=2))
