# RFC 003: AI-TCP Packet Structure Definition

## 1. Purpose
This document formalizes the structure and minimal required fields for AI-TCP-compliant packets. These packets serve as the atomic units of communication between LLMs under the AI-TCP protocol.

## 2. Root Structure

Each packet must be a valid YAML document with the following top-level fields:

| Key              | Type   | Description |
|------------------|--------|-------------|
| `graph_payload`  | object | Contains an embedded conceptual graph in Mermaid format |
| `reasoning_trace`| array  | Sequence of reasoning steps with I/O mapping |
| `meta`           | object | Metadata such as timestamp, source, and packet type |
| `llm_profile`    | object | Information about the sending/receiving LLM |
| `auto_redirect`  | object | Optional: Follow-up routing or delegation instructions |

## 3. Field Definitions

### 3.1 graph_payload
Encapsulates the mental model structure using Mermaid.

```yaml
graph_payload:
  graph_structure: |
    mmd:flowchart TD
    A[Start] --> B[Validate]
```

The `graph_structure` string must begin with the prefix `mmd:` and follow Mermaid syntax (see RFC 001 for semantics).

### 3.2 reasoning_trace

```yaml
reasoning_trace:
  - step: 1
    input: "Request: Analyze"
    output: "Action: Forward to module"
```

Each item must include a step number, input, and output fields. The trace logs the AI's observable reasoning path.

### 3.3 meta

```yaml
meta:
  timestamp: 2025-06-22T12:00:00Z
  origin: ai-core
  type: interaction
```

`meta` must provide minimally a timestamp and source. Additional fields are permitted for contextualization.

### 3.4 llm_profile

```yaml
llm_profile:
  id: GPT-4
  version: 2025.3
```

Indicates the identity of the participating model.

### 3.5 auto_redirect

```yaml
auto_redirect:
  type: feedback
  next_action: clarify
```

Used to propagate an intent or defer reasoning to another handler.

## 4. Constraints

- All listed fields must appear at the top level of the YAML document.
- `graph_structure` must be a string literal starting with `mmd:` and contain valid Mermaid.
- Fields must not conflict or overwrite each other.
- Unknown fields may be ignored unless otherwise specified.

## 5. Minimal Packet Example

```yaml
graph_payload:
  graph_structure: |
    mmd:flowchart TD
    X[Init] --> Y[Parse]
reasoning_trace:
  - step: 1
    input: Start
    output: Parsed
meta:
  timestamp: 2025-06-22T01:00:00Z
  origin: ai-core
  type: request
llm_profile:
  id: GPT
  version: 4.0
auto_redirect:
  type: followup
  next_action: respond
```

## 6. Reference

- RFC 001: AI-TCP Protocol Overview
- RFC 002: LLM Compliance Layer
- YAML Core 1.2 Specification
- Mermaid JS Documentation
