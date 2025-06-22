# RFC 013: Obsidian Integration Schema for AI-TCP

## 1. Overview
This RFC defines the conventions for organising AI-TCP documentation and trace outputs within an Obsidian vault.  The goal is to maintain a consistent folder structure, file naming scheme and linking strategy so that all protocol artefacts remain easily navigable across both Obsidian and GitHub.

## 2. Folder Structure
- `docs/` – Markdown documentation, assets and RFC drafts
  - `rfc_drafts/` – numbered RFC files (`000_rfc_index.md`, `001_ai_tcp_overview.md`, ...)
  - `assets/` – diagrams and images referenced by RFCs
  - `poc_design/` – PoC scenarios and supporting documents
- `structured_yaml/` – YAML schemas and validated outputs
  - `validated_yaml/` – schema-checked YAML examples
- `dmc_sessions/` – narrative logs and HTML traces of live sessions

## 3. File Naming & Indexing
- RFC drafts use a three‑digit prefix: `013_obsidian_schema.md`
- YAML schemas follow `<schema_name>_v<version>.yaml`
- Session files may be timestamped: `dmc_session_20250618_narrative.md`
- `000_rfc_index.md` provides a manual table of all RFCs
- `rfc_drafts/README.md` is auto‑generated via `generate_rfc_toc.py`

## 4. Mermaid Compatibility
Mermaid code blocks must render correctly in both Obsidian and GitHub. Use `<br>` to force line breaks and avoid trailing spaces.  Keep diagrams inside fenced blocks and prefix graphs with `mmd:` when embedded in YAML.

## 5. Link Conventions
- Use relative links between files so the vault remains portable
- Obsidian aliases may be defined with the `[[path|alias]]` syntax
- Cross‑references to YAML or HTML outputs should point to their location under `structured_yaml/` or `generated_html/`

## 6. Future Work
- Automated sync scripts for Obsidian‑Git integration
- Expanded support for multilingual note titles and aliases

---
*Last updated: 2025-06-22*
