#!/usr/bin/env python3
"""YAML structure integrity checker.

This script validates all YAML files under structured_yaml/validated_yaml/
against master_schema_v1.yaml. It detects:
- undefined keys
- type mismatches
- missing required keys
The results are written to validation_logs/summary.log.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

SCHEMA_PATH = Path("structured_yaml/master_schema_v1.yaml")
TARGET_DIR = Path("structured_yaml/validated_yaml")
LOG_DIR = Path("validation_logs")
LOG_FILE = LOG_DIR / "summary.log"


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_node(data: Any, schema: Any, path: str, errors: List[str]) -> None:
    """Recursively validate data against schema."""
    if isinstance(schema, dict):
        if not isinstance(data, dict):
            errors.append(f"{path}: expected mapping")
            return
        # check required keys and validate recursively
        for key, subschema in schema.items():
            subpath = f"{path}.{key}" if path else key
            if key not in data:
                errors.append(f"{subpath}: missing required key")
            else:
                validate_node(data[key], subschema, subpath, errors)
        # check for undefined keys
        for key in data.keys():
            if key not in schema:
                subpath = f"{path}.{key}" if path else key
                errors.append(f"{subpath}: undefined key")
    elif isinstance(schema, list):
        if not isinstance(data, list):
            errors.append(f"{path}: expected list")
            return
        if schema:
            item_schema = schema[0]
            for idx, item in enumerate(data):
                subpath = f"{path}[{idx}]"
                validate_node(item, item_schema, subpath, errors)
    else:  # assume scalar expected
        if isinstance(data, (dict, list)):
            errors.append(f"{path}: expected scalar value")


def validate_file(path: Path, schema: Dict[str, Any]) -> List[str]:
    try:
        data = load_yaml(path)
    except Exception as exc:  # YAML syntax error
        return [f"YAML parse error: {exc}"]

    errors: List[str] = []
    validate_node(data, schema, "", errors)
    return errors


def main() -> None:
    schema_data = load_yaml(SCHEMA_PATH)
    if not isinstance(schema_data, dict) or "structure" not in schema_data:
        print(f"Invalid schema: {SCHEMA_PATH}")
        sys.exit(1)
    schema = schema_data["structure"]

    LOG_DIR.mkdir(exist_ok=True)
    with LOG_FILE.open("w", encoding="utf-8") as log:
        for yaml_file in sorted(TARGET_DIR.glob("*.yaml")):
            errors = validate_file(yaml_file, schema)
            if errors:
                log.write(f"{yaml_file.name}: INVALID\n")
                for err in errors:
                    log.write(f"  - {err}\n")
            else:
                log.write(f"{yaml_file.name}: OK\n")

    print(f"Validation results written to {LOG_FILE}")


if __name__ == "__main__":
    main()
