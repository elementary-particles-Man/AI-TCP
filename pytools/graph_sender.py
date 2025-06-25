#!/usr/bin/env python3
"""Send an AI-TCP packet by writing it to the output/ directory.

This CLI reads a YAML file containing `graph_payload` and `reasoning_trace`
fields, prints their contents, and copies the file into `output/` as a
simulation of sending it to another host.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

try:
    import yaml
except Exception:  # pragma: no cover - dependency missing
    yaml = None


def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML is required but not installed: %s" % path)
    with path.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def extract_graph(data: dict) -> str | None:
    gp = data.get('graph_payload', {})
    gs = None
    if isinstance(gp, dict):
        gs = gp.get('graph_structure')
    if isinstance(gs, str) and 'mmd:' in gs:
        return gs.split('mmd:', 1)[1].strip()
    return None


def extract_trace(data: dict) -> list:
    trace = data.get('reasoning_trace')
    return trace if isinstance(trace, list) else []


def print_packet(graph: str | None, trace: list) -> None:
    if graph:
        print("Graph structure:")
        print(graph)
    else:
        print("Graph structure: (none)")
    for idx, step in enumerate(trace, 1):
        if isinstance(step, dict):
            msg = step.get('step') or step.get('input') or step.get('output') or step.get('message')
            msg = str(msg) if msg is not None else str(step)
        else:
            msg = str(step)
        print(f'Trace step {idx}: "{msg}"')


def send_file(path: Path, output_dir: Path = Path('output')) -> None:
    data = load_yaml(path)
    graph = extract_graph(data)
    trace = extract_trace(data)

    print(f"[Sending] {path.name}")
    print_packet(graph, trace)

    output_dir.mkdir(parents=True, exist_ok=True)
    dest = output_dir / path.name
    shutil.copy(path, dest)
    print(f"File written to {dest}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Send AI-TCP YAML packet")
    parser.add_argument('yaml_file', type=Path, help='YAML packet path')
    args = parser.parse_args()

    if not args.yaml_file.is_file():
        print(f"File not found: {args.yaml_file}", file=sys.stderr)
        sys.exit(1)

    try:
        send_file(args.yaml_file)
    except Exception as exc:  # pragma: no cover - runtime errors
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
