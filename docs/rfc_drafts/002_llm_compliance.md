# RFC 002: LLM Compliance Layer in AI-TCP

## 1. Overview
This document defines the compliance requirements for Large Language Models (LLMs) participating in AI-TCP communication.

## 2. Goals
- Ensure consistent interpretation of YAML packets
- Establish standard fields required by all LLMs
- Enable future-proof trace and feedback handling

## 3. Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `reasoning_trace` | array | Ordered log of internal logic |
| `llm_profile` | object | Metadata about the participating LLM |
| `auto_redirect` | object | Optional feedback routing structure |

## 4. Validation Rules
- Trace must be an ordered list with timestamps
- `llm_profile.id` and `.version` are mandatory
- `auto_redirect` must not overwrite prior trace context

## 5. Example YAML
```yaml
reasoning_trace:
  - step: 1
    input: "Request: Determine action"
    output: "Action: Evaluate"
llm_profile:
  id: GPT-4
  version: 2025.3
auto_redirect:
  type: feedback
  next_action: explain
