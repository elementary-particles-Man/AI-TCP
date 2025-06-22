# 📑 AI-TCP RFC Draft Index

This directory contains draft specifications for the AI-TCP protocol.

## Available Drafts

- [001_ai_tcp_overview.md](001_ai_tcp_overview.md)  
  *Purpose*: High-level design and use-case framing. Describes AI-TCP's intent, structure, and architecture.

- [002_llm_compliance.md](002_llm_compliance.md)  
  *Purpose*: Defines compliance requirements for LLMs. Includes trace logging rules and mandatory fields.

- [003_packet_definition.md](003_packet_definition.md)  
  *Purpose*: YAML schema for AI-TCP packets. Specifies minimal structure, lifecycle, and constraints.

## Format & Conventions

All documents use Markdown (`.md`) for readability and YAML for embedded examples.

- Mermaid diagrams must use the `mmd:` prefix and be embedded in the `graph_payload.graph_structure` YAML field.
- Code examples should use fenced code blocks (```yaml, ```mermaid) with language tags.
- All RFC files are named as `RFC ###_topic.md` using 3-digit identifiers and snake_case.
- Each RFC must begin with `# RFC ###: Title` and use numbered section headings (`## 1.`, `## 2.` etc).

## Status

All drafts listed here are currently in **PoC-phase**, and subject to iterative updates and refinement by AI and human reviewers.

Future additions (e.g., `004_reasoning_diagnostics.md`, `005_security_considerations.md`) will follow the same structure and conventions.
