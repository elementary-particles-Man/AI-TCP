import os
import yaml
from pathlib import Path

# === 設定 ===
INPUT_DIR = Path("structured_yaml")
OUTPUT_FILE = Path("generated_html/structured_yaml_index.html")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# === HTMLヘッダ ===
html_parts = [
    "<html>",
    "<head><meta charset='utf-8'><title>Structured YAML Index</title></head>",
    "<body>",
    "<h1>🧾 AI-TCP Structured YAML Session Index</h1>",
    "<p>This page lists PoC YAML sessions for AI-TCP protocols.</p>"
]

# === YAMLファイルの読み込みとHTML化 ===
for yaml_file in sorted(INPUT_DIR.glob("*.yaml")):
    with open(yaml_file, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
            html_parts.append(f"<h2>{yaml_file.name}</h2><ul>")
            html_parts.append(f"<li><b>Phase:</b> {data.get('phase', 'N/A')}</li>")
            html_parts.append(f"<li><b>Agent:</b> {data.get('agent', 'N/A')}</li>")
            html_parts.append(f"<li><b>Tags:</b> {', '.join(data.get('tags', []))}</li>")
            html_parts.append(f"<li><b>Input:</b> {data.get('data', {}).get('input', 'N/A')}</li>")
            html_parts.append(f"<li><b>Output:</b> {data.get('data', {}).get('output', 'N/A')}</li>")
            html_parts.append("</ul>")
        except yaml.YAMLError as e:
            html_parts.append(f"<p>Error parsing {yaml_file.name}: {e}</p>")

# === HTMLフッタ ===
html_parts.extend(["</body>", "</html>"])

# === HTML出力 ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(html_parts))

print(f"✅ HTML generated at {OUTPUT_FILE}")
