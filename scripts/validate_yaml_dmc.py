#!/usr/bin/env python3
"""Validate a YAML file against a JSON Schema.

This script loads a YAML file and validates its structure using a
JSON Schema definition. It prints each validation error with the
corresponding field path and reason.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - library missing
    sys.exit("PyYAML is required: pip install pyyaml")

try:
    from jsonschema import Draft7Validator
except ImportError as exc:  # pragma: no cover - library missing
    sys.exit("jsonschema is required: pip install jsonschema")


def load_json(path: Path):
    """Load JSON from a file."""
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_yaml(path: Path):
    """Load YAML from a file."""
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def main() -> None:
    """Main validation logic."""
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <yaml_file> [schema_file]", file=sys.stderr)
        sys.exit(1)

    yaml_path = Path(sys.argv[1])
    if not yaml_path.is_file():
        print(f"YAML file not found: {yaml_path}", file=sys.stderr)
        sys.exit(1)

    # If schema is provided, use it. Otherwise, look for schema.json in the same dir.
    if len(sys.argv) > 2:
        schema_path = Path(sys.argv[2])
    else:
        schema_path = yaml_path.parent / "schema.json"

    if not schema_path.is_file():
        print(f"Schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(1)

    schema = load_json(schema_path)
    data = load_yaml(yaml_path)

    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    if errors:
        for err in errors:
            path = ".".join(str(p) for p in err.path)
            path = path or "<root>"
            print(f"{path}: {err.message}")
        sys.exit(1)

    print("YAML conforms to schema.")


if __name__ == "__main__":
    main()