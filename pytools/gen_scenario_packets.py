#!/usr/bin/env python3
"""Generate YAML packets for PoC scenarios.

This script reads graph payload templates and outputs
AI-TCP packet examples for Scenario 1-3 described in
`docs/poc_scenario.md`.
"""
from __future__ import annotations

import argparse
import datetime
from pathlib import Path

import yaml

TEMPLATE_FILE = Path("docs/templates/graph_payload_templates.yaml")
OUTPUT_DIR = Path("dmc_sessions")

# Mapping from scenario name to template key
SCENARIO_TEMPLATE = {
    "scenario1": "template_basic",
    "scenario2": "template_feedback_loop",
    "scenario3": "template_decision_tree",
}


def load_templates() -> dict:
    """Load graph_payload templates."""
    return yaml.safe_load(TEMPLATE_FILE.read_text(encoding="utf-8"))


def build_packet(name: str, templates: dict) -> dict:
    """Return packet dictionary for the given scenario name."""
    now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    packet = {
        "meta": {"timestamp": now, "origin": "gen_scenario_packets"},
    }

    template_key = SCENARIO_TEMPLATE[name]
    packet.update(templates.get(template_key, {}))

    if name == "scenario1":
        packet["reasoning_trace"] = [
            {"step": 1, "action": "share_intent"},
            {"step": 2, "action": "interpret_structure"},
            {"step": 3, "action": "acknowledge"},
        ]
        packet["auto_redirect"] = {"type": "feedback", "next_action": "proceed"}

    elif name == "scenario2":
        packet["reasoning_trace"] = [
            {"step": 1, "action": "propose_graph"},
            {"step": 2, "feedback": "graph mismatch"},
            {"step": 3, "action": "resend_fixed"},
            {"step": 4, "action": "approve"},
        ]
        packet["auto_redirect"] = {"type": "feedback", "next_action": "acknowledge"}

    elif name == "scenario3":
        packet["reasoning_trace"] = [
            {"step": 1, "state": "propose"},
            {"step": 2, "state": "reject"},
            {"step": 3, "state": "revise"},
            {"step": 4, "state": "agree"},
        ]
        packet["auto_redirect"] = {"type": "next_action", "target": "finalize"}

    return packet


def write_packet(name: str, packet: dict) -> None:
    """Write packet YAML to dmc_sessions directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    index = name[-1]
    path = OUTPUT_DIR / f"scenario_{index}.yaml"
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(packet, f, allow_unicode=True, sort_keys=False)
    print(f"Generated {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate PoC scenario packets")
    parser.add_argument("scenario", nargs="?", choices=list(SCENARIO_TEMPLATE.keys()))
    parser.add_argument("--all", action="store_true", help="generate all scenarios")
    args = parser.parse_args()

    templates = load_templates()

    targets = list(SCENARIO_TEMPLATE.keys()) if args.all else [args.scenario]
    if not targets or None in targets:
        parser.error("Specify a scenario or --all")

    for name in targets:
        packet = build_packet(name, templates)
        write_packet(name, packet)


if __name__ == "__main__":
    main()
