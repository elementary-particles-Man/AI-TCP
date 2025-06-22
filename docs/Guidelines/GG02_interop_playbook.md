# GG02: AI-TCP Interoperability Playbook

## 1. Purpose

This document provides interoperability patterns, bridging strategies, and template responses for systems exchanging AI-TCP packets across differing implementations, LLM types, or protocol versions.

## 2. Scenarios Addressed

- LLM A (GPT-4) communicates with LLM B (custom agent with partial compliance)
- AI-TCP v1.0 node interacts with legacy YAML-only clients
- Graph semantics vary across implementations

## 3. Interop Principles

| Principle             | Description |
|-----------------------|-------------|
| Structural Tolerance  | Accept known-safe deviations in trace or graph format |
| Explicit Declaration  | Always define `llm_profile.version` and capabilities |
| Semantic Isolation    | Do not infer across unknown fields or altered graphs |
| Fallback Compatibility| Define minimal set of fields for degraded operation |

## 4. Interop Templates

### 4.1 Minimal Response Template

```yaml
reasoning_trace:
  - step: 1
    input: "request received"
    output: "acknowledged"
llm_profile:
  id: agent-bridge
  version: 0.9
```

### 4.2 Compatibility Notice Packet

```yaml
reasoning_trace:
  - step: 1
    input: "unsupported field detected"
    output: "switching to fallback profile"
auto_redirect:
  type: profile_switch
  next_profile: legacy_mode
```

## 5. Bridging Adapters

- YAML Normalizer: strips unknown fields and flattens nested objects
- Graph Simplifier: translates Mermaid graphs into basic flowcharts
- Trace Translator: renames fields to RFC002-compliant keys

## 6. Capability Declaration (LLM Side)

Include this in `llm_profile` to inform interop logic:

```yaml
llm_profile:
  id: gpt4
  version: 4.3
  capabilities:
    accepts_auto_redirect: true
    supports_mermaid_graphs: false
    schema_mode: lax
```

## 7. Legacy Handling

If communicating with non-AI-TCP systems:

- Only use `reasoning_trace` and `meta` (no `graph_payload`)
- Avoid Mermaid-specific fields
- Use `llm_profile.version: 0.x` to indicate compatibility bridge mode

## 8. Reference

- RFC 001–004
- GG01: Operational Practices
