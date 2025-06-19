# 🗂 AI-TCP YAML Structure Specification / YAML構造仕様

This document defines the canonical structure of YAML files used in AI-TCP sessions.  
本書は AI-TCP セッションで使用される YAML ファイルの正規構造を定義します。

---

## 🔧 Root-Level Structure / ルート構造

```yaml
id: string
timestamp: ISO8601
lang: string
phase: enum
agent: string
tags:
  - string
meta:
  version: string
  source: string
data:
  input: string or object
  output: string or object
```

---

## 🔍 Structure Rules / 構造規則

- `id`, `timestamp`, `lang`, `phase` は **必須** フィールドです。
- `meta` は任意項目ですが、可能であれば `version` を含めてください。
- `tags` は文字列配列として任意に付与できます。
- `data.input` と `data.output` はともに **必須**。値は string またはオブジェクトを許容します。
- YAMLファイル1つにつき、ルート構造ブロックは **1個だけ** 存在する必要があります。

---

## 🔗 Field References / フィールド仕様参照

- 詳細なフィールド仕様については `ai_tcp_metadata_fields.md` を参照してください。
- `phase` の定義は `ai_tcp_phase_definition.md` に従ってください。

---

## 🧪 Example Template / 使用例テンプレート

```yaml
id: "session-001"
timestamp: "2025-06-20T09:00:00Z"
lang: "en"
phase: "intervention"
agent: "gpt-4o"
tags:
  - "triage"
  - "mental-care"
meta:
  version: "1.0.0"
  source: "user-input/mental-check"
data:
  input: "I feel anxious."
  output: "I'm here to help. Can you tell me more about what's bothering you?"
```

---

_Last updated: 2025-06-20_

