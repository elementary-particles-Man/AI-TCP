# AI-TCP PoC Mapping Table

This document outlines how each Proof of Concept (PoC) component corresponds to the AI-TCP protocol specification. It enables traceable validation between theoretical definitions and practical implementations.

---

## 🧭 1. Mapping Summary

| Specification Element          | Corresponding PoC Component                                     |
|-------------------------------|-----------------------------------------------------------------|
| `ai_tcp_packet.schema.yaml`   | `structured_yaml/direct_mental_care.yaml`                      |
| `trace_id`, `phase`, `topic`  | YAML keys validated via `validate_dmc_yaml.py`                 |
| Phase transitions              | `dmc_session_20250618_narrative.md` and `phase_map.html`       |
| Multi-phase model             | Defined in `docs/templates/readme_summary_template_*.md`       |
| Emotion tagging               | Seen in `emotion_tag` values in structured YAML                |
| Internationalization (i18n)   | `README_ja.md`, `README_en.md`, and HTML multilingual outputs  |
| Structural maps               | `dmc_session_20250618_causal_chain_en.md` (Mermaid diagram)    |
| Traceability validation       | `trace_link_summary_mapping.md`                               |
| PoC automation                | Scripts in `scripts/` and `tools/`                             |
| Markdown conversion           | `generate_yaml_schema_doc.py`, `gen_dmc_html.py`               |
| Documentation generation      | `generate_yaml_schema_doc.py` + templates                     |

---

## 🧩 2. YAML Schema–Driven Output Flow

```mermaid
flowchart TD
    A[ai_tcp_packet.schema.yaml] --> B[validate_dmc_yaml.py]
    B --> C[direct_mental_care.yaml]
    C --> D[generate_yaml_schema_doc.py]
    D --> E[HTML / MD documentation]
    C --> F[dmc_session_*.md (narrative)]
```

> 💡 **Note**: Mermaid diagrams require live preview in Obsidian.<br>
> Use `<br>` for all line breaks to prevent rendering errors.

---

## 🔍 3. Validation Points

- YAML files must conform to the schema definition.
- Phase progression must align with session logs.
- `trace_id` values must remain consistent across outputs.
- Translation output must preserve semantic accuracy.
- Output must render properly in both Obsidian and GitHub.

---

## 📚 4. Related Resources

- Protocol Spec: `ai_tcp_protocol_spec.md`
- DMC Session Narrative: `dmc_session_20250618_narrative.md`
- Trace Mapping: `trace_link_summary_mapping.md`
- Style Guide: `translation_style_guide.md`

---

## ✅ 5. Status

This mapping is up-to-date as of **2025-06-20**.  
Future PoC variants (e.g., Crisis Management or Judicial Arbitration) should duplicate this file and adapt it to the new use case.
