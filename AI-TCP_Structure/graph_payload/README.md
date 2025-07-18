# Graph Payload (Mermaid Syntax) Storage Specification

## Overview

This `graph_payload/` directory is dedicated to storing **visual structural definitions (Graph Payload)** within the AI-TCP structure. Each file has a `.mmd.md` extension and is composed using Mermaid syntax (Obsidian compatible).

---

## Naming Convention

- `intent_###.mmd.md`
  - Mermaid structural diagrams derived from YAML-based intent structures (`intent_###.yaml`).
- The `.mmd.md` extension signifies both:
  - `mmd:` prefix (indicating Mermaid content)
  - Obsidian compatible Markdown (`.md`)

---

## Mermaid Syntax Rules (AI-TCP Compliant)

- Mermaid type: `flowchart LR` (left-to-right directed graph)
- Always prefix lines with `mmd:`
- All line breaks are replaced with `<br>` (for Obsidian and GitHub rendering compatibility)
- Each node is defined in `id[label_text]` format
- Based on YAML structure: `components` → node definitions, `connections` → edge definitions

```mermaid
mmd:flowchart LR<br>
    ai_agent_1[AI Agent]<br>
    module_1[Negotiation Module]<br>
    ai_agent_1 --> module_1<br>
```

---

# Graph Payload（Mermaid構文）格納仕様

## 概要

本ディレクトリ `graph_payload/` は、AI-TCP構造における**視覚的構造定義（Graph Payload）**を格納する専用領域です。各ファイルは `.mmd.md` 拡張子を持ち、Mermaid構文（Obsidian対応）によって構成されます。

---

## 命名規則

- `intent_###.mmd.md`
  - YAMLベースとなった意図構造（`intent_###.yaml`）から派生したMermaid構造図
- 拡張子 `.mmd.md` は、以下の両方を意味します：
  - `mmd:` プレフィックス付き（Mermaidであること）
  - Obsidian互換Markdownであること（`.md`）

---

## Mermaid構文ルール（AI-TCP準拠）

- Mermaid種別：`flowchart LR`（左→右の有向グラフ）
- 行頭に必ず `mmd:` プレフィックスを付与
- 改行はすべて `<br>` に置換（ObsidianおよびGitHub描画対策）
- 各ノードは `id[label_text]` 形式で定義
- YAML構造に基づき、`components` → ノード定義、`connections` → エッジ定義

```mermaid
mmd:flowchart LR<br>
    ai_agent_1[AI Agent]<br>
    module_1[Negotiation Module]<br>
    ai_agent_1 --> module_1<br>
```