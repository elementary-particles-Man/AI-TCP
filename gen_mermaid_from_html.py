#!/usr/bin/env python3
"""Generate Mermaid Graph Payload from intent HTML files.

This script reads an HTML file like ``intent_002_output.html`` and
extracts the Intent, Source, Process and Response descriptions.
The information is converted into a single-line Mermaid ``flowchart TD``
string using ``<br>`` as newline markers. The output is saved as
``payload_XXX.mmd.md`` where ``XXX`` comes from the intent ID.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict

from bs4 import BeautifulSoup


def _parse_html(path: Path) -> Dict[str, str]:
    """Return extracted fields from the HTML."""
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    text = soup.get_text("\n")

    patterns = {
        "intent": r"Intent\s*[:：]\s*(.+)",
        "source": r"Source\s*[:：]\s*(.+)",
        "process": r"Process\s*[:：]\s*(.+)",
        "response": r"Response\s*[:：]\s*(.+)",
    }

    fields: Dict[str, str] = {}
    for key, pat in patterns.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            fields[key] = m.group(1).strip()

    labels = [
        ("intent", "Intent"),
        ("source", "Source"),
        ("process", "Process"),
        ("response", "Response"),
    ]
    for key, label in labels:
        if key in fields:
            continue
        th = soup.find(["th", "dt", "strong"], string=re.compile(label, re.I))
        if th:
            td = th.find_next(["td", "dd"])
            if td:
                fields[key] = td.get_text(strip=True)

    return fields


def _build_mermaid(fields: Dict[str, str]) -> str:
    intent = fields.get("intent", "")
    source = fields.get("source", "")
    process = fields.get("process", "")
    response = fields.get("response", "")

    if source and source not in process:
        process = f"{process} {source}".strip()

    lines = [
        "mmd:flowchart TD",
        f'A["Input: {intent}"] --> B["Process: {process}"]',
        f'B --> C["Response: {response}"]',
    ]
    return "<br>".join(lines)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate Mermaid from HTML")
    parser.add_argument("html", type=Path, help="intent HTML file")
    parser.add_argument("-o", "--output", type=Path, help="output file")
    args = parser.parse_args(argv)

    html_path = args.html
    if args.output:
        out_path = args.output
    else:
        m = re.search(r"(\d+)", html_path.stem)
        suffix = m.group(1) if m else html_path.stem
        out_path = html_path.with_name(f"payload_{suffix}.mmd.md")

    fields = _parse_html(html_path)
    mermaid = _build_mermaid(fields)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(mermaid + "\n", encoding="utf-8")
    print(f"✅ Mermaid saved to {out_path}")


if __name__ == "__main__":
    main()
