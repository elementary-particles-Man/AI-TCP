#!/usr/bin/env python3
"""Convert a Markdown chat log into a standalone HTML viewer."""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

# Try markdown converters
converter = None
try:
    import markdown2  # type: ignore

    converter = lambda text: markdown2.markdown(text, extras=["fenced-code-blocks"])
except Exception:
    try:
        import mistune  # type: ignore

        md = mistune.create_markdown()
        converter = lambda text: md(text)
    except Exception:
        converter = None


_DEF_STYLE = """
body{font-family:sans-serif;padding:1em;}
.msg{padding:0.5em;border-radius:8px;margin-bottom:1em;}
.user{background:#e3f2fd;border-left:4px solid #42a5f5;}
.assistant{background:#f1f8e9;border-left:4px solid #66bb6a;}
.system{background:#f5f5f5;border-left:4px solid #aaa;}
.tokens{text-align:right;color:#666;font-size:0.8em;}
"""

_ROLE_RE = re.compile(r"^\s*###\s*(\w+)", re.IGNORECASE)

def parse_chat(text: str) -> list[tuple[str, str]]:
    messages: list[tuple[str, str]] = []
    role: str | None = None
    buf: list[str] = []
    for line in text.splitlines():
        m = _ROLE_RE.match(line)
        if m:
            if role is not None:
                messages.append((role, "\n".join(buf).strip()))
            role = m.group(1).lower()
            buf = []
        else:
            buf.append(line)
    if role is not None:
        messages.append((role, "\n".join(buf).strip()))
    return messages


def build_html(messages: list[tuple[str, str]], count_tokens: bool) -> str:
    html_parts = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        "  <title>Chat Log</title>",
        "  <script type=\"module\" src=\"https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs\"></script>",
        f"  <style>{_DEF_STYLE}</style>",
        "</head>",
        "<body>",
    ]

    for role, msg in messages:
        body = converter(msg) if converter else f"<pre>{html.escape(msg)}</pre>"
        tokens = len(msg.split())
        html_parts.append(f'<div class="msg {role}">')
        html_parts.append(body)
        if count_tokens:
            html_parts.append(f'<div class="tokens">Tokens: {tokens}</div>')
        html_parts.append("</div>")

    html_parts.append("  <script>mermaid.initialize({startOnLoad:true});</script>")
    html_parts.append("</body>")
    html_parts.append("</html>")
    return "\n".join(html_parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert chat log Markdown to HTML")
    parser.add_argument("input", help="input Markdown file")
    parser.add_argument("output", help="output HTML file")
    parser.add_argument("--count-tokens", action="store_true", help="display token counts")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    messages = parse_chat(text)
    html_text = build_html(messages, args.count_tokens)
    Path(args.output).write_text(html_text, encoding="utf-8")
    print(f"✅ Generated {args.output}")


if __name__ == "__main__":
    main()
