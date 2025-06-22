#!/usr/bin/env python3
"""Reformat Mermaid code blocks with `mmd:` prefix in docs/.

This script scans all Markdown files under ``docs/`` and converts code blocks
that contain Mermaid diagrams prefixed with ``mmd:`` to standard ``mermaid``
code blocks.  The modified files are written to ``docs/_autofix/`` preserving
the original directory structure.  Source files remain unchanged.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
OUTPUT_DIR = DOCS_DIR / "_autofix"

FENCE_RE = re.compile(r"^(\s*)(```+|~~~+)(.*)$")


def process_block(lines: list[str]) -> list[str]:
    """Return processed lines for a fenced code block."""
    if len(lines) < 2:
        return lines

    start_line = lines[0]
    end_line = lines[-1]
    body = lines[1:-1]

    # Find first non-empty content line
    for idx, line in enumerate(body):
        if line.strip():
            stripped = line.lstrip()
            if stripped.startswith("mmd:"):
                body[idx] = line.replace("mmd:", "", 1)
                start_line = re.sub(FENCE_RE, r"\1\2mermaid", start_line)
            break

    return [start_line, *body, end_line]


def fix_file(path: Path) -> None:
    """Write a fixed version of ``path`` under ``docs/_autofix``."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    result: list[str] = []
    block: list[str] | None = None
    fence = ""

    for line in lines:
        m = FENCE_RE.match(line)
        if block is None:
            if m:
                block = [line]
                fence = m.group(2)
            else:
                result.append(line)
        else:
            block.append(line)
            if line.strip() == fence:
                result.extend(process_block(block))
                block = None
                fence = ""

    if block is not None:  # unterminated block
        result.extend(block)

    out_path = OUTPUT_DIR / path.relative_to(DOCS_DIR)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(result) + "\n", encoding="utf-8")


def main() -> None:
    for md in DOCS_DIR.rglob("*.md"):
        if md.is_file() and OUTPUT_DIR not in md.parents:
            fix_file(md)


if __name__ == "__main__":
    main()
