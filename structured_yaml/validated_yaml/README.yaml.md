# **Validated YAML Definitions (structured\_yaml/validated\_yaml/)**

このフォルダは、AI-TCPプロトコルにおいて整合性検証済みのYAML定義ファイルを格納しています。すべてのファイルは master\_schema\_v1.yaml に準拠しており、Codex・Gemini・GPTなどのAIエージェントによるPoC実装やメンタルケア実験（DMC）に活用されています。

## **各ファイルの詳細**

### **ai\_tcp\_dmc\_trace.yaml**

| 項目 | 内容 |
| :---- | :---- |
| **概要** | Direct Mental Care (DMC)セッションの具体的な対話ログと、各応対の裏にあるAIの思考プロセス（Intent, Justification等）を構造化したトレース定義です。 |
| **スキーマ依存** | master\_schema\_v1.yaml |
| **関連資料** | 元データ: dmc\_sessions/trace\_packets/gemini\_dmc\_session\_20250618.md 出力先: docs/generated/DMC\_20250618.html |
| **使用目的** | AIによる心理ケアセッションの事後分析、思考プロセスの透明性確保、およびセッション再生UIのデータソースとして使用されます。 |

### **ai\_tcp\_poc\_design.yaml**

| 項目 | 内容 |
| :---- | :---- |
| **概要** | AI-TCPプロトコルの技術的な概念実証（PoC）に関する全体設計（アーキテクチャ、パケット構造、エラー処理等）を定義します。 |
| **スキーマ依存** | master\_schema\_v1.yaml |
| **関連資料** | rfc\_ai\_tcp\_dmc\_poc.md, rfc\_magi\_system.md |
| **使用目的** | 異なるAIエージェント（GPT, Gemini等）を用いたプロトタイプ実装における共通の技術仕様書として機能し、開発の指針となります。 |

### **ai\_tcp\_timeline.yaml**

| 項目 | 内容 |
| :---- | :---- |
| **概要** | AI-TCPおよび関連プロジェクト（Magi System, LSC等）の制定経緯と主要なマイルストーンを時系列で記録した定義ファイルです。 |
| **スキーマ依存** | master\_schema\_v1.yaml |
| **関連資料** | ai\_tcp\_history\_timeline.md |
| **使用目的** | プロジェクト全体の進捗管理、新規参加者への背景情報提供、および将来の参照のための公式な歴史的経緯の保存に使用されます。 |

