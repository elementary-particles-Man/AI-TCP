#!/usr/bin/env python3
"""Validate structured_yaml/dmc_mental_001.yaml against schema.json.

This script loads the YAML file and validates its structure using a
JSON Schema definition. It prints each validation error with the
corresponding field path and reason. Designed for Python 3.7.
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

SCHEMA_PATH = Path("schema.json")
YAML_PATH = Path("structured_yaml/dmc_mental_001.yaml")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def main() -> None:
    if not SCHEMA_PATH.is_file():
        print(f"Schema file not found: {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(1)
    if not YAML_PATH.is_file():
        print(f"YAML file not found: {YAML_PATH}", file=sys.stderr)
        sys.exit(1)

    schema = load_json(SCHEMA_PATH)
    data = load_yaml(YAML_PATH)

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

