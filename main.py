import subprocess
import json

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
    # サンプルGoモジュール (仮定: D:/Dev/AI-TCP/AI-TCP_Structure/tools/gen_link_map.go)
    go_module_path = "D:/Dev/AI-TCP/AI-TCP_Structure/tools/gen_link_map.go"

    # Goモジュールに渡す入力データ
    sample_input = {"key": "value", "number": 123}

    print(f"Invoking Go module: {go_module_path}")
    output = invoke_go_module(go_module_path, sample_input)

    if output:
        print("Received output from Go module:")
        print(json.dumps(output, indent=2))
