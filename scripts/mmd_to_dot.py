#!/usr/bin/env python3
"""Extract ```mmd:``` code blocks from docs/rfc_drafts and convert to DOT.

This script searches all Markdown files under ``docs/rfc_drafts`` for fenced
code blocks beginning with ``mmd:``. For each Mermaid flowchart block found,
it generates a simplistic Graphviz ``digraph`` representation capturing only
node and edge relationships. The result for each block is written to
``output/graphviz_dot`` as ``<markdown_name>_<n>.dot`` where ``n`` is a
sequential number per source file.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs" / "rfc_drafts"
OUTPUT_DIR = ROOT_DIR / "output" / "graphviz_dot"

# Match start of a fenced block like ```mmd:flowchart
FENCE_RE = re.compile(r"^```\s*mmd:(.*)")

def parse_nodes(token: str) -> str:
    """Return a simplified node name removing label syntax."""
    token = token.strip()
    token = re.sub(r"[\[{].*", "", token)
    return re.sub(r"[^A-Za-z0-9_]+", "", token)

def mermaid_to_dot(lines: list[str], header: str | None = None) -> str:
    """Very basic conversion of Mermaid flowchart to DOT digraph."""
    if not lines:
        return ""
    orientation = "G"
    header_line = header or (lines[0].strip() if lines else "")
    m = re.match(r"flowchart\s+(\w+)", header_line)
    if m:
        orientation = m.group(1)
        body = lines
    else:
        body = lines[1:]
    dot_lines = [f"digraph {orientation} {{"]
    for line in body:
        line = line.strip()
        m = re.search(r"(\S+).*--[>-].*(\S+)", line)
        if m:
            src = parse_nodes(m.group(1))
            dst = parse_nodes(m.group(2))
            if src and dst:
                dot_lines.append(f"    {src} -> {dst};")
    dot_lines.append("}")
    return "\n".join(dot_lines) + "\n"

def process_markdown(md_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    idx = 0
    block_no = 0
    while idx < len(lines):
        line = lines[idx]
        m = FENCE_RE.match(line)
        if m:
            block: list[str] = []
            idx += 1
            while idx < len(lines) and not lines[idx].startswith("```"):
                block.append(lines[idx])
                idx += 1
            idx += 1  # skip closing fence
            block_no += 1
            dot = mermaid_to_dot(block, m.group(1).strip())
            if dot.strip():
                out_name = f"{md_path.stem}_{block_no}.dot"
                out_path = OUTPUT_DIR / out_name
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(dot, encoding="utf-8")
        else:
            idx += 1

def main() -> None:
    for md in DOCS_DIR.rglob("*.md"):
        if md.is_file():
            process_markdown(md)

if __name__ == "__main__":
    main()
