#!/usr/bin/env python3
"""Convert Markdown heading hierarchy to YAML.

This script reads a Markdown file and extracts heading levels (#, ##, ###, ...).
It outputs a YAML file representing the hierarchy with automatically generated
IDs based on the heading titles.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:  # PyYAML may not be installed
    yaml = None

# Regular expressions for parsing headings and numeric prefixes
HEADER_RE = re.compile(r"^(#+)\s*(.+)$")
CHAPTER_RE = re.compile(r"^\s*第(\d+)章")
SECTION_RE = re.compile(r"^\s*(\d+(?:\.\d+)*)")


def slugify(text: str) -> str:
    """Generate a simple slug from a title."""
    slug = text.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "section"


def title_to_id(title: str) -> str:
    """Generate an ID from the given title."""
    m = CHAPTER_RE.match(title)
    if m:
        return f"chapter{m.group(1)}"
    m = SECTION_RE.match(title)
    if m:
        return f"section{m.group(1).replace('.', '-')}"
    return slugify(title)


def parse_markdown(path: Path):
    """Return a list of (level, title) tuples from the Markdown file."""
    headers = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = HEADER_RE.match(line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            headers.append((level, title))
    return headers


def build_tree(headers):
    """Build a nested tree from a sequence of headers."""
    root = []
    stack = [{"level": 0, "children": root}]
    for level, title in headers:
        node = {"title": title, "id": title_to_id(title), "children": []}
        while stack and stack[-1]["level"] >= level:
            stack.pop()
        stack[-1]["children"].append(node)
        stack.append({"level": level, "children": node["children"]})
    _prune_children(root)
    return root


def _prune_children(nodes):
    for node in nodes:
        if not node["children"]:
            node.pop("children")
        else:
            _prune_children(node["children"])


def write_yaml(tree, path: Path) -> None:
    """Write the nested tree to a YAML file."""
    if yaml:
        with path.open("w", encoding="utf-8") as fh:
            yaml.dump(tree, fh, allow_unicode=True, sort_keys=False)
    else:
        path.write_text(_simple_dump(tree), encoding="utf-8")


def _simple_dump(nodes, indent: int = 0) -> str:
    """Minimal YAML dumper used when PyYAML is unavailable."""
    lines = []
    prefix = "  " * indent
    for node in nodes:
        lines.append(f"{prefix}- title: {node['title']}")
        lines.append(f"{prefix}  id: {node['id']}")
        if "children" in node:
            lines.append(f"{prefix}  children:")
            lines.append(_simple_dump(node["children"], indent + 2))
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Convert Markdown heading structure to YAML")
    ap.add_argument("input", help="Markdown file path")
    ap.add_argument("output", help="Output YAML file path")
    args = ap.parse_args()

    headers = parse_markdown(Path(args.input))
    tree = build_tree(headers)
    write_yaml(tree, Path(args.output))
    print(f"YAML written to {args.output}")


if __name__ == "__main__":
    main()
