#!/usr/bin/env python3
"""Validate Mermaid code blocks in YAML files.

This script scans YAML files under `structured_yaml/` and `dmc_sessions/`
for `graph_payload.graph_structure` fields containing Mermaid code marked
with the `mmd:` prefix. It performs a very simple syntax sanity check and
reports results. When `--fix` is supplied, the Mermaid block is cleaned of
extra spaces and newlines and written back to the file.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - dependency might be missing
    yaml = None


MERMAID_KEYWORDS = ["flowchart", "graph", "-->", "---", "subgraph"]


def _find_mermaid_nodes(obj: object) -> list[tuple[dict, str, str]]:
    """Recursively search for graph_payload.graph_structure strings."""

    found: list[tuple[dict, str, str]] = []

    def _walk(node: object) -> None:
        if isinstance(node, dict):
            if "graph_payload" in node:
                gp = node.get("graph_payload")
                if isinstance(gp, dict) and "graph_structure" in gp:
                    gs = gp.get("graph_structure")
                    if isinstance(gs, str) and "mmd:" in gs:
                        found.append((gp, "graph_structure", gs))
            for v in node.values():
                _walk(v)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(obj)
    return found


def _clean_mermaid(code: str) -> str:
    lines = [ln.strip() for ln in code.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def _validate_mermaid(code: str) -> bool:
    code = code.strip()
    if not code:
        return False
    lines = code.splitlines()
    first = lines[0].strip() if lines else ""
    if not (first.startswith("flowchart") or first.startswith("graph")):
        return False
    if not any("-->" in ln or "---" in ln for ln in lines):
        return False
    if "subgraph" in code and code.count("end") < code.count("subgraph"):
        return False
    return True


def _find_mmd_line(text_lines: list[str]) -> int:
    for idx, line in enumerate(text_lines, start=1):
        if "mmd:" in line:
            return idx
    return 0


def process_file(path: Path, fix: bool = False) -> int:
    if yaml is None:
        print(f"PyYAML is required but not installed: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(text)
    except Exception as exc:  # pragma: no cover - parse errors are reported
        print(f"YAML parse error in {path}: {exc}")
        return 1

    blocks = _find_mermaid_nodes(data)
    if not blocks:
        return 0

    lines = text.splitlines()
    line_no = _find_mmd_line(lines)

    exit_status = 0
    for parent, key, raw in blocks:
        mermaid = raw.split("mmd:", 1)[1]
        cleaned = _clean_mermaid(mermaid)
        valid = _validate_mermaid(cleaned)
        if valid:
            print(f"✅ Mermaid valid: {path.name} (line {line_no})")
        else:
            snippet = cleaned.splitlines()[0] if cleaned else ""
            print(f"❌ Mermaid syntax error: {path.name} (line {line_no}: {snippet})")
            exit_status = 1
        if fix:
            parent[key] = f"mmd:{cleaned}"

    if fix:
        path.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return exit_status


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Mermaid blocks in YAML files")
    parser.add_argument("--fix", action="store_true", help="auto-fix Mermaid formatting")
    args = parser.parse_args()

    targets = list(Path("structured_yaml").rglob("*.yaml")) + list(Path("dmc_sessions").rglob("*.yaml"))
    exit_code = 0
    for file in sorted(targets):
        if process_file(file, fix=args.fix) != 0:
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
