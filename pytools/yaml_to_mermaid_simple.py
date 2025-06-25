#!/usr/bin/env python3
"""Generate Mermaid diagrams from YAML files without external dependencies."""
from __future__ import annotations

import argparse
from pathlib import Path


def _collect_lines(text: str) -> list[tuple[int, str]]:
    """Return (indent, label) pairs ignoring comments and blank lines."""
    pairs: list[tuple[int, str]] = []
    for line in text.splitlines():
        line = line.split('#', 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(' '))
        pairs.append((indent, line.strip()))
    return pairs


def _to_mermaid(pairs: list[tuple[int, str]]) -> str:
    lines = ["flowchart TD", "  root[\"root\"]"]
    stack: list[tuple[int, str]] = []
    counter = 0
    for indent, label in pairs:
        node_id = f"n{counter}"
        safe_label = label.replace('"', '\\"')
        lines.append(f"  {node_id}[\"{safe_label}\"]")
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = "root" if not stack else stack[-1][1]
        lines.append(f"  {parent} --> {node_id}")
        stack.append((indent, node_id))
        counter += 1
    return "\n".join(lines) + "\n"


def process_file(path: Path, out_dir: Path) -> None:
    text = path.read_text(encoding="utf-8")
    pairs = _collect_lines(text)
    mermaid = _to_mermaid(pairs)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{path.stem}.mmd"
    out_path.write_text(mermaid, encoding="utf-8")
    print(f"✅ {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert YAML to Mermaid diagram")
    parser.add_argument("yaml", type=Path, nargs="*", help="YAML files")
    parser.add_argument("-o", "--output", type=Path, default=Path("generated_mermaid"))
    args = parser.parse_args()

    paths = args.yaml or list(Path("structured_yaml").rglob("*.yaml"))
    for p in sorted(paths):
        process_file(p, args.output)


if __name__ == "__main__":
    main()
