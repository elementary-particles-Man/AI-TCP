#!/usr/bin/env python3
"""Extract Mermaid code blocks and export them as SVG, PNG and PDF.

This script searches all Markdown files under ``docs/rfc_drafts`` for code
blocks that start with `````mmd:````. Each Mermaid block is converted using
``mmdc`` (Mermaid CLI) and exported to ``output/mermaid_exports``.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path
import tempfile

RFC_DIR = Path("docs/rfc_drafts")
OUT_DIR = Path("output/mermaid_exports")

BLOCK_RE = re.compile(r"```mmd:[^\n]*\n(.*?)```", re.DOTALL)


def find_blocks(text: str) -> list[str]:
    """Return Mermaid blocks found in ``text``."""
    return [m.group(1).strip() for m in BLOCK_RE.finditer(text)]


def render(code: str, base: Path) -> None:
    """Render ``code`` to SVG, PNG and PDF with ``mmdc``."""
    if not shutil.which("mmdc"):
        raise RuntimeError("mmdc command not found. Install mermaid CLI.")
    with tempfile.NamedTemporaryFile("w", suffix=".mmd", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name
    for ext in ("svg", "png", "pdf"):
        out_file = base.with_suffix(f".{ext}")
        cmd = ["mmdc", "-i", tmp_path, "-o", str(out_file)]
        subprocess.run(cmd, check=True)
    Path(tmp_path).unlink(missing_ok=True)


def process_file(md_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")
    blocks = find_blocks(text)
    if not blocks:
        return
    base_name = md_path.stem
    for i, code in enumerate(blocks, start=1):
        out_base = OUT_DIR / f"{base_name}_{i}"
        render(code, out_base)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for md in sorted(RFC_DIR.rglob("*.md")):
        process_file(md)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - runtime errors
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
