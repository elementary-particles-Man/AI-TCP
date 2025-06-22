# RFC 013: Obsidian Integration Schema for AI-TCP

## 1. Introduction

This document describes how AI-TCP documentation, structured YAML, and trace outputs
should be organized inside an Obsidian vault. The goal is to maintain
consistency across vaults so that RFC drafts, session logs, and generated
artifacts remain navigable and linkable.

## 2. Folder Structure Conventions

- `docs/` – Human-readable documentation and RFC drafts.
- `structured_yaml/` – YAML session definitions including `validated_yaml/`.
- `dmc_sessions/` – Direct Mental Care session notes and transcripts.
- `generated_mermaid/` – Stand-alone Mermaid diagrams (`.mmd.md`).
- `generated_html/` – HTML renders of RFC documents.

All folders live at the root of the vault so relative links remain stable.

## 3. File Naming and Indexing

RFC files follow the pattern `NNN_<topic>.md` where `NNN` is a zero padded
identifier. YAML sessions are named `<session_type>_<domain>_<serial>.yaml` as
specified in RFC 002. A simple index such as `000_rfc_index.md` lists the RFCs
and SHOULD be updated whenever new drafts are added.

## 4. Mermaid Support

Obsidian renders Mermaid graphs when files use the `.mmd.md` extension.
All Graph Payloads extracted from YAML SHOULD be saved under
`generated_mermaid/` using this format so they can be embedded with:

```markdown
![[generated_mermaid/001_example.mmd.md]]
```

## 5. Link Conventions

Use relative paths for all links. In Obsidian, links may use the wiki-style
syntax with optional aliases:

```markdown
[[structured_yaml/dmc_mental_001.md|DMC Example]]
```

Links between RFCs SHOULD reference the filename directly, e.g.
`[[003_packet_definition.md]]`. Avoid absolute paths so the vault can be moved
without breaking references.

## 6. Example Vault Layout

```
AI-TCP/
├─ docs/
│  └─ rfc_drafts/
│     └─ 013_obsidian_schema.md
├─ structured_yaml/
│  ├─ validated_yaml/
│  └─ tcp_logic_001.md
├─ dmc_sessions/
│  └─ gemini_dmc_session_20250618.md
├─ generated_mermaid/
└─ generated_html/
```

This layout allows Obsidian to index all AI-TCP artifacts while keeping
related assets grouped by type.

## 7. Status

Status: Draft
Last Updated: 2025-06-22
