#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path
import re

RFC_DIR = Path('docs/rfc_drafts')
README_PATH = RFC_DIR / 'README.md'


def git_last_modified_date(path: Path) -> str:
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ad', '--date=short', '--', str(path)],
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.splitlines()[0].strip()
    except Exception:
        return 'Unknown'


def extract_title(path: Path) -> str:
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('# '):
            return line.lstrip('#').strip()
    return ''


def build_readme(rfc_dir: Path) -> str:
    files = sorted([p for p in rfc_dir.glob('*.md') if p.name != 'README.md'])
    lines = ['# AI-TCP RFC Drafts', '']
    for f in files:
        title = extract_title(f)
        date = git_last_modified_date(f)
        lines.append(f"- [{f.name}]({f.name}) - {title} (Updated: {date})")
    lines.append('')
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate RFC README TOC')
    parser.add_argument('--dir', default=RFC_DIR, type=Path, help='RFC drafts directory')
    parser.add_argument('--output', default=README_PATH, type=Path, help='Output README path')
    args = parser.parse_args()

    content = build_readme(args.dir)
    args.output.write_text(content, encoding='utf-8')
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
