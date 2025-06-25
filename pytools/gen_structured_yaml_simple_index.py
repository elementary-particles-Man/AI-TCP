import os
from pathlib import Path

BASE_DIR = Path('structured_yaml')
OUTPUT_FILE = Path('generated_html/structured_yaml_index.html')
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

categories = {
    'Core Schemas': [],
    'Compliance Modules': [],
    'Packet Structures': [],
    'Other YAML Files': [],
}

for path in BASE_DIR.rglob('*.yaml'):
    name = path.name
    lname = name.lower()
    if 'compliance' in lname:
        categories['Compliance Modules'].append(path)
    elif 'packet' in lname or 'structure' in lname:
        categories['Packet Structures'].append(path)
    elif 'schema' in lname:
        categories['Core Schemas'].append(path)
    else:
        categories['Other YAML Files'].append(path)

html = [
    '<!DOCTYPE html>',
    '<html lang="en">',
    '<head>',
    '  <meta charset="UTF-8">',
    '  <title>Structured YAML Index</title>',
    '</head>',
    '<body>',
    '  <h1>Structured YAML Index</h1>',
]

for cat, files in categories.items():
    html.append(f'  <h2>{cat}</h2>')
    html.append('  <ul>')
    if files:
        for f in sorted(files):
            rel = os.path.relpath(f, OUTPUT_FILE.parent)
            html.append(f'    <li><a href="{rel}">{f.name}</a></li>')
    else:
        html.append('    <li>No files found</li>')
    html.append('  </ul>')

html.extend(['</body>', '</html>'])

OUTPUT_FILE.write_text('\n'.join(html), encoding='utf-8')
print(f'Generated {OUTPUT_FILE}')
