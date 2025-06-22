# RFC 002: LLM Compliance Layer in AI-TCP

## 1. Overview
This document defines the compliance requirements for Large Language Models (LLMs) participating in AI-TCP communication.

AI-TCP enables traceable, interpretable, and modular communication between autonomous AI agents. For such communication to succeed, participating LLMs must follow shared conventions in packet structure, field interpretation, and behavior.

## 2. Goals
- Ensure consistent interpretation of YAML packets across diverse LLM implementations
- Define mandatory fields that facilitate reasoning transparency and auditability
- Enable future-proof trace and feedback handling
- Support compatibility with AI-TCP core schema (see RFC 003)

## 3. Required Fields

| Field | Type   | Description |
|-------|--------|-------------|
| `reasoning_trace` | array  | Ordered log of internal reasoning steps |
| `llm_profile`     | object | Metadata describing the acting LLM |
| `auto_redirect`   | object | Optional field for chaining responses |

## 4. Field Semantics

### 4.1 reasoning_trace
A structured array that records input-output reasoning pairs for each step the LLM performs.

Example:
```yaml
reasoning_trace:
  - step: 1
    input: "Request: Determine action"
    output: "Action: Evaluate"
```

### 4.2 llm_profile
Identifies the LLM instance, its version, and optionally its behavioral configuration.

Example:
```yaml
llm_profile:
  id: GPT-4
  version: 2025.3
  profile: default
```

### 4.3 auto_redirect
Used to optionally route the response to a follow-up module or context.

Example:
```yaml
auto_redirect:
  type: feedback
  next_action: explain
```

## 5. Validation Rules

- `reasoning_trace` must be an ordered list. Each item must include both `input` and `output`.
- `llm_profile.id` and `llm_profile.version` are mandatory.
- `auto_redirect` must not overwrite or truncate any previous reasoning context.

## 6. Compliance Declaration

LLMs declaring AI-TCP compliance **must** expose a mechanism—implicit or explicit—that confirms conformance to this structure. This may take the form of:

- Explicit metadata fields
- API conformance
- Static schema binding

## 7. Security Considerations

This specification does not enforce cryptographic integrity or authentication. The focus is on structural interoperability, not security guarantees.

## 8. Reference

- RFC 001: AI-TCP Overview
- RFC 003: AI-TCP Packet Structure
- YAML 1.2 Specification
