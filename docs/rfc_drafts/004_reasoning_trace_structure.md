# RFC 004: Reasoning Trace & Thought Chain Structure

## 1. Purpose

This document defines the internal structure and semantics of `reasoning_trace` used in AI-TCP packets, enabling traceability and chain-of-thought modeling among LLMs.

## 2. Rationale

To support explainable and auditable AI interactions, each LLM must expose its reasoning process in a standardized format. This RFC builds upon RFC 002 and defines additional structure, conventions, and interpretability guidance.

## 3. Core Structure

A `reasoning_trace` is an ordered array of steps.

### Example:

```yaml
reasoning_trace:
  - step: 1
    input: "User requested a document summary"
    output: "Identified task: summarization"
  - step: 2
    input: "Identified task: summarization"
    output: "Delegating to summarization module"
```

## 4. Fields Per Step

| Field   | Type   | Description                                |
|---------|--------|--------------------------------------------|
| `step`  | int    | Sequential identifier (1-based)            |
| `input` | string | Observed or inherited state/context        |
| `output`| string | Action, inference, or outcome at this step |

## 5. Extended Semantics

- Input/output should form a causal chain
- The `output` of step N becomes the `input` of step N+1 (unless overridden)
- Branching structures should be indicated explicitly via `fork:` or `condition:` (future RFC may expand)

## 6. Integrity Rules

- Steps must be strictly ordered (ascending `step`)
- Missing `input` or `output` renders the trace invalid
- Additional fields are permitted (e.g., `module`, `confidence`) but must not overwrite core semantics

## 7. Interoperability

To be interoperable across LLMs:

- Each trace step must be interpretable independently
- Ambiguity in field names or reasoning transitions must be avoided
- Cross-model trace translation may be needed (see RFC 005: Diagnostics)

## 8. Visualization Notes

Future tooling may visualize reasoning chains using flowchart-like semantics.
Trace logs may be converted into Mermaid for human inspection or debugging.

## 9. Reference

- RFC 001: AI-TCP Protocol Overview
- RFC 002: LLM Compliance
- RFC 003: Packet Structure Definition
