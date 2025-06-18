# Proof-of-Concept Design Overview for AI-TCP

This directory contains the design structure and logical relationships of the **Direct Mental Care (DMC)** use-case implemented in AI-TCP framework.

---

## 📂 File Structure & Purpose

| File/Folder                                                       | Purpose                                                                       |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `direct_mental_care.yaml`                                         | Structured YAML representing the PoC phase and packet outline for DMC session |
| `../structured_yaml/validated_yaml/ai_tcp_dmc_trace.yaml`         | Detailed trace log in YAML format (Codex and Gemini collaborative output)     |
| `../../dmc_sessions/trace_packets/gemini_dmc_session_20250618.md` | Original narrative trace (Gemini-generated)                                   |
| `../../gen_dmc_html.py`                                           | Python script for HTML rendering of YAML session                              |
| `../../DMC_20250618.html`                                         | Final human-readable HTML page generated from YAML session                    |
| `../../structured_yaml/README.yaml.md`                            | Meta-documentation on YAML schema hierarchy                                   |
| `../../schemas/ai_tcp_packet.schema.yaml`                         | YAML schema reference for packet validation (optional)                        |

---

## 🔁 Logical Flow

```mermaid
flowchart TD
    Start["User Session Initiation"] --> Gemini["Gemini generates narrative trace (MD)"]
    Gemini --> Codex["Codex maps YAML trace based on AI-TCP format"]
    Codex --> HTMLGen["gen_dmc_html.py renders HTML"]
    HTMLGen --> Output["DMC_20250618.html"]
---

## 🧭 Navigation Map

* 📄 Narrative Log → `dmc_sessions/trace_packets/gemini_dmc_session_20250618.md`
* 🧾 Validated Trace → `structured_yaml/validated_yaml/ai_tcp_dmc_trace.yaml`
* 🧠 Render Engine → `gen_dmc_html.py`
* 🌐 Final Output → `DMC_20250618.html`

---

## 📌 Notes

* This design validates the **AI-TCP packet model** and supports **LSC-based direct intervention scenarios**.
* YAML structure complies with `master_schema_v1.yaml` for consistency and integration.
🔍 See also: [README_Gemini.md](README_Gemini.md) — Narrative and architectural rationale by Gemini
📊 YAML structure analysis available at [analysis/ai_tcp_dmc_trace_structure.md](analysis/ai_tcp_dmc_trace_structure.md)

---

© 2025 [elementary-particles-Man](https://github.com/elementary-particles-Man)

---
