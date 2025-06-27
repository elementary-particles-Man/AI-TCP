#!/usr/bin/env python3
"""Generate Mermaid flowchart from intent Markdown via Gemma3."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import requests

API_URL = "http://localhost:1234/v1/chat/completions"
MODEL = "google/gemma-3-4b"
SYSTEM_PROMPT = (
    "Convert the provided intent Markdown into Mermaid flowchart LR code. "
    "Return only the Mermaid syntax. Use <br> for newlines inside labels."
)

MERMAID_RE = re.compile(r"```mermaid\s*(.*?)```", re.DOTALL)


def call_llm(text: str) -> str:
    """Call local Gemma3 and return response text."""
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        "temperature": 0.2,
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=30)
    except requests.RequestException as exc:  # pragma: no cover - runtime
        raise SystemExit(f"Request failed: {exc}") from exc
    if resp.status_code != 200:
        raise SystemExit(f"HTTP {resp.status_code}: {resp.text}")
    try:
        data = resp.json()
    except ValueError as exc:  # pragma: no cover - runtime
        raise SystemExit(f"Invalid JSON: {exc}") from exc
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:  # pragma: no cover - runtime
        raise SystemExit("Unexpected response format") from exc
    return content.strip()


def extract_mermaid(text: str) -> str:
    """Return Mermaid code from text, removing fences."""
    m = MERMAID_RE.search(text)
    if m:
        return m.group(1).strip()
    return text.strip()


def process_file(md_path: Path, out_path: Path) -> None:
    """Send Markdown to LLM and write Mermaid output."""
    markdown = md_path.read_text(encoding="utf-8")
    result = call_llm(markdown)
    code = extract_mermaid(result)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(f"```mermaid\n{code}\n```\n", encoding="utf-8")
    print(f"✅ Mermaid saved to {out_path}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="intent Markdown -> Mermaid")
    parser.add_argument("markdown", type=Path, help="intent_XXX.md file")
    parser.add_argument("-o", "--output", type=Path, help="output file path")
    args = parser.parse_args(argv)

    out_path = args.output if args.output else args.markdown.with_suffix(".mmd.md")
    process_file(args.markdown, out_path)


if __name__ == "__main__":
    main()
