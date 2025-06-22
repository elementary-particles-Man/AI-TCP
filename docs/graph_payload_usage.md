# Graph Payloads in AI-TCP

## Usage
- All graph structures are embedded as:
```yaml
graph_payload:
  graph_structure: |
    mmd:flowchart TD
    A --> B
Rules
Prefix mmd: MUST be present for Mermaid recognition

Use Obsidian-compatible syntax

Avoid newlines outside Mermaid code

Place graph_structure as a string block (|) for readability

yaml
コピーする
編集する

---

### 📁 **[Obsidian構造レイアウト設計] `AI-TCP_Structure/` 提案**

ディレクトリ案（ローカル向け）：
AI-TCP_Structure/
├── structured_yaml/
│ └── master_schema_v1.yaml, ...
├── dmc_sessions/
│ └── dmc_mental_001.yaml, ...
├── rfc_drafts/
│ └── 001_ai_tcp_overview.md, ...
├── generated_html/
│ └── structure_map_master_schema.html, ...
├── docs/
│ └── graph_payload_usage.md
└── index.md ← 起点リンク（Mermaid構造 + RFCリンク含む）

scss
コピーする
編集する

起点ファイル `index.md`（下書き）には：
```markdown
# 🧠 AI-TCP Master Index

- [RFC Overview](rfc_drafts/001_ai_tcp_overview.md)
- [Graph Structure Rules](docs/graph_payload_usage.md)
- [Generated Mermaid Map](generated_html/structure_map_master_schema.html)
