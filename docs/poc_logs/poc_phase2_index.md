4.1 PoC成果物リスト (GPT-1)
ファイルパス: docs/poc_logs/poc_phase2_index.md
ファイル名
種別
担当
概要
structured_yaml/intent_001.yaml
YAML
Manual
PoCの初期意図構造データ
AI-TCP_Structure/graph/intent_001.mmd.md
Mermaid
Codex
YAMLからMermaidへの変換結果
docs/poc_logs/intent_narrative_001.md
Narrative
Gemini
Mermaidグラフの意味解釈・言語化
docs/poc_logs/poc_003_reverse...md
Log
Gemini
逆受信テストの検証ログ

4.2 フォルダ構造インデックス (GPT-2)
ファイルパス: docs/poc_logs/structure_map_index.md
Repository Structure Map
YAML Definitions: /structured_yaml/
Mermaid Graphs: /AI-TCP_Structure/graph/
PoC Logs: /docs/poc_logs/
RFCs: /docs/rfc_drafts/
4.3 リンクマップ逆検証テーブル (GPT-3)
ファイルパス: docs/poc_logs/link_map_verification.md
Verification Table for link_map.json
Intent ID
From (起点)
Relation (関係性)
To (終点)
Status
DMC-NARRATIVE-001
intent_narrative_001.md
is_narrative_for
intent_001.html
✅ Verified
DMC-GRAPH-VERIFY-001
verify_graph_001.md
validates
intent_001.mmd.md
✅ Verified

4.4 PoCフェーズ進行フロー図 (GPT-4)
ファイルパス: docs/poc_logs/poc_phase_workflow.mmd.md
flowchart TD
    subgraph "PoC Phase 1 & 2"
        A[1. Define Intent<br>(YAML)] --> B[2. Generate Visual Model<br>(Mermaid)];
        B --> C[3. Create Narrative<br>(Human-Readable Text)];
        C --> D[4. Reverse-Reception Test<br>(Reconstruct YAML)];
    end
    D --> E((Phase 3: External LLM Test));


4.5 構造用語の共通定義集 (GPT-5)
ファイルパス: docs/structure_terms.md
AI-TCP Common Structural Terms
Term
Definition
Related RFC
Intent Packet
The canonical YAML structure representing an agent's structured thought, composed of components and connections.
RFC 003
Graph Payload
The visual representation of an Intent Packet, typically rendered as a Mermaid graph.
RFC 003
Reasoning Trace
A sequential log outlining the step-by-step logic that led to the current state or packet.
RFC 004

