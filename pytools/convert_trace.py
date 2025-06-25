#!/usr/bin/env python3
"""Convert a reasoning_trace YAML file to HTML and Mermaid."""
from __future__ import annotations

import argparse
import html
from pathlib import Path

import yaml

HTML_DIR = Path("generated_html")
MERMAID_DIR = Path("generated_mermaid")


def _build_html(trace: list[dict], title: str) -> str:
    headers = sorted({k for item in trace if isinstance(item, dict) for k in item})
    header_row = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    lines = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        f"  <title>{html.escape(title)}</title>",
        "  <link rel=\"stylesheet\" href=\"../html_templates/structured_index_style.css\">",
        "  <style>table{border-collapse:collapse;}th,td{border:1px solid #ccc;padding:0.3em 0.6em;}</style>",
        "</head>",
        "<body>",
        f"  <h1>{html.escape(title)}</h1>",
        "  <table>",
        f"    <thead><tr>{header_row}</tr></thead>",
        "    <tbody>",
    ]
    for item in trace:
        row = []
        for h in headers:
            val = item.get(h, "")
            row.append(f"<td>{html.escape(str(val))}</td>")
        lines.append("      <tr>" + "".join(row) + "</tr>")
    lines.extend([
        "    </tbody>",
        "  </table>",
        "</body>",
        "</html>",
    ])
    return "\n".join(lines)


def _sanitize(text: str) -> str:
    return text.replace("\n", "<br>").replace('"', '\\"')


def _build_mermaid(trace: list[dict]) -> str:
    lines = ["```mermaid", "flowchart TD"]
    for i, item in enumerate(trace, start=1):
        step = item.get("step", i)
        thought = item.get("thought") or item.get("input") or ""
        action = item.get("action") or item.get("output") or ""
        parts = [f"{step}:"]
        if thought:
            parts.append(_sanitize(str(thought)))
        if action:
            if thought:
                parts.append(_sanitize(str(action)))
            else:
                parts[-1] += " " + _sanitize(str(action))
        label = "<br>".join(parts)
        lines.append(f"  s{i}[\"{label}\"]")
    for i in range(1, len(trace)):
        lines.append(f"  s{i} --> s{i+1}")
    lines.append("```")
    return "\n".join(lines)


def convert_trace(yaml_path: Path) -> None:
    data = yaml.safe_load(Path(yaml_path).read_text(encoding="utf-8"))
    trace = data.get("reasoning_trace")
    if not isinstance(trace, list):
        raise ValueError("reasoning_trace list not found")
    title = f"{Path(yaml_path).name} reasoning trace"
    html_text = _build_html(trace, title)
    mermaid_text = _build_mermaid(trace)

    HTML_DIR.mkdir(parents=True, exist_ok=True)
    MERMAID_DIR.mkdir(parents=True, exist_ok=True)

    html_path = HTML_DIR / f"{Path(yaml_path).stem}_trace.html"
    mmd_path = MERMAID_DIR / f"{Path(yaml_path).stem}_trace.mmd.md"

    html_path.write_text(html_text, encoding="utf-8")
    mmd_path.write_text(mermaid_text + "\n", encoding="utf-8")
    print(f"✅ {html_path}")
    print(f"✅ {mmd_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert reasoning_trace to HTML and Mermaid")
    parser.add_argument("yaml", type=Path, help="YAML file containing reasoning_trace")
    args = parser.parse_args()
    convert_trace(args.yaml)


if __name__ == "__main__":
    main()
