# AI-TCP: Overview and Documentation Index

## 🧠 Project Purpose

**AI-TCP** (Artificial Intelligence - Thought Communication Protocol) is a framework for defining and structuring interoperable communication protocols between AI agents. The aim is to formalize shared memory, inference traces, and high-level intention exchange through structured YAML, RFC-style documentation, and executable PoC examples.

---

## 📂 Directory Overview

| Folder               | Purpose                                                                 |
|----------------------|-------------------------------------------------------------------------|
| `rfc_drafts/`        | Drafts of AI-TCP specifications in RFC format                          |
| `structured_yaml/`   | YAML schemas for protocol definitions and compliance structure          |
| `dmc_sessions/`      | Use-case PoC sessions (Direct Mental Care etc.)                         |
| `generated_html/`    | Automatically rendered versions of YAML and documents                   |
| `scripts/`           | Utility scripts for generation, validation, or conversion tasks         |

---

## 📘 RFC Drafts

The RFC documents provide the foundational standards for AI-TCP:

| RFC       | Title                                | Purpose                                           |
|-----------|--------------------------------------|--------------------------------------------------|
| RFC001    | Overview                             | Defines AI-TCP core concepts and architecture    |
| RFC002    | LLM Compliance Protocol              | Outlines compliance interface for LLMs           |
| RFC003    | Packet Structure                     | YAML packet and Graph Payload specifications     |
| RFC004    | Reasoning Trace Format               | Structure for thought chains and inference logs  |

See [rfc_drafts/README.md](./rfc_drafts/README.md) for detailed navigation.

---

## 🚧 Work in Progress

- Finalize PoC validation for `dmc_sessions/`
- Complete Graph Payload specifications in Mermaid
- Automate Index/README generation
- Validate YAML↔HTML↔Graph synchronization

---

## 🔁 See Also

- [rfc_index.md](./rfc_drafts/rfc_index.md) – RFC document registry
- [master_schema_v1.yaml](../schemas/master_schema_v1.yaml) – Root schema structure
