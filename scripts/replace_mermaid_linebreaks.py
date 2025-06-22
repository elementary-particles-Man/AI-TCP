#!/usr/bin/env python3
"""Replace newlines in Mermaid code blocks with <br>.

This script scans all Markdown files under ``docs/rfc_drafts``. For any fenced
code block whose info string begins with ``mmd:``, the newline characters within
that block are replaced with ``<br>``. A ``.bak`` backup of each modified file is
saved alongside the original.
"""
from __future__ import annotations

import re
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET_DIR = ROOT / "docs" / "rfc_drafts"

FENCE_RE = re.compile(r"^(\s*)(```+|~~~+)(.*)$")


def process_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    result: list[str] = []
    block: list[str] | None = None
    fence = ""
    replace = False

    for line in lines:
        m = FENCE_RE.match(line)
        if block is None:
            if m:
                block = [line]
                fence = m.group(2)
                replace = m.group(3).strip().startswith("mmd:")
            else:
                result.append(line)
        else:
            block.append(line)
            if line.strip() == fence:
                if replace:
                    body = block[1:-1]
                    joined = "<br>".join(body)
                    result.extend([block[0], joined, block[-1]])
                else:
                    result.extend(block)
                block = None
                fence = ""
                replace = False

    if block is not None:  # unterminated block
        result.extend(block)

    new_text = "\n".join(result) + "\n"
    if new_text != text:
        bak_path = path.with_suffix(path.suffix + ".bak")
        shutil.copyfile(path, bak_path)
        path.write_text(new_text, encoding="utf-8")


def main() -> None:
    for md in TARGET_DIR.rglob("*.md"):
        if md.is_file():
            process_file(md)


if __name__ == "__main__":
    main()
