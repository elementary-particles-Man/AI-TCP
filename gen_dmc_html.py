# gen_dmc_html.py
# YAML 形式の DMC トレースを HTML に変換するスクリプト

import yaml
from pathlib import Path

INPUT_PATH = Path("structured_yaml/validated_yaml/ai_tcp_dmc_trace.yaml")
OUTPUT_PATH = Path("generated_html/DMC_20250618.html")


def parse_yaml_trace(yaml_data):
    """
    YAMLデータをパースし、HTML出力用に整形されたデータ構造へ変換
    """
    header = yaml_data.get("meta") or yaml_data.get("session_trace", {}).get("session_id")
    phases = yaml_data.get("session_trace", {}).get("phases")
    
    return header, phases


def generate_html(header, phases):
    html_parts = ["<html><head><meta charset='utf-8'><title>DMC Trace</title></head><body>"]
    
    html_parts.append("<h1>DMCセッション トレース</h1>")
    if isinstance(header, dict):
        html_parts.append(f"<h2>{header.get('title', 'No Title')}</h2>")
    else:
        html_parts.append(f"<h2>Session ID: {header}</h2>")

    if phases:
        for phase in phases:
            html_parts.append(f"<h3>フェーズ: {phase.get('name')}</h3>")
            for pkt in phase.get("packets", []):
                html_parts.append("<div style='margin-left:20px;'>")
                html_parts.append(f"<p><strong>ID:</strong> {pkt.get('packet_id')}</p>")
                html_parts.append(f"<p><strong>意図:</strong> {pkt.get('intent')}</p>")
                html_parts.append(f"<p><strong>トレースリンク:</strong> {pkt.get('trace_link')}</p>")
                html_parts.append("</div>")

    html_parts.append("</body></html>")
    return "\n".join(html_parts)


def main():
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)

    header, phases = parse_yaml_trace(yaml_data)
    html_out = generate_html(header, phases)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html_out)

    print(f"✔ HTML 出力完了: {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
