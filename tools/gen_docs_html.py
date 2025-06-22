from __future__ import annotations

import sys
from pathlib import Path

# Directory containing markdown docs
DOCS_DIR = Path('docs')
# Base directory for generated HTML
OUTPUT_DIR = Path('generated_html')

# Try to import markdown converters
converter = None
try:
    import markdown2

    converter = lambda text: markdown2.markdown(text)
except Exception:
    try:
        import mistune

        md = mistune.create_markdown()
        converter = lambda text: md(text)
    except Exception:
        converter = None


def convert_file(md_path: Path, out_path: Path) -> None:
    """Convert a single Markdown file to HTML."""
    if converter is None:
        print('[WARN] No markdown library available; skipping', md_path, file=sys.stderr)
        return
    html_body = converter(md_path.read_text(encoding='utf-8'))
    html_lines = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '  <meta charset="UTF-8">',
        f'  <title>{md_path.name}</title>',
        '  <script type="module" src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"></script>',
        '  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>',
        '</head>',
        '<body>',
        html_body,
        '</body>',
        '</html>',
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text('\n'.join(html_lines), encoding='utf-8')
    print(f'[OK] {md_path} -> {out_path}')


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for md_file in DOCS_DIR.rglob('*.md'):
        rel = md_file.relative_to(DOCS_DIR)
        out_file = OUTPUT_DIR / rel.with_suffix('.html')
        convert_file(md_file, out_file)


if __name__ == '__main__':
    main()
