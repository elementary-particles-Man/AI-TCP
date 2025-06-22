#!/usr/bin/env python3
"""Extract Mermaid diagrams from RFC markdown and generate individual HTML files."""
from __future__ import annotations

import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

RFC_DIR = Path("docs/rfc_drafts")
OUTPUT_DIR = Path("output/mermaid_htmls")
TEMPLATE = Path("html_templates/mermaid_block_template.html")


_MMD_PATTERN = re.compile(r"```mmd:\s*([\s\S]*?)```", re.MULTILINE)


def extract_mmd_blocks(text: str) -> list[str]:
    """Return list of Mermaid code blocks without surrounding markers."""
    return [m.group(1).strip() for m in _MMD_PATTERN.finditer(text)]


def render_blocks(md_path: Path, env: Environment) -> None:
    blocks = extract_mmd_blocks(md_path.read_text(encoding="utf-8"))
    if not blocks:
        return

    template = env.get_template(TEMPLATE.name)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for idx, block in enumerate(blocks, 1):
        html = template.render(title=f"{md_path.stem} {idx}", mermaid=block)
        out = OUTPUT_DIR / f"{md_path.stem}_{idx}.html"
        out.write_text(html, encoding="utf-8")
        print(f"Generated {out}")


def main() -> None:
    env = Environment(loader=FileSystemLoader(str(TEMPLATE.parent)))
    for md_file in sorted(RFC_DIR.glob("*.md")):
        render_blocks(md_file, env)


if __name__ == "__main__":
    main()
