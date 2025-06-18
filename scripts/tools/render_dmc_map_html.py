#!/usr/bin/env python3
"""Render DMC phase map Markdown as HTML with embedded SVG."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


INPUT_MD = Path("dmc_sessions/maps/dmc_session_20250618_map.md")
OUTPUT_HTML = Path("dmc_sessions/maps/dmc_session_20250618_map.html")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <title>DMC Session Phase Map</title>
</head>
<body>
  <h1>DMCセッション・フェーズ構造マップ</h1>
  <p>以下は、2025年6月18日のセッションに基づくフェーズ進行構造図です。</p>
  <!-- SVG content here -->
</body>
</html>
"""


def extract_mermaid_block(text: str) -> str:
    """Return the Mermaid code block from text."""
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
    """Convert Mermaid Markdown to SVG using the mmdc CLI."""
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
    svg_path = INPUT_MD.with_suffix(".svg")
    convert_to_svg(INPUT_MD, svg_path)

    svg_content = svg_path.read_text(encoding="utf-8")
    html = HTML_TEMPLATE.replace("<!-- SVG content here -->", svg_content)

    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"[OK] HTML written to {OUTPUT_HTML}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
