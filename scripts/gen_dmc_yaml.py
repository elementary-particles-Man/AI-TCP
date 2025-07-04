#!/usr/bin/env python3
"""Reconstruct YAML from AI-TCP DMC HTML report.

This script reads an HTML file generated by ``gen_dmc_html.py`` and
attempts to rebuild the original YAML structure. Only a subset of the
information (session meta and packet trace) is extracted to provide a
proof-of-concept reverse conversion.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from bs4 import BeautifulSoup
import yaml

DEFAULT_INPUT = "generated_html/DMC_20250618.html"
DEFAULT_OUTPUT = "reverse_generated.yaml"


def parse_meta(soup: BeautifulSoup) -> tuple[str, dict]:
    """Parse meta-info section and return session_id and meta mapping."""
    meta_div = soup.find("div", class_="meta-info")
    meta: dict[str, str] = {}
    session_id = ""
    if meta_div:
        titles = meta_div.find_all("span", class_="field-title")
        values = meta_div.find_all("span", class_="field-value")
        for t, v in zip(titles, values):
            key = t.get_text(strip=True).strip(":")
            val = v.get_text(strip=True)
            if key.startswith("セッションID"):
                session_id = val
            elif key.startswith("作成日"):
                meta["created"] = val
            elif key.startswith("目的"):
                meta["purpose"] = val
    return session_id, meta


def parse_packets(start_tag) -> list[dict]:
    """Collect packet information until the next <h2> tag."""
    packets: list[dict] = []
    current = start_tag.find_next_sibling()
    while current and current.name != "h2":
        if current.name == "details":
            summary = current.find("summary")
            packet_id = intent = ""
            if summary:
                m = re.match(r"Packet\s*(\S+):\s*(.+)", summary.get_text(strip=True))
                if m:
                    packet_id, intent = m.groups()
                else:
                    intent = summary.get_text(strip=True)
            span = current.find("span", string=lambda s: s and "Trace Link" in s)
            trace_link = ""
            if span:
                code = span.find_next("code")
                if code:
                    trace_link = code.get_text(strip=True)
                else:
                    val_div = span.find_next("div", class_="field-value")
                    if val_div:
                        trace_link = val_div.get_text(strip=True)
            packets.append({
                "packet_id": packet_id,
                "intent": intent,
                "trace_link": trace_link,
            })
        current = current.find_next_sibling()
    return packets


def parse_phases(soup: BeautifulSoup) -> list[dict]:
    """Parse phases and their packets."""
    phases: list[dict] = []
    for h2 in soup.find_all("h2"):
        m = re.match(r"Phase\s*(\d+):\s*(.+)", h2.get_text(strip=True))
        if not m:
            continue
        num, name = m.groups()
        packets = parse_packets(h2)
        phases.append({
            "id": f"dmc_phase{num}",
            "name": name,
            "packets": packets,
        })
    return phases


def parse_html(path: Path) -> dict:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    session_id, meta = parse_meta(soup)
    phases = parse_phases(soup)
    data = {"session_trace": {"session_id": session_id, "phases": phases}}
    if meta:
        data["meta"] = meta
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate YAML from DMC HTML")
    parser.add_argument("--input", "-i", default=DEFAULT_INPUT, help="HTML input path")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="YAML output path")
    args = parser.parse_args()

    html_path = Path(args.input)
    yaml_path = Path(args.output)

    data = parse_html(html_path)
    yaml_path.write_text(yaml.dump(data, allow_unicode=True), encoding="utf-8")
    print(f"[OK] YAML saved to {yaml_path}")


if __name__ == "__main__":
    main()
