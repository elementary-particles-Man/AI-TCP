#!/usr/bin/env python3
"""Validate DMC YAML using JSON Schema.

This script reads a YAML file describing the Direct Mental Care system
and validates it against the AI-TCP packet schema. If validation
succeeds, the YAML is written to the validated directory. On failure,
an `.err` file with the validation error message is created next to the
expected output.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml
from jsonschema import Draft7Validator

INPUT = Path("docs/poc_design/direct_mental_care.yaml")
SCHEMA = Path("schemas/ai_tcp_packet.schema.yaml")
OUTPUT = Path("structured_yaml/validated_yaml/ai_tcp_dmc_trace.yaml")


def load_yaml(path: Path):
    """Load YAML and return the resulting object."""
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate(data: dict, schema: dict) -> None:
    """Validate data against schema, raising on first error."""
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    if errors:
        msgs = [f"{list(err.path)}: {err.message}" for err in errors]
        raise ValueError("\n".join(msgs))


def main() -> None:
    try:
        data = load_yaml(INPUT)
        schema = load_yaml(SCHEMA)
        validate(data, schema)
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(yaml.dump(data, allow_unicode=True), encoding="utf-8")
        print(f"[OK] validated and saved: {OUTPUT}")
    except Exception as exc:
        err_path = OUTPUT.with_suffix(".err")
        err_path.write_text(str(exc), encoding="utf-8")
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
