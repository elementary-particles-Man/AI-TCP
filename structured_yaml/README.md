# 📁 `structured_yaml/` Directory Overview

This directory contains structured YAML files used in AI-TCP Proof-of-Concept (PoC) sessions. These files are crucial for documenting PoC interactions in a structured format, enabling reproducible testing, validation, and documentation, and facilitating HTML rendering, YAML-to-JSON transformation, and UI integration.

## 📐 Naming Convention

Each file follows the format:

```
<session_type>_<domain>_<serial>.yaml
```

Examples:

*   `dmc_mental_001.yaml` – DMC session for mental health
*   `tcp_logic_001.yaml` – TCP session for logical reasoning

For full specification, see [`session_naming_convention.md`](../docs/spec/session_naming_convention.md).

## 📦 File Contents

Each YAML file includes the following structure:

```yaml
id: "<unique_session_id>"
timestamp: "<ISO8601 time>"
lang: "en" | "ja" | ...
phase: "pre_assessment" | "intervention" | "decision" | ...
agent: "gpt-4o" | ...
tags: [ "keyword1", "keyword2", ... ]
meta:
  version: "<schema_version>"
  source: "<origin>"
data:
  input: |
    <User input or scenario prompt>
  output: |
    <AI-generated response>
```

See full schema details at:

*   [`ai_tcp_yaml_structure.md`](../docs/spec/ai_tcp_yaml_structure.md)
*   [`ai_tcp_metadata_fields.md`](../docs/spec/ai_tcp_metadata_fields.md)
*   [`ai_tcp_phase_definition.md`](../docs/spec/ai_tcp_phase_definition.md)

## 🌐 View as HTML

Generated HTML version of these YAML sessions is available at:

➡️ [`generated_html/structured_yaml_index.html`](../generated_html/structured_yaml_index.html)

In the HTML version, all sessions are listed with styling.

## 🔧 YAML Structure Separation Policy

*   `master_schema_v1.yaml` is the foundational structure for the entire AI-TCP.
*   Please split it as needed, as follows:

| Module Name | Purpose |
| :---------- | :------ |
| `llm_compliance_v1.yaml` | Syntax and structural requirements to be observed between LLMs |
| `packet_structure_v1.yaml` | Required keys and semantic descriptions for the packet body |
| `reason_trace_v1.yaml` | Format of reasoning logs (trace) |

*   For splitting, use `$ref:` comment notation to maintain connectivity with higher-level structures.

---

# 📁 `structured_yaml/` ディレクトリ概要

本ディレクトリは、AI-TCPの概念実証（PoC）セッションで使用される構造化YAMLファイルを格納しています。これらのファイルは、PoCのインタラクションを構造化された形式で文書化し、再現可能なテスト、検証、ドキュメント化を可能にし、HTMLレンダリング、YAMLからJSONへの変換、UI統合を容易にする上で非常に重要です。

## 📐 命名規則

各ファイルは以下の形式に従います：

```
<session_type>_<domain>_<serial>.yaml
```

例:

*   `dmc_mental_001.yaml` – メンタルヘルス向けDMCセッション
*   `tcp_logic_001.yaml` – 論理的推論向けTCPセッション

完全な仕様については、[`session_naming_convention.md`](../docs/spec/session_naming_convention.md) を参照してください。

## 📦 ファイル内容

各YAMLファイルは以下の構造を含みます：

```yaml
id: "<一意のセッションID>"
timestamp: "<ISO8601形式の時刻>"
lang: "en" | "ja" | ...
phase: "pre_assessment" | "intervention" | "decision" | ...
agent: "gpt-4o" | ...
tags: [ "キーワード1", "キーワード2", ... ]
meta:
  version: "<スキーマバージョン>"
  source: "<オリジン>"
data:
  input: |
    <ユーザー入力またはシナリオプロンプト>
  output: |
    <AI生成応答>
```

完全なスキーマの詳細は以下を参照してください：

*   [`ai_tcp_yaml_structure.md`](../docs/spec/ai_tcp_yaml_structure.md)
*   [`ai_tcp_metadata_fields.md`](../docs/spec/ai_tcp_metadata_fields.md)
*   [`ai_tcp_phase_definition.md`](../docs/spec/ai_tcp_phase_definition.md)

## 🌐 HTMLで閲覧

これらのYAMLセッションの生成されたHTML版は以下で利用可能です：

➡️ [`generated_html/structured_yaml_index.html`](../generated_html/structured_yaml_index.html)

HTML版では、すべてのセッションがスタイル付きで一覧表示されます。

## 🔧 YAML構造の分離方針

*   `master_schema_v1.yaml` はAI-TCP全体の基盤構造です。
*   必要に応じて以下のように分割してください：

| モジュール名 | 用途 |
| :----------- | :--- |
| `llm_compliance_v1.yaml` | LLM間で守るべき構文と構造要件 |
| `packet_structure_v1.yaml` | パケット本体の必須キーと意味記述 |
| `reason_trace_v1.yaml` | 推論ログ（トレース）の形式 |

*   分割には `$ref:` コメント記法を用い、上位構造との接続性を保ちます。