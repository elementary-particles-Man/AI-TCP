# 🗂️ AI-TCP Documentation Overview

This directory contains the complete documentation structure for the AI-TCP project, including its specifications, drafts, and session data.

---

## 📘 Structure

### `/rfc_drafts/`
Contains all RFC specification drafts related to AI-TCP.

- `000_rfc_index.md` – Index listing of all RFC drafts
- `001_ai_tcp_overview.md` – Overview of AI-TCP philosophy and architecture
- `002_llm_compliance.md` – Requirements for language model compliance
- `003_packet_definition.md` – Technical definition of TCP-style packet structures
- `004_thought_logging.md` – Specification for inference and reasoning chain logging

### `/dmc_sessions/`
Contains YAML and HTML logs of real-time AI mental session use cases for PoC.

### `/assets/`
Visual aids and diagrams to supplement RFC documents (e.g., Mermaid exports)

---
Phase 3: Graph Payload-Based Inter-AI Communication
In this phase, AI-TCP introduces a new structure called "Graph Payload" using Mermaid syntax.
This allows LLMs to communicate not just with plain text or YAML, but with interpretable graph semantics.
Graph Payloads enable:
Intent clarification through graph edges
Role-based rendering (e.g., source, process, response)
Bidirectional interpretation and negotiation
This phase includes:
Graph transmission & reception PoC
Reverse parsing from Graph to YAML
Use case: conflict negotiation and resolution

## 🛠️ Contribution Guide

- **Update RFCs** via `rfc_drafts/`
- **Link from index** in `000_rfc_index.md`
- All additions should follow Markdown RFC format guidelines

---

_Last updated: 2025-06-22_
