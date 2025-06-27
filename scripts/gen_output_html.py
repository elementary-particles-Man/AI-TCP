#!/usr/bin/env python3
"""Convert Mermaid .mmd.md file to Obsidian compatible HTML.

This script reads a Mermaid file located under ``cli_logs/`` and writes
an HTML file to ``AI-TCP_Structure/html_logs/``.  The output embeds
Mermaid.js and uses minimal CSS (white background, centered layout).
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

MERMAID_RE = re.compile(r"```mermaid\s*(.*?)```", re.DOTALL)


def extract_mermaid(text: str) -> str:
    """Return Mermaid code without fences or ``mmd:`` prefix."""
    m = MERMAID_RE.search(text)
    if m:
        return m.group(1).strip()
    if text.startswith("mmd:"):
        return text.split("mmd:", 1)[1].strip()
    return text.strip()


def build_html(title: str, mermaid: str) -> str:
    """Return simple HTML page with Mermaid code."""
    style = (
        "body{background:#fff;text-align:center;font-family:sans-serif;}"
        ".mermaid{display:inline-block;margin:auto;}"
    )
    return "\n".join(
        [
            "<!DOCTYPE html>",
            "<html lang=\"en\">",
            "<head>",
            "  <meta charset=\"UTF-8\">",
            f"  <title>{title}</title>",
            "  <script src=\"https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js\"></script>",
            f"  <style>{style}</style>",
            "</head>",
            "<body>",
            "  <div class=\"mermaid\">",
            mermaid,
            "  </div>",
            "  <script>mermaid.initialize({startOnLoad:true});</script>",
            "</body>",
            "</html>",
        ]
    )


def process_file(input_path: Path, output_path: Path) -> None:
    mermaid = extract_mermaid(input_path.read_text(encoding='utf-8'))
    html = build_html(output_path.stem, mermaid)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding='utf-8')
    print(f"✅ HTML saved to {output_path}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="mmd.md -> HTML")
    parser.add_argument("input", type=Path, help="cli_logs/YYYYMMDDHHMMSS.mmd.md")
    parser.add_argument("-o", "--output", type=Path, help="output HTML path")
    args = parser.parse_args(argv)

    input_path = args.input
    if args.output:
        output_path = args.output
    else:
        name = input_path.stem
        output_path = Path('AI-TCP_Structure/html_logs') / f"{name}.html"

    process_file(input_path, output_path)


if __name__ == '__main__':
    main()
