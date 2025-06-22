#!/usr/bin/env python3
"""Generate a combined Mermaid diagram HTML from YAML files.

This script scans a directory recursively for YAML files and extracts
`graph_payload.graph_structure` fields containing Mermaid diagrams. A
single HTML page listing all found diagrams is created for easy
comparison.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import yaml


def _find_mermaid_blocks(obj: object) -> list[str]:
    """Recursively collect Mermaid blocks from `graph_payload.graph_structure`."""
    blocks: list[str] = []

    def _walk(node: object) -> None:
        if isinstance(node, dict):
            if "graph_payload" in node:
                gp = node.get("graph_payload")
                if isinstance(gp, dict) and "graph_structure" in gp:
                    gs = gp.get("graph_structure")
                    if isinstance(gs, str) and "mmd:" in gs:
                        blocks.append(gs.split("mmd:", 1)[1].strip())
            for v in node.values():
                _walk(v)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(obj)
    return blocks


def _process_yaml(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
    except Exception as exc:  # pragma: no cover - parse errors are reported
        print(f"❌ Failed to parse {path}: {exc}")
        return []
    return _find_mermaid_blocks(data)


def generate_html(directory: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    html: list[str] = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        "  <title>Mermaid Graph Structures</title>",
        "  <script type=\"module\" src=\"https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs\"></script>",
        "  <style>body{font-family:sans-serif;padding:1em;} pre{background:#f8f8f8;padding:1em;border-radius:8px;overflow-x:auto;} h2{margin-top:2em;}</style>",
        "</head>",
        "<body>",
        "  <h1>Mermaid Graph Structures</h1>",
    ]

    for yaml_path in sorted(directory.rglob("*.yaml")):
        blocks = _process_yaml(yaml_path)
        if not blocks:
            continue
        rel = os.path.relpath(yaml_path, output.parent)
        html.append(f"  <h2>{yaml_path.name}</h2>")
        html.append(f"  <p><a href=\"{rel}\" target=\"_blank\">🔗 YAMLソースを見る</a></p>")
        for block in blocks:
            html.append("  <pre><code class=\"language-mermaid\">")
            html.append(block)
            html.append("  </code></pre>")

    html.append("  <script>mermaid.initialize({startOnLoad:true});</script>")
    html.append("</body>")
    html.append("</html>")

    output.write_text("\n".join(html), encoding="utf-8")
    print(f"✅ Generated {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Mermaid HTML from multiple YAML files")
    parser.add_argument("directory", nargs="?", default="structured_yaml", help="target directory to scan")
    parser.add_argument("-o", "--output", default="generated_html/mermaid_multi.html", help="output HTML file")
    args = parser.parse_args()

    generate_html(Path(args.directory), Path(args.output))


if __name__ == "__main__":
    main()
