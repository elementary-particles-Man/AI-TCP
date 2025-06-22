import argparse
import re
import subprocess
from pathlib import Path
import html

DEFAULT_RFC_DIR = Path('docs/rfc_drafts')
DEFAULT_OUTPUT = Path('output/rfc_index.html')
DEFAULT_BASE_URL = 'https://github.com/your/repo/blob/main'


def git_creation_date(path: Path) -> str:
    try:
        result = subprocess.run(
            ['git', 'log', '--format=%ad', '--date=short', '--follow', '--reverse', str(path)],
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )
        line = result.stdout.splitlines()[0]
        return line.strip()
    except Exception:
        return 'Unknown'


def extract_info(path: Path) -> tuple[str, str, str]:
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()

    title = ''
    start = 0
    for i, line in enumerate(lines):
        if line.startswith('# '):
            title = line.lstrip('#').strip()
            start = i + 1
            break

    date_match = re.search(r'\d{4}-\d{2}-\d{2}', text)
    if date_match:
        date = date_match.group(0)
    else:
        date = git_creation_date(path)

    # Extract first paragraph after title
    summary_lines: list[str] = []
    i = start
    while i < len(lines) and (lines[i].strip() == '' or lines[i].startswith('#')):
        i += 1
    while i < len(lines) and lines[i].strip():
        summary_lines.append(lines[i].strip())
        i += 1
    summary = ' '.join(summary_lines)

    return title, date, summary


def build_html(rfc_dir: Path, base_url: str) -> str:
    files = sorted([p for p in rfc_dir.glob('*.md') if p.name != 'README.md'])
    rows = []
    for path in files:
        title, date, summary = extract_info(path)
        link = f'{base_url}/{path.as_posix()}'
        rows.append(
            f'<tr><td><a href="{link}">{html.escape(path.name)}</a></td>'
            f'<td>{html.escape(title)}</td>'
            f'<td>{html.escape(date)}</td>'
            f'<td>{html.escape(summary)}</td></tr>'
        )
    table = '\n'.join(rows)
    html_text = (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '  <meta charset="utf-8">\n'
        '  <title>RFC Index</title>\n'
        '  <style>\n'
        '    table{border-collapse:collapse;width:100%;}\n'
        '    th,td{border:1px solid #ccc;padding:4px;}\n'
        '    th{background-color:#f0f0f0;}\n'
        '  </style>\n'
        '</head>\n'
        '<body>\n'
        '  <h1>RFC Index</h1>\n'
        '  <table>\n'
        '    <tr><th>File</th><th>Title</th><th>Date</th><th>Summary</th></tr>\n'
        f'{table}\n'
        '  </table>\n'
        '</body>\n'
        '</html>\n'
    )
    return html_text


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate HTML index for RFC drafts')
    parser.add_argument('--rfc-dir', type=Path, default=DEFAULT_RFC_DIR)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--base-url', default=DEFAULT_BASE_URL,
                        help='Base URL to prefix file paths for links')
    args = parser.parse_args()

    html_content = build_html(args.rfc_dir, args.base_url.rstrip('/'))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html_content, encoding='utf-8')
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
