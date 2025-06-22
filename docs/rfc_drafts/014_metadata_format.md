# RFC 014: Unified Metadata Format for AI-TCP Packets

## 1. Introduction
This RFC defines a unified metadata header used in all AI-TCP packets exchanged between Large Language Models (LLMs). A consistent metadata format simplifies validation, orchestration, and auditing across diverse nodes.

## 2. Metadata Format
The header is a YAML or JSON object placed at the beginning of every packet. Fields are case-sensitive and use `snake_case` naming.

## 3. Required Fields
| Field | Type | Description |
|-------|------|-------------|
| `llm_id` | string | Identifier of the generating or target LLM |
| `language` | string | BCP-47 or ISO 639 language code for the payload |
| `timestamp` | string | UTC timestamp in ISO 8601 format |
| `compliance` | string | RFC or policy version that governs packet structure |

## 4. Optional Fields
| Field | Type | Description |
|-------|------|-------------|
| `trace_id` | string | Unique identifier for tracking across packets |
| `role` | string | Agent role or capability tag |
| `tags` | array of strings | Free-form labels for routing or auditing |

## 5. Field Validation and Defaults
- `llm_id` must match `[A-Za-z0-9._-]+`.
- `language` defaults to `en` if omitted.
- Invalid or missing `timestamp` values trigger rejection.
- `compliance` defaults to `RFC003` if not provided.

## 6. Usage in Validation and Orchestration
AI-TCP orchestration layers SHALL validate these fields before further processing. Packets failing validation MAY be quarantined or returned with an error. The metadata header is also logged to the reasoning trace for audit purposes.

## 7. Example Header
```yaml
meta:
  llm_id: gpt-4
  language: en
  timestamp: 2025-06-22T00:00:00Z
  compliance: RFC003
  trace_id: abc123
  role: assistant
  tags: [demo, rfc014]
```

## 8. Status
Draft – Last updated: 2025-06-22
