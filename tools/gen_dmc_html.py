import os
import yaml
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# ディレクトリ定義
DMC_DIR = "dmc_sessions"
OUTPUT_DIR = "generated_html"
TEMPLATE_PATH = "docs/templates"
TEMPLATE_FILE = "html_template_dmc.html"

# HTML生成環境初期化
env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
template = env.get_template(TEMPLATE_FILE)

def generate_dmc_html():
    for filename in os.listdir(DMC_DIR):
        if not filename.endswith(".yaml"):
            continue

        filepath = os.path.join(DMC_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        html = template.render(
            title=f"DMC Session: {filename}",
            header="🧠 DMC Session Output",
            description="This page renders a full AI session for mental care.",
            session={
                "filename": filename,
                "phase": content.get("phase", ""),
                "agent": content.get("agent", ""),
                "tags": content.get("tags", []),
                "input": content.get("data", {}).get("input", ""),
                "output": content.get("data", {}).get("output", "")
            }
        )

        output_path = os.path.join(OUTPUT_DIR, filename.replace(".yaml", ".html"))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ {output_path} generated")

if __name__ == "__main__":
    generate_dmc_html()
