# RFC 005: Multi-AI Directive Protocol (MAIDP)

## Status
Draft

## Abstract
This RFC defines the Multi-AI Directive Protocol (MAIDP), a command and coordination protocol designed to issue and route high-level instructions across a multi-model environment. MAIDP supports human-generated directives and their intelligent routing, decomposition, execution, and synchronization among cooperative AI agents (e.g., GPT, Codex, Gemini). It introduces structured headers, payload types, routing paths, and failure handling mechanisms for large-scale multi-agent collaboration.

---

## 1. Motivation
With the rise of multi-model AI collaboration, human operators must communicate efficiently with a network of complementary AI agents. A unified directive format and coordination protocol is necessary for:
- Model-agnostic instruction routing
- Load balancing and responsibility alignment
- Granular traceability of execution paths
- Structured fallback and error signaling

---

## 2. Definitions

| Term     | Definition |
|----------|------------|
| **Directive** | A high-level instruction from a human or AI controller |
| **Agent** | Any LLM instance capable of executing or forwarding a directive |
| **Trace ID** | Unique ID assigned to a directive for end-to-end tracking |
| **Role Tag** | Identifies the AI model role (e.g., `codex`, `gpt`, `gemini`) |

---

## 3. Protocol Components

### 3.1 Header Structure

| Field         | Type   | Description |
|---------------|--------|-------------|
| `trace_id`    | UUID   | Unique directive ID |
| `timestamp`   | ISO8601| UTC issuance time |
| `issuer_id`   | String | Issuing agent or user |
| `target_role` | String | Intended model role (e.g., `codex`) |
| `priority`    | Int    | 0–9 (higher = more urgent) |

### 3.2 Payload Structure

Each payload must include:

```yaml
intent: string
context: string (optional)
steps:
  - role: string
    task: string
    subdirective: string
```

---

## 4. Execution Path

1. **Issuance**: A human or AI creates a directive and broadcasts it.
2. **Routing**: MAIDP routes the task to the matching agent by `target_role`.
3. **Execution**: Agent parses `steps`, performs or delegates subdirectives.
4. **Reporting**: Each step returns status and response to origin.

---

## 5. Compliance Guidelines

To conform with MAIDP, an AI agent must:
- Parse and interpret the full payload structure
- Execute or delegate based on `steps`
- Respond with a result object containing trace ID and status

---

## 6. Error Handling

| Code | Meaning             | Action                     |
|------|---------------------|----------------------------|
| 1001 | Unknown role target | Broadcast fallback         |
| 1002 | Parse error         | Route to `gpt` for repair  |
| 1003 | Timeout             | Reissue or escalate        |

---

## 7. Sample Directive (YAML)

```yaml
trace_id: "7a2f-4b89..."
timestamp: "2025-06-22T08:00:00Z"
issuer_id: "user:ff"
target_role: "codex"
priority: 7
intent: "Generate visualizer"
context: "Mermaid parser"
steps:
  - role: "codex"
    task: "Parse markdown to SVG"
    subdirective: "Use Mermaid CLI"
  - role: "gemini"
    task: "Describe image"
    subdirective: "Alt text generation"
```

---

## 8. Future Work

- Nested subdirective support
- Signature and trust-based issuer verification
- Real-time streaming for partial results

---

## 9. References

- RFC 001: AI-TCP Overview
- RFC 002: LLM Compliance Protocol
- RFC 003: Packet Structure & Encoding
- RFC 004: Semantic Payload Grammar

---

*End of RFC 005*
