#!/usr/bin/python3
"""Generate simple HTML from AI-TCP DMC trace YAML."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def extract_data(data: Dict[str, Any]):
    """Extract meta, session and tcp trace information."""
    meta = data.get('meta', {}) if isinstance(data, dict) else {}

    if 'session_trace' in data:
        session = data['session_trace'] or {}
    else:
        # Gemini style might put session fields at top level
        session_keys = {'session_id', 'phases'}
        session = {k: data.get(k) for k in session_keys if k in data}

    tcp_trace = data.get('tcp_packet_trace', {}) if isinstance(data, dict) else {}
    return meta, session, tcp_trace


def html_escape(text: Any) -> str:
    from html import escape

    return escape(str(text))


def create_html(title: str, session_id: str, phases: Any, tcp_trace: Any) -> str:
    parts = [
        '<!DOCTYPE html>',
        '<html lang="ja">',
        '<head>',
        '  <meta charset="UTF-8">',
        f'  <title>{html_escape(title)}</title>',
        '</head>',
        '<body>',
    ]

    if title:
        parts.append(f'<h1>{html_escape(title)}</h1>')
    if session_id:
        parts.append(f'<h2>Session ID: {html_escape(session_id)}</h2>')

    if phases:
        parts.append('<h3>Phases</h3>')
        parts.append('<ul>')
        for ph in phases:
            ph_id = ph.get('id', '')
            ph_name = ph.get('name', '')
            parts.append(f'<li><strong>{html_escape(ph_id)} {html_escape(ph_name)}</strong>')
            packets = ph.get('packets', [])
            if packets:
                parts.append('<ul>')
                for pkt in packets:
                    pid = pkt.get('packet_id', '')
                    intent = pkt.get('intent', '')
                    trace_link = pkt.get('trace_link', '')
                    parts.append('<li>')
                    parts.append(f'{html_escape(pid)}: {html_escape(intent)}')
                    if trace_link:
                        parts.append(f'<br><small>{html_escape(trace_link)}</small>')
                    parts.append('</li>')
                parts.append('</ul>')
            parts.append('</li>')
        parts.append('</ul>')

    if tcp_trace:
        parts.append('<h3>TCP Packet Trace</h3>')
        parts.append('<ol>')
        for entry in tcp_trace.get('trace', []):
            phase_name = entry.get('phase', '')
            parts.append(f'<li><strong>{html_escape(phase_name)}</strong>')
            packet = entry.get('packet', {})
            header = packet.get('header', {})
            payload = packet.get('payload', {})
            if header:
                parts.append('<details><summary>Header</summary><pre>')
                parts.append(html_escape(yaml.dump(header, allow_unicode=True)))
                parts.append('</pre></details>')
            if payload:
                parts.append('<details><summary>Payload</summary><pre>')
                parts.append(html_escape(yaml.dump(payload, allow_unicode=True)))
                parts.append('</pre></details>')
            parts.append('</li>')
        parts.append('</ol>')

    parts.append('</body>')
    parts.append('</html>')
    return '\n'.join(parts)


def main():
    input_path = Path('structured_yaml/validated_yaml/ai_tcp_dmc_trace.yaml')
    output_dir = Path('generated_html')
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / 'DMC_20250618.html'

    data = load_yaml(input_path)
    meta, session, tcp_trace = extract_data(data)
    title = meta.get('title', '')
    session_id = session.get('session_id', '')
    phases = session.get('phases', [])
    html = create_html(title, session_id, phases, tcp_trace)
    output_path.write_text(html, encoding='utf-8')
    print(f'HTML generated at {output_path}')


if __name__ == '__main__':
    main()
