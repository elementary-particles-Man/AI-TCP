#!/usr/bin/env python3
"""YAML -> HTML -> Mermaid conversion proof-of-concept.

This script scans `structured_yaml/validated_yaml/` for YAML files and performs
three steps:

1. Convert each YAML file to a simple HTML representation and save it to
   `temp/`.
2. Read the generated HTML, extract the YAML content and build a `flowchart TD`
   Mermaid graph describing the YAML structure.
3. Save the Mermaid code as `.mmd` in `temp/`.

The script requires PyYAML. No external HTML parsing dependencies are used.
"""
from __future__ import annotations

import html
import os
import re
from pathlib import Path

import yaml

INPUT_DIR = Path("structured_yaml/validated_yaml")
TEMP_DIR = Path("temp")


def yaml_to_html(yaml_path: Path) -> str:
    """Return HTML representation for the YAML file."""
    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        data = {"error": str(exc)}
    yaml_text = yaml.dump(data, allow_unicode=True, sort_keys=False)
    lines = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "  <meta charset='UTF-8'>",
        f"  <title>{yaml_path.name}</title>",
        "</head>",
        "<body>",
        "  <pre>",
        html.escape(yaml_text),
        "  </pre>",
        "</body>",
        "</html>",
    ]
    return "\n".join(lines)


def extract_yaml_from_html(html_text: str) -> str:
    """Return YAML text contained in <pre>...</pre> block."""
    m = re.search(r"<pre>(.*?)</pre>", html_text, flags=re.S)
    if m:
        return html.unescape(m.group(1)).strip()
    return ""


def yaml_to_mermaid(data: object) -> str:
    """Convert YAML data structure to Mermaid flowchart code."""
    lines: list[str] = ["flowchart TD", "  root[\"root\"]"]
    counter = 0

    def sanitize(label: str) -> str:
        return label.replace("\"", "\'")

    def traverse(node: object, parent: str) -> None:
        nonlocal counter
        if isinstance(node, dict):
            for key, value in node.items():
                counter += 1
                nid = f"n{counter}"
                lines.append(f"  {parent} --> {nid}[\"{sanitize(str(key))}\"]")
                traverse(value, nid)
        elif isinstance(node, list):
            for item in node:
                counter += 1
                nid = f"n{counter}"
                lines.append(f"  {parent} --> {nid}((item))")
                traverse(item, nid)
        else:
            counter += 1
            nid = f"n{counter}"
            label = sanitize(str(node))
            lines.append(f"  {parent} --> {nid}[\"{label}\"]")

    traverse(data, "root")
    return "\n".join(lines)


def process_yaml_file(yaml_file: Path) -> None:
    """Convert a YAML file to HTML and Mermaid."""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    html_path = TEMP_DIR / f"{yaml_file.stem}.html"
    html_content = yaml_to_html(yaml_file)
    html_path.write_text(html_content, encoding="utf-8")

    yaml_text = extract_yaml_from_html(html_content)
    if not yaml_text:
        print(f"⚠️ YAML not found in {html_path}")
        return
    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        print(f"❌ Failed to parse YAML from {html_path}: {exc}")
        return

    mermaid = yaml_to_mermaid(data)
    mmd_path = TEMP_DIR / f"{yaml_file.stem}.mmd"
    mmd_path.write_text(mermaid, encoding="utf-8")
    print(f"✅ {yaml_file.name} -> {mmd_path}")


def main() -> None:
    for yaml_file in sorted(INPUT_DIR.glob("*.yaml")):
        process_yaml_file(yaml_file)


if __name__ == "__main__":
    main()
