#!/usr/bin/env python3
"""Generate HTML from AI-TCP DMC trace YAML."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import yaml

DEFAULT_INPUT = "structured_yaml/validated_yaml/ai_tcp_dmc_trace.yaml"
DEFAULT_OUTPUT = "docs/generated/DMC_20250618.html"
DEFAULT_TEMPLATE = "html_templates/dmc_base_template.html"


def parse_yaml_trace(yaml_data):
    """Extract header and phases information from YAML."""
    header = yaml_data.get("meta") or yaml_data.get("session_trace", {}).get("session_id")
    phases = yaml_data.get("session_trace", {}).get("phases")
    return header, phases


def generate_body_html(header, phases):
    parts = []
    parts.append("<h1>DMCセッション トレース</h1>")
    if isinstance(header, dict):
        parts.append(f"<h2>{header.get('title', 'No Title')}</h2>")
    else:
        parts.append(f"<h2>Session ID: {header}</h2>")
    if phases:
        for phase in phases:
            parts.append(f"<h3>フェーズ: {phase.get('name')}</h3>")
            for pkt in phase.get('packets', []):
                parts.append("<div style='margin-left:20px;'>")
                parts.append(f"<p><strong>ID:</strong> {pkt.get('packet_id')}</p>")
                parts.append(f"<p><strong>意図:</strong> {pkt.get('intent')}</p>")
                parts.append(f"<p><strong>トレースリンク:</strong> {pkt.get('trace_link')}</p>")
                parts.append("</div>")
    return "\n".join(parts)


def apply_template(body_html: str, template_path: Path) -> str:
    if template_path.is_file():
        template = template_path.read_text(encoding="utf-8")
        return template.replace("{{body}}", body_html)
    return f"<html><body>{body_html}</body></html>"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate HTML from DMC trace YAML")
    parser.add_argument("--input", "-i", default=DEFAULT_INPUT, help="YAML input path")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="HTML output path")
    parser.add_argument("--template", "-t", default=DEFAULT_TEMPLATE, help="HTML template path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    template_path = Path(args.template)

    yaml_data = yaml.safe_load(input_path.read_text(encoding="utf-8"))
    header, phases = parse_yaml_trace(yaml_data)
    body_html = generate_body_html(header, phases)
    final_html = apply_template(body_html, template_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_html, encoding="utf-8")
    print(f"[OK] HTML出力完了: {output_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
