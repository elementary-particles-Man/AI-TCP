#!/usr/bin/env python3
"""Check consistency of RFC numbers in docs/rfc_drafts/*.md files.

This script verifies that the numeric prefix of each markdown filename
matches the RFC number mentioned near the top of the file.
"""
from __future__ import annotations

import re
from pathlib import Path

RFC_DIR = Path('docs/rfc_drafts')
MAX_LINES = 20
FILE_PATTERN = re.compile(r'^(\d{3})_.*\.md$')
RFC_PATTERN = re.compile(r'RFC\s*0*(\d+)\s*:')


def check_file(path: Path) -> str:
    """Return formatted result line for a single RFC file."""
    match = FILE_PATTERN.match(path.name)
    if not match:
        return ''
    file_num = match.group(1)
    lines = path.read_text(encoding='utf-8').splitlines()[:MAX_LINES]
    text = '\n'.join(lines)
    m = RFC_PATTERN.search(text)
    if m:
        rfc_num = m.group(1).zfill(3)
        if rfc_num == file_num:
            return f"\u2714 {path.name} \u2192 RFC{rfc_num} \u2705"
        return f"\u2716 {path.name} \u2192 RFC{rfc_num} \u274c（不一致）"
    return f"\u2716 {path.name} \u2192 RFC記載なし"


def main() -> None:
    for md_path in sorted(RFC_DIR.rglob('*.md')):
        result = check_file(md_path)
        if result:
            print(result)


if __name__ == '__main__':
    main()
