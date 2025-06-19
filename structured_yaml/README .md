# 📁 `structured_yaml/` Directory Overview

This directory contains structured YAML files used in AI-TCP Proof-of-Concept (PoC) sessions.  \
本ディレクトリは AI-TCP の PoC セッションにおいて使用される構造化 YAML ファイルを収めています。

---

## 📐 Naming Convention / 命名規則

Each file follows the format:

```
<session_type>_<domain>_<serial>.yaml
```

Examples:

- `dmc_mental_001.yaml` – DMC session for mental health
- `tcp_logic_001.yaml` – TCP session for logical reasoning

For full specification, see [`session_naming_convention.md`](../docs/spec/session_naming_convention.md).

---

## 📦 File Contents / ファイル内容

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

- [`ai_tcp_yaml_structure.md`](../docs/spec/ai_tcp_yaml_structure.md)
- [`ai_tcp_metadata_fields.md`](../docs/spec/ai_tcp_metadata_fields.md)
- [`ai_tcp_phase_definition.md`](../docs/spec/ai_tcp_phase_definition.md)

---

## 🔄 Use Case / 利用目的

- Document PoC interactions in structured format
- Enable reproducible testing, validation, and documentation
- Facilitate HTML rendering, YAML-to-JSON transformation, and UI integration

---

*Last updated: 2025-06-20*

