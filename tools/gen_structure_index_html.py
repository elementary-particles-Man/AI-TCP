import re
from datetime import date
from pathlib import Path
import os

SOURCE = Path('docs/AI-TCP_Structure/index.md')
OUTPUT = Path('generated_html/structure_index.html')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

sections = []
current = None
for raw in SOURCE.read_text(encoding='utf-8').splitlines():
    line = raw.strip()
    if line.startswith('```'):
        continue
    if line.startswith('##'):
        heading = line.lstrip('#').strip()
        current = {'heading': heading, 'links': []}
        sections.append(current)
    elif line.startswith('-'):
        m = re.search(r'\[([^\]]+)\]\(([^)]+)\)', line)
        if m and current is not None:
            text, href = m.groups()
            current['links'].append((text, href))

rel_src = os.path.relpath(SOURCE, OUTPUT.parent)
html = [
    '<!DOCTYPE html>',
    '<html lang="en">',
    '<head>',
    '  <meta charset="UTF-8">',
    '  <title>AI-TCP Structure Index</title>',
    '  <link rel="stylesheet" href="../html_templates/structured_index_style.css">',
    '</head>',
    '<body>',
    f'  <p><a href="{rel_src}" target="_blank">🔗 Markdownソースを見る</a></p>',
    '  <h1>AI-TCP Structure Index</h1>',
    '  <p>This portal links to key AI-TCP documents and tools.</p>',
    f'  <p><i>Updated: {date.today().isoformat()}</i></p>',
]
for sec in sections:
    html.append(f'  <h2>{sec["heading"]}</h2>')
    html.append('  <ul>')
    for text, href in sec['links']:
        html.append(f'    <li><a href="{href}" target="_blank">{text}</a></li>')
    html.append('  </ul>')
html.extend(['</body>', '</html>'])

OUTPUT.write_text('\n'.join(html), encoding='utf-8')
print(f'Generated {OUTPUT}')
