#!/usr/bin/env python3
"""Verify structural alignment between Japanese and English DMC summaries."""
from __future__ import annotations

import re
import sys
from pathlib import Path

JP_FILE = Path("dmc_sessions/summary/dmc_session_20250618_narrative_summary.md")
EN_FILE = Path("dmc_sessions/summary/dmc_session_20250618_narrative_summary_en.md")

PHASE_RE = re.compile(r"^###\s*\*\*?Phase\s*(\d+)", re.IGNORECASE)


def parse_phases(path: Path) -> list[tuple[int, str]]:
    """Return list of (phase_number, content) tuples from Markdown."""
    if not path.exists():
        print(f"[ERROR] File not found: {path}", file=sys.stderr)
        sys.exit(1)

    phases: list[tuple[int, str]] = []
    current_num: int | None = None
    buffer: list[str] = []

    lines = path.read_text(encoding="utf-8").splitlines()

    for line in lines + [""]:
        match = PHASE_RE.match(line.strip())
        if match:
            if current_num is not None:
                phases.append((current_num, "\n".join(buffer).strip()))
            current_num = int(match.group(1))
            buffer = []
        else:
            if current_num is not None:
                buffer.append(line)

    if current_num is not None:
        phases.append((current_num, "\n".join(buffer).strip()))

    return phases


def main() -> None:
    jp_phases = parse_phases(JP_FILE)
    en_phases = parse_phases(EN_FILE)

    jp_nums = [num for num, _ in jp_phases]
    en_nums = [num for num, _ in en_phases]
    max_len = max(len(jp_nums), len(en_nums))

    for idx in range(max_len):
        jp_num = jp_nums[idx] if idx < len(jp_nums) else None
        en_num = en_nums[idx] if idx < len(en_nums) else None

        if jp_num != en_num:
            phase = jp_num if jp_num is not None else en_num
            print(f"\u274c Phase {phase}: Title mismatch")
            continue

        jp_content = jp_phases[idx][1] if idx < len(jp_phases) else ""
        en_content = en_phases[idx][1] if idx < len(en_phases) else ""
        msg = []
        if not jp_content:
            msg.append("Japanese content missing")
        if not en_content:
            msg.append("English content missing")

        if msg:
            print(f"\u274c Phase {jp_num}: {' & '.join(msg)}")
        else:
            print(f"\u2705 Phase {jp_num}: OK")


if __name__ == "__main__":
    main()
