#!/usr/bin/env python3
"""Convert TaskValidation.txt log to Markdown and archive."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def parse_log(log_path: Path) -> str:
    """Return Markdown-formatted string from log file."""
    text = log_path.read_text(encoding="utf-8")
    return "# Task Validation Log\n\n```\n" + text.rstrip() + "\n```\n"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="TaskValidation.txt -> Markdown")
    parser.add_argument("log", type=Path, help="full path to TaskValidation.txt")
    args = parser.parse_args(argv)

    if not args.log.exists():
        raise SystemExit(f"Log file not found: {args.log}")

    markdown = parse_log(args.log) + "\n[Task Completed]\n"

    archive_dir = Path("cli_archives")
    archive_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = archive_dir / f"TaskValidation_{timestamp}.md"
    out_path.write_text(markdown, encoding="utf-8")
    print(f"Markdown saved to {out_path}")


if __name__ == "__main__":
    main()
