#!/usr/bin/env python3
"""Generate simple Markdown documentation for a YAML structure without PyYAML."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, List

# Required fields defined in docs/spec/ai_tcp_yaml_structure.md
REQUIRED = {
    "id",
    "timestamp",
    "lang",
    "phase",
    "data",
    "data.input",
    "data.output",
}


def parse_yaml(path: Path) -> Dict[str, Any]:
    """Parse a limited YAML subset expected for DMC packets."""
    lines = path.read_text(encoding="utf-8").splitlines()
    data: Dict[str, Any] = {}
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("tags:"):
            i += 1
            items: List[str] = []
            while i < n and lines[i].startswith("  - "):
                items.append(lines[i][4:].strip().strip('"'))
                i += 1
            data["tags"] = items
            continue
        if line.startswith("meta:"):
            i += 1
            meta: Dict[str, Any] = {}
            while i < n and lines[i].startswith("  ") and not lines[i].lstrip().startswith("-"):
                key, val = lines[i].split(":", 1)
                meta[key.strip()] = val.strip().strip('"')
                i += 1
            data["meta"] = meta
            continue
        if line.startswith("data:"):
            i += 1
            section: Dict[str, Any] = {}
            while i < n and lines[i].startswith("  "):
                sub = lines[i].strip()
                if sub.startswith("input: |"):
                    i += 1
                    buf: List[str] = []
                    while i < n and lines[i].startswith("    "):
                        buf.append(lines[i][4:])
                        i += 1
                    section["input"] = "\n".join(buf)
                    continue
                if sub.startswith("output: |"):
                    i += 1
                    buf: List[str] = []
                    while i < n and lines[i].startswith("    "):
                        buf.append(lines[i][4:])
                        i += 1
                    section["output"] = "\n".join(buf)
                    continue
                key, val = sub.split(":", 1)
                section[key.strip()] = val.strip().strip('"')
                i += 1
            data["data"] = section
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            data[key.strip()] = val.strip().strip('"')
        i += 1
    return data


def classify(val: Any) -> str:
    if isinstance(val, dict):
        return "dict"
    if isinstance(val, list):
        return "list[scalar]" if (not val or not isinstance(val[0], dict)) else "list[dict]"
    return "scalar"


def traverse(node: Any, path: str, level: int, lines: List[str]) -> None:
    if isinstance(node, dict):
        for key, val in node.items():
            new_path = f"{path}.{key}" if path else key
            required = "yes" if new_path in REQUIRED else "optional"
            lines.append(f"{'#' * level} {key}")
            lines.append("")
            lines.append(f"- path: `{new_path}`")
            lines.append(f"- type: `{classify(val)}`")
            lines.append(f"- required: {required}")
            lines.append("")
            traverse(val, new_path, level + 1, lines)
    elif isinstance(node, list) and node and isinstance(node[0], dict):
        traverse(node[0], f"{path}[]", level, lines)


def generate_markdown(data: Dict[str, Any]) -> str:
    lines: List[str] = []
    traverse(data, "", 1, lines)
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate YAML structure markdown")
    ap.add_argument("input", help="YAML file path")
    ap.add_argument("output", help="Markdown output path")
    args = ap.parse_args()

    data = parse_yaml(Path(args.input))
    markdown = generate_markdown(data)
    Path(args.output).write_text(markdown, encoding="utf-8")
    print(f"[OK] wrote {args.output}")


if __name__ == "__main__":
    main()
