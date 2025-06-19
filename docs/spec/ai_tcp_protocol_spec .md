# AI-TCP Protocol Specification

This document defines the core protocol used in AI-TCP (Artificial Intelligence - Thought Communication Protocol), designed to facilitate structured, layered, and traceable communication between AI agents and humans.

---

## 🧠 1. Purpose

AI-TCP is a protocol aimed at:

- Structuring semantic-rich exchanges between agents
- Enabling modular multi-phase dialog sessions
- Supporting traceability, validation, and multi-language rendering
- Forming the basis for inter-agent and human-AI collaboration over time

---

## 📦 2. Packet Structure

### Base YAML Fields

| Field          | Type     | Required | Description                                      |
|----------------|----------|----------|--------------------------------------------------|
| `trace_id`     | string   | ✅       | Unique ID linking messages across phases        |
| `phase`        | string   | ✅       | Semantic phase tag (e.g., `phase1`, `phase2`)   |
| `topic`        | string   | ✅       | Human-readable theme of the exchange            |
| `content`      | string   | ✅       | The core communicative message (may be multiline)|
| `emotion_tag`  | string   | ⭕       | Optional tone/emotional classification           |
| `metadata`     | object   | ⭕       | Optional runtime/environment context             |

---

## 🔄 3. Communication Flow

### Multi-Phase Session Model

| Phase    | Description                       |
|----------|-----------------------------------|
| Phase 1  | Initial engagement / rapport setup|
| Phase 2  | Emotional reflection              |
| Phase 3  | Decision support / prompting      |
| Phase 4  | Closure / future orientation      |

Each phase must reference the `trace_id` to preserve continuity. Transitioning between phases can be conditional or sequential depending on application logic.

---

## 🧩 4. Validation Logic

- All packets must conform to `ai_tcp_packet.schema.yaml`
- Conditional fields (e.g., `emotion_tag`) must comply with enumerated lists defined in `schemas/`
- Bidirectional traceability must be ensured via `trace_link_summary_mapping.md`

---

## 🌐 5. Internationalization Support

- Native YAML is designed to be translation-ready.
- Tools such as `generate_yaml_schema_doc.py` enable language-neutral documentation generation.
- Locale suffixes (e.g., `_ja`, `_en`) apply to both schema-derived output and narrative logs.

---

## 🔒 6. Security & Authenticity (Planned)

- Optional cryptographic signing of packets using `metadata.signature`
- Timestamping and hash-chaining for regulatory integrity

---

## 🧱 7. File/Directory Integration

| Category             | Directory               |
|----------------------|-------------------------|
| Schemas              | `schemas/`              |
| PoC Data Packets     | `structured_yaml/`      |
| Validation Scripts   | `scripts/`, `tools/`    |
| Narrative Sessions   | `dmc_sessions/`         |
| Protocol Spec Docs   | `docs/spec/`            |

---

## 📚 8. Related Documents

- PoC Mapping Table → [ai_tcp_poc_mapping.md](./ai_tcp_poc_mapping.md)
- YAML Schema → [ai_tcp_packet.schema.yaml](../../schemas/ai_tcp_packet.schema.yaml)
- Trace Link Map → [trace_link_summary_mapping.md](../../dmc_sessions/analysis/trace_link_summary_mapping.md)

---

## 📄 9. Future Enhancements

- RFC-compliant version for IETF Internet-Draft
- Integration with CI/CD test automation
- AI-side introspection layer over `metadata.agent_state`

---

この `ai_tcp_protocol_spec.md` によって、AI-TCPプロトコルの「基本パケット構造」「会話遷移」「ファイル連携」「多言語展開」などの中核定義が文書化されました。

---

次に、PoC成果物とこの仕様書の「対応関係マッピング表（[5/5] `ai_tcp_poc_mapping.md`）」を作成します。よろしければ進めます。
