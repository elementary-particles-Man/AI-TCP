#!/usr/bin/env python3
"""Batch convert YAML reasoning traces to Mermaid and HTML.

This CLI searches for YAML files that contain a `reasoning_trace` array.
For each file it outputs two artifacts using the same basename:

- `generated_mermaid/<name>.mmd.md` – Obsidian-compatible Mermaid diagram
- `generated_html/<name>.html` – simple HTML table view

Use `--all` to process every `*.yaml` under `dmc_sessions/` or
`--file <path>` to convert a single file.
"""
from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path
from typing import Iterable, List, Optional

try:
    import yaml
except Exception:  # pragma: no cover - missing dependency
    yaml = None

MERMAID_DIR = Path("generated_mermaid")
HTML_DIR = Path("generated_html")
DEFAULT_SRC = Path("dmc_sessions")


def _load_yaml(path: Path) -> Optional[object]:
    if yaml is None:
        raise RuntimeError("PyYAML is required but not installed")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as exc:  # pragma: no cover - runtime errors
        print(f"[WARN] Failed to parse {path}: {exc}", file=sys.stderr)
        return None


def _find_reasoning_trace(obj: object) -> Optional[List[object]]:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'reasoning_trace' and isinstance(v, list):
                return v
            res = _find_reasoning_trace(v)
            if res is not None:
                return res
    elif isinstance(obj, list):
        for item in obj:
            res = _find_reasoning_trace(item)
            if res is not None:
                return res
    return None


def _validate_trace(trace: List[object]) -> bool:
    for step in trace:
        if not isinstance(step, dict):
            return False
        if 'input' not in step or 'output' not in step:
            return False
    return True


def _trace_to_mermaid(trace: List[dict]) -> str:
    lines = ['flowchart TD']
    for idx, step in enumerate(trace, 1):
        inp = html.escape(str(step.get('input', ''))).replace('\n', '<br>')
        out = html.escape(str(step.get('output', ''))).replace('\n', '<br>')
        label = f"{idx}: {inp} → {out}"
        node = f"n{idx}[\"{label}\"]"
        lines.append(f"  {node}")
        if idx > 1:
            lines.append(f"  n{idx-1} --> n{idx}")
    return '\n'.join(lines)


def _trace_to_html(trace: List[dict], title: str) -> str:
    rows = []
    for idx, step in enumerate(trace, 1):
        inp = html.escape(str(step.get('input', '')))
        out = html.escape(str(step.get('output', '')))
        rows.append(f"<tr><td>{idx}</td><td>{inp}</td><td>{out}</td></tr>")
    table = '\n'.join(rows)
    return f"""<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>{html.escape(title)}</title>
  <link rel='stylesheet' href='../html_templates/structured_index_style.css'>
</head>
<body>
<h1>{html.escape(title)}</h1>
<table border='1'>
<tr><th>Step</th><th>Input</th><th>Output</th></tr>
{table}
</table>
</body>
</html>"""


def _process_file(path: Path) -> None:
    data = _load_yaml(path)
    if data is None:
        return
    trace = _find_reasoning_trace(data)
    if trace is None:
        print(f"[SKIP] No reasoning_trace in {path}")
        return
    if not _validate_trace(trace):
        print(f"[SKIP] Invalid reasoning_trace format in {path}")
        return

    mermaid = _trace_to_mermaid(trace) + "\n"
    MERMAID_DIR.mkdir(parents=True, exist_ok=True)
    mmd_path = MERMAID_DIR / f"{path.stem}.mmd.md"
    mmd_path.write_text(mermaid, encoding='utf-8')

    html_doc = _trace_to_html(trace, path.stem)
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    html_path = HTML_DIR / f"{path.stem}.html"
    html_path.write_text(html_doc, encoding='utf-8')
    print(f"[OK] {path} -> {mmd_path}, {html_path}")


def _iter_yaml_files(directory: Path) -> Iterable[Path]:
    for p in sorted(directory.rglob('*.yaml')):
        if p.is_file():
            yield p


def main() -> None:
    parser = argparse.ArgumentParser(description='Convert reasoning_trace YAMLs')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--all', action='store_true', help='process all YAML files under dmc_sessions/')
    group.add_argument('--file', type=Path, help='single YAML file to process')
    args = parser.parse_args()

    if args.all:
        for path in _iter_yaml_files(DEFAULT_SRC):
            _process_file(path)
    else:
        _process_file(args.file)


if __name__ == '__main__':
    main()
