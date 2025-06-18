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
from datetime import datetime

import yaml

DEFAULT_INPUT = "docs/poc_design/direct_mental_care.yaml"
DEFAULT_OUTPUT = None
DEFAULT_TEMPLATE = "html_templates/dmc_base_template.html"


def load_yaml(path: Path) -> dict:
    """Load YAML safely and ensure the result is a mapping."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("YAML root must be a mapping")
    return data


def validate_yaml(data: dict) -> dict:
    """Basic structural validation. Missing fields are allowed."""
    if not isinstance(data, dict):
        raise ValueError("YAML root must be a mapping")

    session = data.get("session_trace")
    if session and not isinstance(session, dict):
        raise ValueError("'session_trace' must be a mapping if present")
    if session:
        phases = session.get("phases")
        if phases and not isinstance(phases, list):
            raise ValueError("'phases' must be a list")
        if phases:
            for ph in phases:
                if not isinstance(ph, dict):
                    raise ValueError("each phase must be a mapping")
                packets = ph.get("packets")
                if packets and not isinstance(packets, list):
                    raise ValueError("'packets' must be a list")

    tcp = data.get("tcp_packet_trace")
    if tcp and not isinstance(tcp, dict):
        raise ValueError("'tcp_packet_trace' must be a mapping if present")

    return data


def parse_yaml_trace(yaml_data: dict):
    """Extract session header and phases if available."""
    session = yaml_data.get("session_trace") or {}
    header = yaml_data.get("meta") or session.get("session_id")
    phases = session.get("phases", []) if isinstance(session, dict) else []
    tcp_trace = yaml_data.get("tcp_packet_trace")
    return header, phases, tcp_trace


def compute_max_depth(node, current: int = 1) -> int:
    """Recursively compute maximum depth of a YAML structure."""
    if isinstance(node, dict):
        if not node:
            return current
        return max(compute_max_depth(v, current + 1) for v in node.values())
    if isinstance(node, list):
        if not node:
            return current
        return max(compute_max_depth(v, current + 1) for v in node)
    return current


def generate_summary_html(data: dict) -> str:
    """Create summary HTML section with meta information."""
    session = data.get("session") or data.get("session_trace") or {}
    start_time = session.get("start_time")
    session_id = session.get("id") or session.get("session_id")
    version = data.get("meta", {}).get("version")
    depth = compute_max_depth(data)

    parts: list[str] = ["<section class='summary'>"]
    if start_time:
        parts.append(f"<h2>セッション日時: {escape(str(start_time))}</h2>")
    if session_id:
        parts.append(f"<h2>セッションID: {escape(str(session_id))}</h2>")
    if version:
        parts.append(f"<h2>AI-TCPバージョン: {escape(str(version))}</h2>")
    parts.append(f"<h2>YAML最大階層: {depth}</h2>")
    parts.append("</section>")
    return "\n".join(parts)


def generate_body_html(header, phases, tcp_trace, summary_html: str = "") -> str:
    parts: list[str] = []
    session_title = header.get("title") if isinstance(header, dict) else None
    session_id = header.get("session_id") if isinstance(header, dict) else header

    parts.append("<h1>DMCセッション トレース</h1>")
    if summary_html:
        parts.append(summary_html)
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
    if match:
        return match.group(1)
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d")


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    template_path = Path(args.template)

    data = validate_yaml(load_yaml(input_path))
    header, phases, tcp_trace = parse_yaml_trace(data)
    summary_html = generate_summary_html(data)

    session_id = header.get("session_id") if isinstance(header, dict) else header
    
    output_path: Path
    if args.output:
        output_path = Path(args.output)
    else:
        date_part = extract_date(str(session_id))
        output_path = Path("docs/generated") / f"DMC_{date_part}.html"

    if output_path.exists() and not args.force:
        raise FileExistsError(f"{output_path} already exists. Use --force to overwrite")

    body_html = generate_body_html(header, phases, tcp_trace, summary_html)
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
