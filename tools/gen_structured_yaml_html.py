import os
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# === 設定 ===
INPUT_DIR = Path("structured_yaml")
TEMPLATE_PATH = Path("docs/templates")
TEMPLATE_FILE = "html_template_base.html"
OUTPUT_FILE = Path("generated_html/structured_yaml_index.html")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# === テンプレート読み込み ===
env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
template = env.get_template(TEMPLATE_FILE)

# === YAMLファイルの読み込み ===
sessions = []

for yaml_file in sorted(INPUT_DIR.glob("*.yaml")):
    with open(yaml_file, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
            sessions.append({
                "filename": yaml_file.name,
                "phase": data.get("phase", "N/A"),
                "agent": data.get("agent", "N/A"),
                "tags": data.get("tags", []),
                "input": data.get("data", {}).get("input", "N/A"),
                "output": data.get("data", {}).get("output", "N/A"),
            })
        except yaml.YAMLError as e:
            sessions.append({
                "filename": yaml_file.name,
                "phase": "Error",
                "agent": "Parse Error",
                "tags": [],
                "input": f"Error parsing YAML: {e}",
                "output": "N/A"
            })

# === テンプレート適用 ===
html = template.render(
    title="Structured YAML Index",
    header="🧾 AI-TCP Structured YAML Session Index",
    description="This page lists PoC YAML sessions for AI-TCP protocols.",
    sessions=sessions
)

# === 出力 ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ HTML generated at {OUTPUT_FILE}")
