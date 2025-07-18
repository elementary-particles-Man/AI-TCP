# 📑 AI-TCP RFC Drafts (Refined)

This document presents a refined list of AI-TCP RFC drafts, focusing on key specifications.

| Title | Created | Summary |
| :---- | :------ | :------ |
| [RFC 001: AI-TCP Protocol Overview](001_ai_tcp_overview.md) | 2025-06-22 | AI-TCP is a lightweight, structured protocol for inter-AI communication using YAML, Graph Payloads (Mermaid), and traceable reasoning. |
| [RFC 002: LLM Compliance Layer in AI-TCP](002_llm_compliance.md) | 2025-06-22 | This document defines the compliance requirements for Large Language Models (LLMs) participating in AI-TCP communication. |
| [RFC 003: AI-TCP Packet Structure Definition](003_packet_definition.md) | 2025-06-22 | This document formalizes the structure and minimal required fields for AI-TCP-compliant packets. These packets serve as the atomic units of communication between LLMs under the AI-TCP protocol. |
| [RFC 004: Reasoning Trace & Thought Chain Structure](004_reasoning_trace_structure.md) | 2025-06-22 | This document defines the internal structure and semantics of `reasoning_trace` used in AI-TCP packets, enabling traceability and chain-of-thought modeling among LLMs. |
| [RFC 012: AI Packet Conflict Resolution in AI-TCP](../012_conflict_resolution.md) | 2025-06-22 | Resolution strategies and metadata flags for handling packet-level conflicts. |

---

# 📑 AI-TCP RFC ドラフト (改訂版)

本ドキュメントは、主要な仕様に焦点を当てたAI-TCP RFCドラフトの改訂版リストを提示します。

| タイトル | 作成日 | 概要 |
| :------- | :----- | :--- |
| [RFC 001: AI-TCP プロトコル概要](001_ai_tcp_overview.md) | 2025-06-22 | AI-TCPは、YAML、グラフペイロード（Mermaid）、および追跡可能な推論を使用する、AI間通信のための軽量で構造化されたプロトコルです。 |
| [RFC 002: AI-TCPにおけるLLMコンプライアンス層](002_llm_compliance.md) | 2025-06-22 | 本ドキュメントは、AI-TCP通信に参加する大規模言語モデル（LLM）のコンプライアンス要件を定義します。 |
| [RFC 003: AI-TCP パケット構造定義](003_packet_definition.md) | 2025-06-22 | 本ドキュメントは、AI-TCP準拠パケットの構造と最小限の必須フィールドを形式化します。これらのパケットは、AI-TCPプロトコル下でのLLM間の通信の最小単位として機能します。 |
| [RFC 004: 推論トレースと思考チェーン構造](004_reasoning_trace_structure.md) | 2025-06-22 | 本ドキュメントは、AI-TCPパケットで使用される`reasoning_trace`の内部構造とセマンティクスを定義し、LLM間の追跡可能性と思考チェーンモデリングを可能にします。 |
| [RFC 012: AI-TCPにおけるAIパケット競合解決](../012_conflict_resolution.md) | 2025-06-22 | パケットレベルの競合を処理するための解決戦略とメタデータフラグ。 |