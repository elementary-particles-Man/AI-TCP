# 📘 AI-TCP RFC Collection

## 概要
このディレクトリは、AI間通信プロトコル「AI-TCP」の仕様群（RFC）を収録しています。  
各文書は独立して参照可能でありながら、全体構造の中で明確な役割を持ちます。

## ドキュメント構成

### RFC001: AI-TCP Overview
- AI-TCPの設計哲学、背景、全体像を記述
- Mermaidによる構造図を含む
- [📄 RFC001を読む](./001_ai_tcp_overview.md)

### RFC002: LLM Compliance Schema
- LLMが準拠すべき入出力構造・役割記述・応答要件を定義
- [📄 RFC002を読む](./002_llm_compliance.md)

### RFC003: AI-TCP Packet Protocol
- 通信単位としてのパケット構造、ヘッダ、ペイロード定義
- Mermaid視覚構造付き
- [📄 RFC003を読む](./003_packet_definition.md)

### GG01: LLM Role Definitions
- 各AIエージェントに割り当てる「役割階層」の定義
- [📄 GG01を読む](./GG01_llm_roles.md)

### GG02: Trace Annotation Syntax
- トレース記法および思考ログの共通記述ルール
- [📄 GG02を読む](./GG02_trace_annotation.md)

### GG03: Fault Handling & Resilience
- 例外処理、回復戦略、再実行指針などの統一ルール
- [📄 GG03を読む](./GG03_fault_handling.md)

### GG04: Security Policies
- AI-TCPの安全基準、通信暗号化、アクセス制御ポリシー
- [📄 GG04を読む](./GG04_security_policy.md)

### GG05: Evaluation Metrics & Criteria
- PoC評価、判定基準、スコア設計の標準化
- [📄 GG05を読む](./GG05_evaluation_metrics.md)

## インデックス
- [📂 RFC一覧（rfc_index.md）](./rfc_index.md)

---
*自動生成：G6タスク（GPT/Codex協調）*