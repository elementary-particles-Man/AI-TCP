#!/usr/bin/env python3
"""Generate a Mermaid flowchart from cli_logs/output.json."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

INPUT_PATH = Path("cli_logs/output.json")
OUTPUT_DIR = Path("cli_logs")


def _br(text: str) -> str:
    """Replace newlines with <br>."""
    return text.replace("\n", "<br>")


def build_flowchart(data: dict) -> str:
    """Return Mermaid flowchart code based on execution result."""
    status = data.get("execution_status", "error")
    message = _br(str(data.get("message", "")))
    details = data.get("details", {})

    lines = ["flowchart TD", "    start([start]) --> validate[validate]", "    validate --> dispatch[dispatch]", "    dispatch --> commit[commit]"]

    if status == "success":
        pr_name = _br(str(details.get("pr_name", "pr")))
        lines.append(f"    commit --> pr[pr生成]")
        lines.append(f"    pr --> complete[完了<br>{pr_name}]")
    else:
        lines.append(f"    commit --> error[{message}]")
    return "\n".join(lines)


def main() -> None:
    if not INPUT_PATH.exists():
        raise SystemExit(f"Input file not found: {INPUT_PATH}")
    data = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    chart = build_flowchart(data)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    out_path = OUTPUT_DIR / f"{timestamp}.mmd.md"
    out_path.write_text(f"```mermaid\n{chart}\n```\n", encoding="utf-8")
    print(f"Mermaid saved to {out_path}")


if __name__ == "__main__":
    main()
