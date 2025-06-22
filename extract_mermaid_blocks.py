#!/usr/bin/env python3
"""Extract Mermaid code blocks from docs/ into individual files.

This script scans all Markdown files under ``docs/`` for fenced code blocks
that begin with ``mermaid`` or ``mmd``.  Each block is saved as a ``.mmd`` file
inside ``mermaid_blocks/`` with a comment referencing the source document.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS_DIR = Path("docs")
OUT_DIR = Path("mermaid_blocks")

BLOCK_RE = re.compile(
    r"^```(?:mermaid|mmd)[^\n]*\n(.*?)\n```",
    re.MULTILINE | re.DOTALL,
)


def find_blocks(text: str) -> list[str]:
    """Return Mermaid blocks found in ``text``."""
    return [m.group(1).strip() for m in BLOCK_RE.finditer(text)]


def process_file(md_path: Path) -> None:
    """Extract Mermaid blocks from ``md_path`` and write to ``OUT_DIR``."""
    blocks = find_blocks(md_path.read_text(encoding="utf-8"))
    if not blocks:
        return
    base = md_path.stem
    for idx, code in enumerate(blocks, 1):
        out_path = OUT_DIR / f"{base}_{idx}.mmd"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        header = f"# From {md_path.as_posix()}\n"
        out_path.write_text(header + code + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for md in sorted(DOCS_DIR.rglob("*.md")):
        process_file(md)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - runtime errors
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
