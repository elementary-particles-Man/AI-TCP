#!/usr/bin/env python3
"""Simple YAML semantics checker for AI-TCP intent files.

This script validates that an intent_*.yaml file follows the expected
structure. It ensures that each component defines ``id``, ``type`` and
``label`` fields and that all connection ``from``/``to`` references point
to existing component IDs.

Usage:
    python check_semantics.py path/to/intent_file.yaml

The script prints error messages with line numbers on failure or
"構文チェック成功" on success.

Requirements:
    PyYAML==5.3.1
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Set

import yaml


class LineLoader(yaml.SafeLoader):
    """YAML loader that attaches line numbers to mappings."""


def construct_mapping(loader: LineLoader, node: yaml.nodes.MappingNode, deep: bool = False) -> Dict[str, Any]:
    mapping = yaml.SafeLoader.construct_mapping(loader, node, deep=deep)
    mapping['__line__'] = node.start_mark.line + 1
    return mapping


LineLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
)


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open('r', encoding='utf-8') as f:
        return yaml.load(f, Loader=LineLoader)


def validate_components(data: Dict[str, Any], errors: List[str]) -> Set[str]:
    comps = data.get('components')
    comp_ids: Set[str] = set()
    if comps is None:
        return comp_ids
    if not isinstance(comps, list):
        line = data.get('__line__', '?')
        errors.append(f"Line {line}: 'components' should be a list")
        return comp_ids

    for comp in comps:
        if not isinstance(comp, dict):
            line = comp.get('__line__', '?') if isinstance(comp, dict) else data.get('__line__', '?')
            errors.append(f"Line {line}: component should be a mapping")
            continue
        line = comp.get('__line__', '?')
        for key in ['id', 'type', 'label']:
            if key not in comp:
                errors.append(f"Line {line}: component missing '{key}'")
        cid = comp.get('id')
        if isinstance(cid, str):
            comp_ids.add(cid)
    return comp_ids


def validate_connections(data: Dict[str, Any], comp_ids: Set[str], errors: List[str]) -> None:
    conns = data.get('connections')
    if conns is None:
        return
    if not isinstance(conns, list):
        line = data.get('__line__', '?')
        errors.append(f"Line {line}: 'connections' should be a list")
        return

    for conn in conns:
        if not isinstance(conn, dict):
            line = conn.get('__line__', '?') if isinstance(conn, dict) else data.get('__line__', '?')
            errors.append(f"Line {line}: connection should be a mapping")
            continue
        line = conn.get('__line__', '?')
        from_id = conn.get('from')
        to_id = conn.get('to')
        if from_id is None:
            errors.append(f"Line {line}: connection missing 'from'")
        if to_id is None:
            errors.append(f"Line {line}: connection missing 'to'")
        if isinstance(from_id, str) and from_id not in comp_ids:
            errors.append(f"Line {line}: undefined component id '{from_id}' in 'from'")
        if isinstance(to_id, str) and to_id not in comp_ids:
            errors.append(f"Line {line}: undefined component id '{to_id}' in 'to'")


def validate_file(path: Path) -> List[str]:
    try:
        data = load_yaml(path)
    except Exception as exc:  # YAML parse error
        return [f"YAML parse error: {exc}"]

    errors: List[str] = []
    if not isinstance(data, dict):
        line = data.get('__line__', '?') if isinstance(data, dict) else 1
        errors.append(f"Line {line}: root should be a mapping")
        return errors

    comp_ids = validate_components(data, errors)
    validate_connections(data, comp_ids, errors)
    return errors


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print('Usage: python check_semantics.py <path>', file=sys.stderr)
        return 1
    path = Path(argv[1])
    if not path.exists():
        print(f'File not found: {path}', file=sys.stderr)
        return 1

    errors = validate_file(path)
    if errors:
        for err in errors:
            print(err)
        return 1

    print('構文チェック成功')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
