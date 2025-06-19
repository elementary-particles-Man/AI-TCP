# 🧬 DMC YAML Template / DMC YAMLテンプレート

This is a reference template for AI-TCP DMC YAML format.\
本テンプレートは AI-TCP DMC 構造に基づく YAML 記述の雛形です。

---

## 🧾 YAML Template

```yaml
id: "session-xxx"
timestamp: "YYYY-MM-DDTHH:MM:SSZ"
lang: "en"
phase: "pre_assessment"
agent: "gpt-4o"
tags:
  - "example"
  - "prototype"
meta:
  version: "1.0.0"
  source: "system-initial"
data:
  input: "Describe the user's current concern."
  output: "User indicates mild anxiety about job security."
```

---

## 🔗 Related Specifications / 関連仕様

- [`ai_tcp_yaml_structure.md`](./ai_tcp_yaml_structure.md)
- [`ai_tcp_metadata_fields.md`](./ai_tcp_metadata_fields.md)
- [`ai_tcp_phase_definition.md`](./ai_tcp_phase_definition.md)

---

*Last updated: 2025-06-20*

