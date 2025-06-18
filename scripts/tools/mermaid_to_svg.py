#!/usr/bin/env python3
"""Convert Mermaid diagram in Markdown to SVG using mmdc."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
import tempfile


def extract_mermaid_block(text: str) -> str:
    """Return Mermaid code from text or raise ValueError."""
    start = text.find("```mermaid")
    if start == -1:
        raise ValueError("Mermaid block not found")
    start = text.find("\n", start)
    if start == -1:
        raise ValueError("Malformed Mermaid block")
    start += 1
    end = text.find("```", start)
    if end == -1:
        end = len(text)
    return text[start:end].strip()


def convert_to_svg(md_path: Path, svg_path: Path) -> None:
    if shutil.which("mmdc") is None:
        raise EnvironmentError("mmdc CLI tool is not installed")

    code = extract_mermaid_block(md_path.read_text(encoding="utf-8"))

    with tempfile.NamedTemporaryFile("w", suffix=".mmd", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    try:
        subprocess.run(["mmdc", "-i", tmp_path, "-o", str(svg_path)], check=True)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Mermaid in Markdown to SVG via mmdc")
    parser.add_argument("input_md", type=Path, help="Input Markdown file")
    parser.add_argument("output_svg", type=Path, help="Output SVG path")
    args = parser.parse_args()

    try:
        convert_to_svg(args.input_md, args.output_svg)
        print(f"[OK] SVG saved to {args.output_svg}")
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
