#!/usr/bin/env python3
"""Convert Markdown heading hierarchy to a Mermaid flowchart.

This utility reads a Markdown file and outputs `<name>.mmd.md` containing
 a `flowchart TD` representation of the heading structure. Newlines inside
labels are converted to `<br>` for better rendering in tools like Obsidian.
"""
from __future__ import annotations

import argparse
import re
import string
from pathlib import Path
from typing import List, Tuple

HEADER_RE = re.compile(r'^(#{1,6})\s*(.+)$')


def parse_headings(text: str) -> List[Tuple[int, str]]:
    """Return list of `(level, title)` tuples from Markdown text."""
    headings: List[Tuple[int, str]] = []
    for line in text.splitlines():
        m = HEADER_RE.match(line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            headings.append((level, title))
    return headings


def _next_letter(idx: int) -> str:
    """Return uppercase letter sequence for `idx` (0=A, 1=B, ...)."""
    letters = string.ascii_uppercase
    if idx < len(letters):
        return letters[idx]
    idx -= len(letters)
    return letters[idx // len(letters)] + letters[idx % len(letters)]


def build_mermaid(headings: List[Tuple[int, str]]) -> str:
    """Generate Mermaid `flowchart TD` code from headings."""
    lines = ["flowchart TD"]
    id_by_level: dict[int, str] = {}
    count_by_level: dict[int, int] = {}

    for level, title in headings:
        count_by_level[level] = count_by_level.get(level, 0) + 1
        for lvl in list(count_by_level):
            if lvl > level:
                del count_by_level[lvl]
                id_by_level.pop(lvl, None)
        if level == 1:
            node_id = _next_letter(count_by_level[level] - 1)
        else:
            parent_id = id_by_level[level - 1]
            node_id = f"{parent_id}{count_by_level[level]}"
        id_by_level[level] = node_id
        label = title.replace("\n", "<br>")
        if level == 1:
            lines.append(f"{node_id}[{label}]")
        else:
            parent = id_by_level[level - 1]
            lines.append(f"{node_id}[{label}] --> {parent}")
    return "\n".join(lines) + "\n"


def process_file(md_path: Path, out_path: Path) -> None:
    headings = parse_headings(md_path.read_text(encoding="utf-8"))
    mermaid = build_mermaid(headings)
    out_path.write_text(f"mmd:{mermaid}", encoding="utf-8")
    print(f"✅ Mermaid saved to {out_path}")


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Markdown headings -> Mermaid")
    parser.add_argument("markdown", type=Path, help="input Markdown file")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        help="output .mmd.md path (defaults to same name)",
    )
    args = parser.parse_args(argv)

    md_path: Path = args.markdown
    out_path: Path = args.output if args.output else md_path.with_suffix(".mmd.md")

    process_file(md_path, out_path)


if __name__ == "__main__":
    main()
