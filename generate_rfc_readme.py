#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path
import re

RFC_DIR = Path('docs/rfc_drafts')
README_PATH = RFC_DIR / 'README.md'


def git_creation_date(path: Path) -> str:
    try:
        result = subprocess.run(
            ['git', 'log', '--format=%ad', '--date=short', '--follow', '--reverse', '--', str(path)],
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )
        first_line = result.stdout.splitlines()[0]
        return first_line.strip()
    except Exception:
        return 'Unknown'


def extract_info(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    title = ''
    summary_lines: list[str] = []
    found_title = False
    for i, line in enumerate(lines):
        if not found_title and line.startswith('#'):
            title = line.lstrip('#').strip()
            found_title = True
            continue
        if found_title:
            if line.strip() == '' or line.startswith('#'):
                if summary_lines:
                    break
                else:
                    continue
            summary_lines.append(line.strip())
    summary = ' '.join(summary_lines).strip()
    return title, summary


def build_readme(rfc_dir: Path) -> str:
    files = sorted(p for p in rfc_dir.glob('*.md') if p.name != 'README.md')
    header = ['# \U0001F4D1 AI-TCP RFC Drafts', '', '| Title | Created | Summary |', '| ----- | ------- | ------- |']
    rows = []
    for f in files:
        title, summary = extract_info(f)
        date = git_creation_date(f)
        link = f'[{title}]({f.name})'
        rows.append(f'| {link} | {date} | {summary} |')
    return '\n'.join(header + rows) + '\n'


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate RFC README listing')
    parser.add_argument('--dir', default=RFC_DIR, type=Path, help='RFC drafts directory')
    parser.add_argument('--output', default=README_PATH, type=Path, help='Output README path')
    args = parser.parse_args()

    content = build_readme(args.dir)
    args.output.write_text(content, encoding='utf-8')
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
