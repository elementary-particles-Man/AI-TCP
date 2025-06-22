#!/usr/bin/env python3
"""Receive AI-TCP packets from the input/ directory.

This script watches `input/` for YAML files. When a file appears, it prints
its `graph_payload.graph_structure` and `reasoning_trace` contents, then moves
the file into `input/processed/` to mark it as handled.
"""
from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

try:
    import yaml
except Exception:  # pragma: no cover - dependency missing
    yaml = None

INPUT_DIR = Path('input')
PROCESSED_DIR = INPUT_DIR / 'processed'


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


def print_packet(name: str, graph: str | None, trace: list) -> None:
    print(f"[Receiving] {name}")
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


def handle_file(path: Path) -> None:
    data = load_yaml(path)
    graph = extract_graph(data)
    trace = extract_trace(data)
    print_packet(path.name, graph, trace)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    shutil.move(path, PROCESSED_DIR / path.name)


def watch(poll: float) -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Watching {INPUT_DIR}... Press Ctrl+C to stop.")
    seen = set()
    try:
        while True:
            for file in INPUT_DIR.glob('*.yaml'):
                if file in seen:
                    continue
                try:
                    handle_file(file)
                    seen.add(file)
                except Exception as exc:  # pragma: no cover - runtime errors
                    print(f"Error processing {file.name}: {exc}", file=sys.stderr)
            time.sleep(poll)
    except KeyboardInterrupt:  # pragma: no cover - interactive exit
        print("\nStopped")


def main() -> None:
    parser = argparse.ArgumentParser(description="Receive AI-TCP YAML packets")
    parser.add_argument('--poll', type=float, default=1.0, help='poll interval seconds')
    args = parser.parse_args()
    watch(args.poll)


if __name__ == '__main__':
    main()
