#!/usr/bin/env python
# build_all.py

import subprocess
import datetime
from pathlib import Path

try:
    import markdown
except ImportError:  # pragma: no cover - markdown may not be installed
    markdown = None


def generate_rfc_docs() -> None:
    """Convert docs/rfc_drafts/*.md to HTML in generated_html/rfc_docs."""
    input_dir = Path("docs/rfc_drafts")
    output_dir = Path("generated_html/rfc_docs")
    output_dir.mkdir(parents=True, exist_ok=True)

    if markdown is None:
        print("⚠️  python-markdown library not installed; skipping RFC HTML generation")
        return

    for md_file in sorted(input_dir.glob("*.md")):
        md_text = md_file.read_text(encoding="utf-8")
        body = markdown.markdown(md_text)
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang=\"en\">",
            "<head>",
            "  <meta charset=\"UTF-8\">",
            f"  <title>{md_file.name}</title>",
            "</head>",
            "<body>",
            f"<h1>{md_file.name}</h1>",
            body,
            "</body>",
            "</html>",
        ]
        output_path = output_dir / f"{md_file.stem}.html"
        output_path.write_text("\n".join(html_parts), encoding="utf-8")
        print(f"✅ RFC HTML generated at {output_path}")

print("\n🛠 AI-TCP Build System Starting...\n")

# DMC session HTMLs
dmc_result = subprocess.run(["python", "tools/gen_dmc_html.py"])
if dmc_result.returncode == 0:
    print("📄 generated_html/index_dmc_sessions.html generated\n")

# Structured YAML HTML
structured_result = subprocess.run(["python", "tools/gen_structured_yaml_html.py"])
if structured_result.returncode == 0:
    print("✅ HTML generated at generated_html/structured_yaml_index.html\n")

# Structure Map HTML
structure_map_result = subprocess.run(["python", "tools/gen_structure_html.py"])
if structure_map_result.returncode == 0:
    print("✅ HTML generated at generated_html/structure_map_master_schema.html\n")

# RFC draft HTML
generate_rfc_docs()

print(f"✅ Build completed at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
