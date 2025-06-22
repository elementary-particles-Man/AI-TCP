#!/usr/bin/env python3
"""Convert DMC session YAML files to HTML summaries."""
from __future__ import annotations

import sys
from pathlib import Path
try:
    import yaml
except Exception:  # noqa: BLE001
    yaml = None

TEMPLATE = """<!DOCTYPE html>
<html lang=\"ja\">
<head>
<meta charset=\"UTF-8\">
<title>{title}</title>
<link rel=\"stylesheet\" href=\"../html_templates/structured_index_style.css\">
</head>
<body>
<h1>{title}</h1>
<div class=\"session-block\">
<h2>メタ情報</h2>
<ul>
<li><b>セッションID:</b> {sid}</li>
<li><b>日時:</b> {ts}</li>
<li><b>エージェント:</b> {agent}</li>
<li><b>フェーズ:</b> {phase}</li>
<li><b>タグ:</b> {tags}</li>
</ul>
</div>
<div class=\"session-block\">
<h2>会話</h2>
<pre>{dialog}</pre>
</div>
{mermaid}
</body>
</html>"""

MERMAID_TEMPLATE = """<div class=\"session-block\">
<h2>Mermaid Flow</h2>
<pre class=\"mermaid\">
sequenceDiagram
{flow}
</pre>
</div>"""

def load_sessions(directory: Path):
    for path in directory.rglob('*.yaml'):
        yield path

def parse_yaml(path: Path) -> dict:
    if yaml is None:
        print(f"[WARN] PyYAML not available; skipping {path}", file=sys.stderr)
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding='utf-8'))
    except Exception as exc:  # noqa: BLE001
        print(f"[WARN] Failed to read {path}: {exc}", file=sys.stderr)
        return {}

def build_html(data: dict, out_path: Path):
    sid = data.get('id', '')
    ts = data.get('timestamp', '')
    agent = data.get('agent', '')
    phase = data.get('phase', '')
    tags = ', '.join(data.get('tags', [])) if isinstance(data.get('tags'), list) else ''
    dialog = ''
    flow_lines: list[str] = []
    d = data.get('data', {})
    if isinstance(d, dict):
        user = d.get('input', '').strip()
        ai = d.get('output', '').strip()
        dialog = f"User:\n{user}\n---\nAI:\n{ai}"
        if user or ai:
            flow_lines.append(f"User->>AI: {user.replace('\n',' ')}")
            flow_lines.append(f"AI-->>User: {ai.replace('\n',' ')}")
    mermaid = ''
    if flow_lines:
        mermaid = MERMAID_TEMPLATE.format(flow='\n'.join(flow_lines))
    title = f"DMC Session {sid}" if sid else "DMC Session"
    html = TEMPLATE.format(title=title, sid=sid, ts=ts, agent=agent, phase=phase, tags=tags, dialog=dialog, mermaid=mermaid)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding='utf-8')
    print(f"[OK] wrote {out_path}")

def main() -> None:
    src_dir = Path('dmc_sessions')
    dst_dir = Path('html_sessions')
    found = False
    for path in load_sessions(src_dir):
        found = True
        data = parse_yaml(path)
        name = path.stem + '.html'
        out_path = dst_dir / name
        build_html(data, out_path)
    if not found:
        print('[INFO] No YAML sessions found in dmc_sessions/')

if __name__ == '__main__':
    main()
