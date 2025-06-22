# RFC 013: Obsidian Integration Schema for AI-TCP

## 1. Introduction

This RFC defines the conventions for organizing AI-TCP documentation, YAML artifacts, and trace outputs within an Obsidian vault. The goal is to maintain consistency across vaults and GitHub so that all protocol artifacts remain easily navigable, linkable, and portable.

## 2. Folder Structure

AI-TCP/
├─ docs/
│ ├─ rfc_drafts/ # Markdown-based RFCs (e.g., 001_ai_tcp_overview.md)
│ ├─ assets/ # Diagrams or images for RFCs
│ └─ poc_design/ # PoC scenarios and design specs
├─ structured_yaml/
│ ├─ validated_yaml/ # Schema-validated YAML examples
│ └─ tcp_logic_001.yaml # Main YAML definitions
├─ dmc_sessions/ # Narrative logs and transcripts of DMC sessions
│ └─ gemini_dmc_session_20250618.md
├─ generated_mermaid/ # Renderable Mermaid diagrams (.mmd.md)
├─ generated_html/ # Rendered HTML views of RFCs and payloads

markdown
コピーする
編集する

## 3. File Naming & Indexing

- RFC drafts use the pattern `NNN_<topic>.md`, where `NNN` is a zero-padded ID (e.g., `013_obsidian_schema.md`).
- YAML files follow `<schema>_v<version>.yaml` or `<type>_<domain>_<serial>.yaml` as defined in RFC 002.
- Mermaid files should use `.mmd.md` suffix to trigger Obsidian rendering.
- Index files:
  - `000_rfc_index.md`: manual RFC registry
  - `README.md` in `rfc_drafts/`: auto-generated via `generate_rfc_toc.py`

## 4. Mermaid Compatibility

Mermaid graphs:
- MUST be placed in `.mmd.md` files under `generated_mermaid/`
- MUST use `<br>` for line breaks instead of `\n`
- SHOULD be embedded in YAML payloads using `mmd:` prefix if needed
- Obsidian renders Mermaid inline with:

```markdown
![[generated_mermaid/001_example.mmd.md]]
5. Link Conventions
All internal links MUST be relative.

Use wiki-style syntax for Obsidian links, e.g., [[structured_yaml/dmc_mental_001.yaml|DMC Session]].

Between RFCs: [[003_packet_definition.md]]

Avoid absolute paths to ensure portability across environments.

6. Future Enhancements
Integration of Obsidian ↔ Git auto-sync scripts

Expanded multilingual support in note metadata and aliases

7. Status
Status: Draft

Last Updated: 2025-06-22

Maintainer: elementary-particles-Man