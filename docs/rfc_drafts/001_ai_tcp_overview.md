# RFC 001: AI-TCP Protocol Overview

## 1. Purpose
AI-TCP is a lightweight, structured protocol for inter-AI communication using YAML, Graph Payloads (Mermaid), and traceable reasoning.

## 2. Terminology
- **LLM**: Large Language Model
- **Packet**: A YAML-encoded unit containing trace, graph_payload, metadata
- **Compliance Layer**: Structural expectations for interpreting packets

## 3. Architecture
- YAML-based packet structure
- Trace log → Reasoning transfer
- Graph structure → Mental model embedding

## 4. Packet Lifecycle
1. Construct YAML with `graph_payload`, `reasoning_trace`
2. Send to receiving LLM
3. Receiving LLM parses structure
4. Optionally replies with `auto_redirect` and updated context

### YAML Integration

AI-TCP packets are encoded as standard YAML documents. The structure follows the specification defined in [RFC 003](003_packet_definition.md).

Each packet includes reasoning logs, profile metadata, and an embedded graph structure representing mental models.

```yaml
graph_payload:
  graph_structure: |
    mmd:flowchart TD
    A[Start] --> B[Parse YAML]
    B --> C{Validate}
    C --> D[Reasoning]
    D --> E[Reply]
reasoning_trace:
  - step: 1
    input: Receive
    output: Parse and Validate
llm_profile:
  id: GPT-4
  version: 2025.3
```

The `graph_structure` field begins with the `mmd:` prefix to indicate Mermaid encoding. The receiving LLM interprets this structure in conjunction with the reasoning trace to determine its next action.

## 5. Security & Scope
AI-TCP is intended for inter-AI communication, not for user-facing authentication or cryptographic security.

## 6. Reference
- YAML Core 1.2
- Mermaid JS 10+
- AI-TCP PoC 2025
