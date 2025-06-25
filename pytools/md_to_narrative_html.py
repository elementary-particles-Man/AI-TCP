from __future__ import annotations

import sys
import re
from pathlib import Path
import html

# Try to import markdown libraries
converter = None
converter_type = None
try:
    import markdown2  # type: ignore

    converter = lambda text: markdown2.markdown(
        text, extras=["fenced-code-blocks", "header-ids"]
    )
    converter_type = "markdown2"
except Exception:
    try:
        import mistune  # type: ignore

        md = mistune.create_markdown()
        converter = lambda text: md(text)
        converter_type = "mistune"
    except Exception:
        converter = None

# Paths relative to repository root
TEMPLATE_DIR = Path("html_templates")
TEMPLATE_FILE = "narrative_template.html"
STYLE_FILE = "narrative_style.css"


def simple_markdown_to_html(text: str):
    """Very small Markdown to HTML converter returning html and heading list."""
    lines = text.splitlines()
    html_lines: list[str] = []
    headings: list[tuple[int, str, str]] = []
    list_open = False
    code_open = False
    code_lang = ""

    def fmt_inline(t: str) -> str:
        t = html.escape(t)
        return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)

    def close_list():
        nonlocal list_open
        if list_open:
            html_lines.append("</ul>")
            list_open = False

    for line in lines:
        if line.startswith("```"):
            if not code_open:
                code_lang = line[3:].strip()
                cls = "mermaid" if code_lang == "mermaid" else ""
                html_lines.append(f'<pre class="{cls}">')
                code_open = True
            else:
                html_lines.append("</pre>")
                code_open = False
            continue
        if code_open:
            html_lines.append(html.escape(line))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            close_list()
            level = len(m.group(1))
            text_val = m.group(2).strip()
            plain = re.sub(r"\*\*(.+?)\*\*", r"\1", text_val)
            slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", plain).strip("-").lower()
            headings.append((level, slug, plain))
            html_lines.append(
                f'<h{level} id="{slug}">{fmt_inline(text_val)}</h{level}>'
            )
            continue
        m = re.match(r"^[*+-]\s+(.*)", line)
        if m:
            if not list_open:
                html_lines.append("<ul>")
                list_open = True
            html_lines.append(f"<li>{fmt_inline(m.group(1).strip())}</li>")
            continue
        close_list()
        if line.strip() == "":
            html_lines.append("")
        else:
            html_lines.append(f"<p>{fmt_inline(line.strip())}</p>")

    close_list()
    if code_open:
        html_lines.append("</pre>")

    return "\n".join(html_lines), headings


def build_toc(headings: list[tuple[int, str, str]]) -> str:
    """Build a nested HTML TOC from heading tuples."""
    matches = headings
    toc_parts: list[str] = ["<details><summary>Table of Contents</summary>"]
    current_level = 0
    for level, hid, text in matches:
        while level > current_level:
            toc_parts.append("<ul>")
            current_level += 1
        while level < current_level:
            toc_parts.append("</ul>")
            current_level -= 1
        toc_parts.append(f'<li><a href="#{hid}">{text}</a></li>')
    while current_level > 0:
        toc_parts.append("</ul>")
        current_level -= 1
    toc_parts.append("</details>")
    return "\n".join(toc_parts)


def convert_file(md_path: Path, out_path: Path) -> None:
    """Convert a Markdown file to styled HTML."""

    template_text = (TEMPLATE_DIR / TEMPLATE_FILE).read_text(encoding="utf-8")
    style_text = (TEMPLATE_DIR / STYLE_FILE).read_text(encoding="utf-8")

    md_text = md_path.read_text(encoding="utf-8")
    headings: list[tuple[int, str, str]]
    if converter is None:
        html_body, headings = simple_markdown_to_html(md_text)
    else:
        html_body = converter(md_text)
        if converter_type == "mistune":
            md_heads = re.findall(r"^(#{1,6})\s+(.*)", md_text, flags=re.MULTILINE)
            headings = []
            for hashes, text_val in md_heads:
                level = len(hashes)
                slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", text_val).strip("-").lower()
                pattern = rf"<h{level}>{re.escape(text_val)}</h{level}>"
                repl = rf'<h{level} id="{slug}">{text_val}</h{level}>'
                html_body = re.sub(pattern, repl, html_body, count=1)
                headings.append((level, slug, text_val))
        else:
            matches = re.findall(r'<h([1-6]) id="([^\"]+)">(.*?)</h\1>', html_body)
            headings = [(int(l), i, t) for l, i, t in matches]

    toc_html = build_toc(headings)
    html_text = (
        template_text.replace("{{ title }}", md_path.name)
        .replace("{{ style }}", style_text)
        .replace("{{ toc | safe }}", toc_html)
        .replace("{{ toc }}", toc_html)
        .replace("{{ content | safe }}", html_body)
        .replace("{{ content }}", html_body)
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_text, encoding="utf-8")
    print(f"[OK] {md_path} -> {out_path}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python pytools/md_to_narrative_html.py input.md [output.html]")
        return
    md_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else md_path.with_suffix(".html")
    convert_file(md_path, out_path)


if __name__ == "__main__":
    main()
