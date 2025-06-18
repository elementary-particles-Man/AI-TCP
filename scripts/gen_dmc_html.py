#!/usr/bin/env python3
"""Generate HTML from AI-TCP DMC trace YAML.

This script reads a YAML trace file for a Direct Mental Care (DMC) session
and converts it into a structured HTML document.  The output file name can be
derived automatically from the session ID embedded in the YAML.  Basic
validation of required YAML keys is performed to avoid malformed input.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import webbrowser
from html import escape

import yaml

DEFAULT_INPUT = "structured_yaml/validated_yaml/ai_tcp_dmc_trace.yaml"
DEFAULT_OUTPUT = None
DEFAULT_TEMPLATE = "html_templates/dmc_base_template.html"


def load_yaml(path: Path) -> dict:
    """Load YAML safely and ensure the result is a mapping."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("YAML root must be a mapping")
    return data


def validate_yaml(data: dict) -> dict:
    """Validate required keys for session_trace and packets."""
    if "session_trace" not in data or not isinstance(data["session_trace"], dict):
        raise ValueError("missing 'session_trace'")
    session = data["session_trace"]
    if "session_id" not in session:
        raise ValueError("'session_id' is required in session_trace")
    if "phases" not in session or not isinstance(session["phases"], list):
        raise ValueError("'phases' list is required in session_trace")

    for ph in session["phases"]:
        if "packets" not in ph or not isinstance(ph["packets"], list):
            raise ValueError(f"phase {ph.get('id')} missing packets list")
        for pkt in ph["packets"]:
            for key in ("packet_id", "intent", "trace_link"):
                if key not in pkt:
                    raise ValueError(f"packet missing '{key}' in phase {ph.get('id')}")

    # tcp_packet_trace is optional but if present should have 'trace'
    tcp = data.get("tcp_packet_trace")
    if tcp and (not isinstance(tcp, dict) or "trace" not in tcp):
        raise ValueError("invalid 'tcp_packet_trace' format")
    return data


def parse_yaml_trace(yaml_data: dict):
    """Extract session header and phases."""
    header = yaml_data.get("meta") or yaml_data["session_trace"].get("session_id")
    phases = yaml_data["session_trace"].get("phases", [])
    tcp_trace = yaml_data.get("tcp_packet_trace")
    return header, phases, tcp_trace


def generate_body_html(header, phases, tcp_trace) -> str:
    parts: list[str] = []
    session_title = header.get("title") if isinstance(header, dict) else None
    session_id = header.get("session_id") if isinstance(header, dict) else header

    parts.append("<h1>DMCセッション トレース</h1>")
    if session_title:
        parts.append(f"<h2>{escape(session_title)}</h2>")
    if session_id:
        parts.append(f"<h3>Session ID: {escape(session_id)}</h3>")

    for ph in phases:
        parts.append("<section>")
        parts.append(f"<h2>{escape(ph.get('name', ''))}</h2>")
        for pkt in ph.get("packets", []):
            parts.append("<article>")
            parts.append(f"<h3>{escape(pkt.get('packet_id'))}</h3>")
            parts.append("<ul>")
            parts.append(f"<li><strong>Intent:</strong> {escape(pkt.get('intent', ''))}</li>")
            trace = pkt.get("trace_link")
            if trace:
                parts.append(f"<li><strong>Trace:</strong> {escape(trace)}</li>")
            parts.append("</ul>")
            parts.append("</article>")
        parts.append("</section>")

    if tcp_trace:
        parts.append("<section>")
        parts.append("<h2>TCP Packet Trace</h2>")
        for entry in tcp_trace.get("trace", []):
            parts.append("<article>")
            phase = entry.get("phase", "")
            parts.append(f"<h3>{escape(phase)}</h3>")
            packet = entry.get("packet", {})
            header_data = packet.get("header", {})
            payload = packet.get("payload", {})
            if header_data:
                parts.append("<details><summary>Header</summary><pre>")
                parts.append(escape(yaml.dump(header_data, allow_unicode=True)))
                parts.append("</pre></details>")
            if payload:
                parts.append("<details><summary>Payload</summary>")
                parts.append(format_payload(payload))
                parts.append("</details>")
            parts.append("</article>")
        parts.append("</section>")

    return "\n".join(parts)


def format_payload(payload) -> str:
    """Recursively format payload dict or list as HTML."""
    if isinstance(payload, dict):
        items = [f"<li><strong>{escape(k)}:</strong> {format_payload(v)}</li>" for k, v in payload.items()]
        return "<ul>" + "".join(items) + "</ul>"
    if isinstance(payload, list):
        items = [f"<li>{format_payload(v)}</li>" for v in payload]
        return "<ul>" + "".join(items) + "</ul>"
    return escape(str(payload))


def apply_template(body_html: str, template_path: Path, session_id: str) -> str:
    if template_path.is_file():
        template = template_path.read_text(encoding="utf-8")
    else:
        template = "<html><body>{{ content }}</body></html>"

    html = template
    html = html.replace("{{ session_id }}", escape(session_id))
    html = html.replace("{{ content }}", body_html)
    return html


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate HTML from DMC trace YAML")
    parser.add_argument("--input", "-i", default=DEFAULT_INPUT, help="YAML input path")
    parser.add_argument("--output", "-o", help="HTML output path")
    parser.add_argument("--template", "-t", default=DEFAULT_TEMPLATE, help="HTML template path")
    parser.add_argument("--force", action="store_true", help="overwrite existing output")
    parser.add_argument("--open", action="store_true", help="open generated HTML in browser")
    return parser.parse_args()


def extract_date(session_id: str) -> str:
    match = re.search(r"(\d{8})", session_id)
    return match.group(1) if match else session_id


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    template_path = Path(args.template)

    data = validate_yaml(load_yaml(input_path))
    header, phases, tcp_trace = parse_yaml_trace(data)

    session_id = header.get("session_id") if isinstance(header, dict) else header

    output_path: Path
    if args.output:
        output_path = Path(args.output)
    else:
        date_part = extract_date(str(session_id))
        output_path = Path("docs/generated") / f"DMC_{date_part}.html"

    if output_path.exists() and not args.force:
        raise FileExistsError(f"{output_path} already exists. Use --force to overwrite")

    body_html = generate_body_html(header, phases, tcp_trace)
    final_html = apply_template(body_html, template_path, str(session_id))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_html, encoding="utf-8")
    print(f"[OK] HTML出力完了: {output_path}")

    if args.open:
        webbrowser.open(output_path.resolve().as_uri())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
