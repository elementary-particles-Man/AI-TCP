#!/usr/bin/env python3
"""Batch convert Mermaid code blocks in Markdown files to SVG.

This script searches the given directory recursively for `.md` files,
extracts Mermaid diagrams, and converts them to SVG using
`mermaid_to_svg.py`. Logs of successes and failures are appended to the
`log/` directory at the repository root.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
import tempfile

# Location of the existing conversion script
THIS_DIR = Path(__file__).resolve().parent
MERMAID_SCRIPT = THIS_DIR / "mermaid_to_svg.py"

ROOT_DIR = THIS_DIR.parent.parent  # repository root
LOG_DIR = ROOT_DIR / "log"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "batch_mermaid_svg.log"


def log(message: str) -> None:
    """Append a message to the log file."""
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(message + "\n")


def find_mermaid_blocks(text: str) -> list[str]:
    """Return Mermaid code blocks found in text."""
    blocks: list[str] = []
    start = 0
    while True:
        idx = text.find("```mermaid", start)
        if idx == -1:
            break
        idx = text.find("\n", idx)
        if idx == -1:
            break
        idx += 1
        end = text.find("```", idx)
        if end == -1:
            end = len(text)
        blocks.append(text[idx:end].strip())
        start = end + 3
    return blocks


def convert_block(block: str, svg_path: Path) -> None:
    """Convert a Mermaid block to SVG via mermaid_to_svg.py."""
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as tmp:
        tmp.write("```mermaid\n" + block + "\n```")
        tmp_path = Path(tmp.name)

    try:
        subprocess.run([
            sys.executable,
            str(MERMAID_SCRIPT),
            str(tmp_path),
            str(svg_path),
        ], check=True)
    finally:
        tmp_path.unlink(missing_ok=True)


def process_file(md_path: Path) -> None:
    """Process a single Markdown file for Mermaid blocks."""
    text = md_path.read_text(encoding="utf-8")
    blocks = find_mermaid_blocks(text)
    if not blocks:
        return

    for i, block in enumerate(blocks, 1):
        suffix = "" if len(blocks) == 1 else f"_{i}"
        svg_path = md_path.with_name(md_path.stem + f"_mermaid{suffix}.svg")
        try:
            convert_block(block, svg_path)
            msg = f"OK: {md_path} -> {svg_path}"
            print(f"[OK] {md_path} -> {svg_path}")
        except Exception as exc:  # noqa: BLE001
            msg = f"ERROR: {md_path} -> {exc}"
            print(f"[ERROR] {md_path}: {exc}", file=sys.stderr)
        log(msg)


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch render Mermaid diagrams to SVG")
    parser.add_argument("directory", type=Path, help="target directory")
    args = parser.parse_args()

    for md_file in args.directory.rglob("*.md"):
        process_file(md_file)


if __name__ == "__main__":
    main()
