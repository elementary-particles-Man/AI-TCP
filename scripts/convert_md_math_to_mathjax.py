#!/usr/bin/env python3
"""Convert LaTeX math in docs/ for MathJax.

This script searches all Markdown files under ``docs/`` and converts LaTeX
expressions written with ``$...$`` or ``$$...$$`` to the ``\(...\)`` and
``\[...\]`` forms expected by MathJax.  The original files are left
untouched; converted versions are written under ``converted_md/`` preserving
the directory structure.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
OUT_DIR = ROOT_DIR / "converted_md"

FENCE_RE = re.compile(r"^(\s*)(```+|~~~+)")
BLOCK_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
INLINE_MATH_RE = re.compile(r"\$(.+?)\$")


def convert_text(text: str) -> str:
    """Convert LaTeX math in a block of plain Markdown text."""
    text = BLOCK_MATH_RE.sub(r"\\[\1\\]", text)
    parts = re.split(r"(`[^`]*`)", text)
    for i, part in enumerate(parts):
        if i % 2 == 0:
            parts[i] = INLINE_MATH_RE.sub(r"\\(\1\\)", part)
    return "".join(parts)


def convert_file(path: Path) -> None:
    """Write converted version of ``path`` under ``converted_md``."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    segments: list[tuple[str, str]] = []
    buf: list[str] = []
    in_code = False
    fence = ""

    for line in lines:
        m = FENCE_RE.match(line)
        if in_code:
            buf.append(line)
            if m and m.group(2) == fence:
                segments.append(("code", "".join(buf)))
                buf = []
                in_code = False
        else:
            if m:
                if buf:
                    segments.append(("text", "".join(buf)))
                    buf = []
                in_code = True
                fence = m.group(2)
                buf.append(line)
            else:
                buf.append(line)
    if buf:
        segments.append(("code" if in_code else "text", "".join(buf)))

    result = []
    for kind, seg in segments:
        if kind == "text":
            result.append(convert_text(seg))
        else:
            result.append(seg)
    out_text = "".join(result)

    out_path = OUT_DIR / path.relative_to(DOCS_DIR)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out_text, encoding="utf-8")


def main() -> None:
    for md in DOCS_DIR.rglob("*.md"):
        if md.is_file():
            convert_file(md)


if __name__ == "__main__":
    main()
