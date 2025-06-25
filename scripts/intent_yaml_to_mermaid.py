#!/usr/bin/env python3
"""Convert AI-TCP intent YAML to a Mermaid flowchart.

This utility reads an intent_XXX.yaml file and outputs
`intent_XXX.mmd.md` containing a Mermaid ``flowchart TD`` graph
built from the ``components`` and ``connections`` sections.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, List

import yaml


def _load_yaml(path: Path) -> Dict[str, Any]:
    """Load YAML file and ensure it is a mapping."""
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # pragma: no cover - runtime parsing
        raise SystemExit(f"Failed to parse YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("YAML root must be a mapping")
    return data


def _get_label(component: Dict[str, Any]) -> str:
    """Return label from component using label/name/title or id."""
    for key in ("label", "name", "title"):
        if key in component and component[key] is not None:
            return str(component[key])
    return str(component.get("id", ""))


def build_mermaid(data: Dict[str, Any]) -> str:
    """Generate Mermaid flowchart code from intent data."""
    comps: List[Dict[str, Any]] = data.get("components") or []
    conns: List[Dict[str, Any]] = data.get("connections") or []

    lines = ["flowchart TD"]

    for comp in comps:
        cid = str(comp.get("id", "")).strip()
        if not cid:
            continue
        label = _get_label(comp)
        ctype = str(comp.get("type", "")).strip()
        lines.append(f"    {cid}[\"{label}\"]:::{ctype}")

    lines.append("")

    for conn in conns:
        src = conn.get("from")
        dst = conn.get("to")
        if not src or not dst:
            continue
        label = str(conn.get("label", ""))
        lines.append(f"    {src} -->|{label}| {dst}")

    lines.extend(
        [
            "",
            "    classDef source fill:#f9f,stroke:#333,stroke-width:1px",
            "    classDef process fill:#bbf,stroke:#333,stroke-width:1px",
            "    classDef response fill:#bfb,stroke:#333,stroke-width:1px",
            "    classDef log fill:#ffb,stroke:#333,stroke-width:1px",
            "",
        ]
    )

    for comp in comps:
        cid = str(comp.get("id", "")).strip()
        ctype = str(comp.get("type", "")).strip()
        if cid and ctype:
            lines.append(f"    class {cid} {ctype}")

    return "\n".join(lines) + "\n"


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="intent YAML -> Mermaid")
    parser.add_argument("yaml", type=Path, help="path to intent_XYZ.yaml")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        help="output .mmd.md path (defaults to same name)",
    )
    args = parser.parse_args(argv)

    yaml_path: Path = args.yaml
    out_path: Path = args.output if args.output else yaml_path.with_suffix(".mmd.md")

    data = _load_yaml(yaml_path)
    mermaid = build_mermaid(data)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(f"```mermaid\n{mermaid}```\n", encoding="utf-8")
    print(f"✅ Mermaid saved to {out_path}")


if __name__ == "__main__":
    main()
