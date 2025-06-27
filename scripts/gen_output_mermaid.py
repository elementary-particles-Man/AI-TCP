# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

# --- 設定項目 ---
# このスクリプトが置かれているディレクトリを基準とする
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# AI-TCPのルートディレクトリまで遡る
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

# 入力・出力先の定義
INPUT_JSON_PATH = os.path.join(PROJECT_ROOT, "AI-TCP_Structure", "task_bridge", "cli_logs", "output.json")
OUTPUT_MD_PATH = os.path.join(PROJECT_ROOT, "AI-TCP_Structure", "graph", "latest_output_visualization.mmd.md")

def generate_mermaid_from_output(output_data: dict) -> str:
    """
    output.jsonのデータを受け取り、Mermaid.jsのgraph TD形式の文字列を生成する。
    """
    meta = output_data.get("response_metadata", {})
    result = output_data.get("execution_result", {})
    error = output_data.get("error_details")

    # --- ノードとスタイルの定義 ---
    graph_str = "graph TD\n"
    graph_str += "    %% --- スタイル定義 ---\n"
    graph_str += "    classDef success fill:#d4edda,stroke:#c3e6cb,stroke-width:2px;\n"
    graph_str += "    classDef error fill:#f8d7da,stroke:#f5c6cb,stroke-width:2px;\n"
    graph_str += "    classDef process fill:#e2e3e5,stroke:#d6d8db;\n"
    graph_str += "    classDef io fill:#cce5ff,stroke:#b8daff;\n\n"

    # --- ノードの定義 ---
    task_id = meta.get('original_task_id', 'N/A')
    resp_id = meta.get('response_id', 'N/A')
    status = meta.get('execution_status', 'unknown')

    graph_str += f"    %% --- ノード定義 ---\n"
    graph_str += f"    A[new_task.json<br/>id: {task_id}]:::io\n"
    graph_str += f"    B{{Gemini CLI Agent<br/>実行: {meta.get('executed_by', 'N/A')}}};;;process\n"
    graph_str += f"    C[output.json<br/>id: {resp_id}]:::io\n"

    # ステータスに応じて結果ノードを追加
    if status == "success":
        result_message = result.get("message", "No message")
        graph_str += f"    D[\"✅ 成功<br/>{result_message}\"]:::success\n"
        # 詳細情報の追加
        details = result.get("details", {})
        details_str = "<br/>".join([f"{k}: {v}" for k, v in details.items()])
        graph_str += f"    E[\"詳細<br/>{details_str}\"]\n"
        graph_str += "    D --> E\n"

    else:
        error_message = error.get("message", "No message") if error else "Unknown error"
        graph_str += f"    D[\"❌ 失敗<br/>{error_message}\"]:::error\n"
        if error and "code" in error:
             graph_str += f"    E[\"エラーコード: {error.get('code')}\"]\n"
             graph_str += "    D --> E\n"


    # --- 関係性の定義 ---
    graph_str += "\n    %% --- 関係性定義 ---\n"
    graph_str += f"    A --依頼--> B\n"
    graph_str += f"    B --実行結果--> C\n"
    graph_str += f"    C --ステータス--> D\n"

    return graph_str

def main():
    """
    メイン関数
    """
    print(f"[INFO] output.json を読み込んでいます: {INPUT_JSON_PATH}")
    if not os.path.exists(INPUT_JSON_PATH):
        print(f"[ERROR] 入力ファイルが見つかりません: {INPUT_JSON_PATH}")
        return

    try:
        with open(INPUT_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSONの解析に失敗しました: {e}")
        return

    print("[INFO] Mermaidグラフを生成しています...")
    mermaid_content = generate_mermaid_from_output(data)

    output_wrapper = f"""
# AI-TCP 実行結果可視化

- **生成日時:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **元データ:** `{os.path.basename(INPUT_JSON_PATH)}`

```mermaid
{mermaid_content}
```
"""
    
    print(f"[INFO] Mermaidファイルを保存しています: {OUTPUT_MD_PATH}")
    with open(OUTPUT_MD_PATH, 'w', encoding='utf-8') as f:
        f.write(output_wrapper)
    
    print("[INFO] 処理が正常に完了しました。")


if __name__ == "__main__":
    main()
