# 📑 AI-TCP Metadata Fields Specification / メタデータ項目定義

This document defines standard metadata fields used in AI-TCP YAML structures.  
本書は AI-TCP の YAML 構造で共通使用されるメタデータ項目について定義します。

---

## 🧾 Field List

| Field Name   | Type              | Required | Description (EN)                              | 説明（日本語）                                 |
|--------------|-------------------|----------|-----------------------------------------------|------------------------------------------------|
| `id`         | string            | Yes      | Unique identifier for the session or object   | セッションまたはオブジェクトの一意識別子       |
| `timestamp`  | string (ISO8601)  | Yes      | Time of the event or record creation          | イベントまたは記録の作成時刻（ISO形式）        |
| `lang`       | string            | Yes      | Language code (e.g., `en`, `ja`)              | 入出力に使われる言語コード                     |
| `tags`       | array of strings  | No       | Classification or custom labels               | 分類用またはカスタムラベル                      |
| `phase`      | enum              | Yes      | Processing stage (see phase definition)       | 処理段階（詳細は `ai_tcp_phase_definition.md` 参照） |
| `agent`      | string            | No       | Agent name or role in the session             | セッションにおけるエージェント名または役割     |
| `version`    | string (semver)   | No       | AI-TCP or PoC schema version                  | 適用される AI-TCP または PoC スキーマのバージョン |
| `source`     | string            | No       | Input origin or reference ID                  | 入力元または関連識別子                         |
| `notes`      | string            | No       | Free text comment or annotation               | コメントまたは注記                              |

---

## 📘 Notes

- Fields marked **Required = Yes** must be included in all YAML blocks.
- `phase` must match one of the entries defined in `ai_tcp_phase_definition.md`.
- `timestamp` should follow **ISO 8601 extended format** (e.g., `2025-06-20T09:00:00Z`).
- `tags` can be used for any custom internal processing or UI filtering.
- This specification is versioned and subject to augmentation as AI-TCP evolves.

---

_Last updated: 2025-06-20_

