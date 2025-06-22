# GG03: Fault Handling Structures for AI-TCP

## 1. Purpose

This guideline defines standard procedures and fallback strategies to handle errors, inconsistencies, and failures encountered during AI-TCP communication across systems.

## 2. Fault Categories

| Category     | Code | Description |
|--------------|------|-------------|
| SYNTAX_ERROR | F01  | Malformed YAML or unrecognized packet format |
| TIMEOUT      | F02  | No response received within specified TTL |
| VERSION_MISMATCH | F03 | Incompatible `llm_profile.version` |
| GRAPH_FAILURE | F04 | Mermaid rendering or graph structure error |
| COMPLIANCE_FAIL | F05 | Violation of declared LLM compliance level |

## 3. Fault Packet Template

```yaml
fault_packet:
  code: F03
  message: "Protocol version mismatch"
  resolution_suggested: "Request fallback profile or YAML-normalized format"
  trace_id: session-8249-error
```

## 4. Fallback Strategies

| Code | Action                            |
|------|-----------------------------------|
| F01  | Parse with `strict: false`, strip unknown fields |
| F02  | Retry with exponential backoff (up to 3x) |
| F03  | Request updated `llm_profile` declaration |
| F04  | Convert graph into bullet-point trace |
| F05  | Notify sender with minimal accepted packet format |

## 5. Diagnostic Trace Format

Append to `reasoning_trace` upon fault:

```yaml
reasoning_trace:
  - step: 9
    input: "received malformed graph"
    output: "initiating graph_fallback"
    meta:
      fault_code: F04
      fallback_used: true
```

## 6. Fault Broadcast (Optional)

Systems may broadcast unresolved faults for auditing:

```yaml
fault_broadcast:
  system: ai-node-73
  fault:
    code: F01
    timestamp: 2025-06-22T14:53:21Z
    criticality: high
```

## 7. Recovery Patterns

- Use `auto_redirect` to delegate to a simplified or legacy agent
- Include `fault_packet` in response when dropping session
- Declare `fallback_used: true` in meta or trace block

## 8. References

- RFC 002: Compliance Modes
- RFC 003: AI-TCP Packet Structure
- GG02: Interop Playbook
