# 📊 Graph Payload Usage in AI-TCP

## 1. 概要

AI-TCPでは、思考・意図・構造の視覚的共有のため、`graph_payload.graph_structure` に Mermaid形式（flowchart等）を使用します。

## 2. フォーマット仕様

- Mermaid構造は `mmd:` で始めること
- YAMLでは `|` ブロック表現で記述する
- Mermaidコードの途中に YAMLコメント（#）は不可
- Obsidian互換構文を推奨（新規行を避け、インデントで明示）

```yaml
graph_payload:
  graph_structure: |
    mmd:flowchart TD
    A[Request] --> B{Decision}
    B -->|Yes| C[Process]
    B -->|No| D[Reject]
3. 使用例
ユースケース	Mermaid構造の目的
意図共有	目的や流れの可視化
合意形成	分岐条件の構造共有
フィードバック	中断・巻き戻し構造の提示

4. 構文制約と推奨
Mermaidブロックは YAMLとして1つの文字列とみなされること（Python/PyYAML互換）

Mermaid記述には flowchart TD, graph TD, stateDiagram を推奨

Mermaid構造内に \n は使用しない（YAML的に不安定）
