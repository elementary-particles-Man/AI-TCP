import argparse
import re
from pathlib import Path

RFC_DIR = Path('docs/rfc_drafts')
README_PATH = RFC_DIR / 'README.md'


def extract_info(path: Path, max_lines: int = 3) -> tuple[str, str, str]:
    """Return (filename, title, summary) for the given RFC markdown file."""
    lines = path.read_text(encoding='utf-8').splitlines()
    title = ''
    summary_lines: list[str] = []
    heading_pattern = re.compile(r'^##\s+')
    for i, line in enumerate(lines):
        if line.startswith('# RFC'):
            title = line.strip('# ').strip()
        if re.match(r'^##\s+1\.', line):
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            while j < len(lines) and len(summary_lines) < max_lines and not heading_pattern.match(lines[j]):
                if lines[j].strip():
                    summary_lines.append(lines[j].strip())
                j += 1
            break
    summary = ' '.join(summary_lines)
    return path.name, title, summary


def build_readme(rfc_dir: Path) -> str:
    rfc_files = sorted(rfc_dir.glob('[0-9][0-9][0-9]_*.md'), key=lambda p: p.name)
    lines = ['# \U0001F4D1 AI-TCP RFC Index', '', 'Drafts', '']
    for file in rfc_files:
        _, _, summary = extract_info(file)
        lines.append(file.name)
        if summary:
            lines.append(summary)
        lines.append('')
    return '\n'.join(lines).rstrip() + '\n'


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate RFC README index')
    parser.add_argument('--dir', default=RFC_DIR, type=Path, help='RFC drafts directory')
    parser.add_argument('--output', default=README_PATH, type=Path, help='Output README path')
    args = parser.parse_args()

    content = build_readme(args.dir)
    args.output.write_text(content, encoding='utf-8')
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
