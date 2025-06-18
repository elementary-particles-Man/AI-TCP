#!/usr/bin/env python3
"""Generate Markdown documentation for a YAML file structure.

This script reads a YAML file and outputs a Markdown document describing
its hierarchical structure. If a JSON Schema file is provided and contains
`description` fields, they are included alongside each path.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict

import yaml


def classify(value: Any) -> str:
    """Return a simple string representation of the YAML value type."""
    if isinstance(value, dict):
        return "dict"
    if isinstance(value, list):
        if not value:
            return "list"
        first = value[0]
        if isinstance(first, dict):
            return "list[dict]"
        if isinstance(first, list):
            return "list[list]"
        return "list[scalar]"
    return "scalar"


def build_desc_map(schema: Dict[str, Any]) -> Dict[str, str]:
    """Traverse JSON Schema and map paths to descriptions."""
    desc_map: Dict[str, str] = {}

    def _walk(node: Dict[str, Any], path: str) -> None:
        if not isinstance(node, dict):
            return
        if path and "description" in node:
            desc_map[path] = str(node["description"])
        if node.get("type") == "object" and "properties" in node:
            for key, val in node["properties"].items():
                new_path = f"{path}.{key}" if path else key
                _walk(val, new_path)
        if node.get("type") == "array" and "items" in node:
            _walk(node["items"], f"{path}[]")

    _walk(schema, "")
    return desc_map


def traverse(value: Any, lines: list[str], level: int, path: str, desc_map: Dict[str, str]) -> None:
    """Recursively document YAML structure as Markdown."""
    if isinstance(value, dict):
        for key, val in value.items():
            new_path = f"{path}.{key}" if path else key
            lines.append(f"{'#' * level} {key}")
            lines.append("")
            lines.append(f"- path: `{new_path}`")
            lines.append(f"- type: `{classify(val)}`")
            if new_path in desc_map:
                lines.append(f"- description: {desc_map[new_path]}")
            lines.append("")
            traverse(val, lines, level + 1, new_path, desc_map)
    elif isinstance(value, list) and value:
        first = value[0]
        if isinstance(first, (dict, list)):
            traverse(first, lines, level, f"{path}[]", desc_map)


def generate_markdown(data: Any, desc_map: Dict[str, str]) -> str:
    """Return Markdown representation for YAML data."""
    lines: list[str] = []
    traverse(data, lines, 1, "", desc_map)
    return "\n".join(lines)


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate YAML structure docs")
    parser.add_argument("--input", "-i", default="docs/poc_design/direct_mental_care.yaml", help="YAML input path")
    parser.add_argument("--schema", "-s", default="schemas/ai_tcp_packet.schema.yaml", help="Optional schema path")
    parser.add_argument("--output", "-o", default="structured_yaml/README.yaml.md", help="Markdown output path")
    args = parser.parse_args()

    data = load_yaml(Path(args.input))

    desc_map: Dict[str, str] = {}
    schema_path = Path(args.schema)
    if schema_path.exists():
        desc_map = build_desc_map(load_yaml(schema_path))

    markdown = generate_markdown(data, desc_map)
    output_path = Path(args.output)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"[OK] Markdown written to {output_path}")


if __name__ == "__main__":
    main()
