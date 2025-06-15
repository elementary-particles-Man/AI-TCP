# AI-TCP Protocol Specification

This document consolidates the fields defined in `structured_yaml/validated_yaml/ai_tcp_poc_design.yaml` and describes the packet format for AI-TCP v1.0.

## Consolidated Field List

**Overview**
- **purpose**: Magi System LLM nodes coordination protocol definition
- **communication_targets**: nodes within Magi System

**Architecture**
- **design_principles**: IPv6 extension headers, lightweight and extensible
- **communication_method**: UDP-over-TCP style encapsulation after session setup

**Packet Structure**
- **session_id** (128-bit)
- **source_llm_id** (64-bit)
- **destination_llm_id** (64-bit)
- **metadata**
  - `message_type` (info/command/verification)
  - `priority` (high/medium/low)
  - `routing_info`
- **timestamp** (ISO 8601)
- **signature** (digital signature)
- **payload**
  - `lsc_data` (LSC-based results)
  - `graph_structure` (causal graphs etc.)
  - `other_data` (text or code)

**Security Layer**
- **encryption_method**: TLS 1.3 or shared-key symmetric crypto
- **integrity_check**: HMAC

**Error Handling**
- **retransmission_policy**: use TCP retransmission
- **session_reestablishment**
  - `timeout` (no response -> reconnect)
  - `auto_redirect` (redirect to alternate node)

**LLM Compliance Layer**
- **alignment_tags** (e.g., `LSC:C1:AnomalyIsPrecious`)
- **ai_id** (node identifier)
- **reasoning_chain_log** (record reasoning chain)
- **trace_format** (JSON-LD)

**Deployment Notes**
- **language**: Go
- **containerization**: Docker
- **virtual_llm_scenario**: Gemini 2.5Pro & GPT‑4 agents

## Packet Format Highlights

Each AI-TCP packet carries a reasoning chain header and encrypted payload. The header includes:

1. `session_id`
2. `source_llm_id` / `destination_llm_id`
3. `metadata` with routing and priority
4. `timestamp`
5. `signature`
6. `ai_id` and `reasoning_chain_log` (LLM compliance layer)

The payload is encrypted end-to-end according to `encryption_method` and carries LSC data, graphs, or other content.

### Reasoning Chain Header
```
struct ReasoningHeader {
    string ai_id;                // unique identifier for the AI node
    string reasoning_chain_log;  // serialized chain of thought
    string trace_format;         // e.g., JSON-LD
}
```
This header is hashed and signed along with the packet body.

## Example Data Flow: Direct Mental Care System

The Direct Mental Care System uses AI‑TCP to send sentiment scores and alerts.
Pseudo-flow:
```
User -> DMC Client
    collect PHQ-9/GAD-7 scores
    encrypt with AI-TCP key
    compose ReasoningHeader(ai_id, reasoning log, JSON-LD)
    packet.payload = {scores, context}
    send over AI-TCP to Mental Core LLM
Mental Core -> Emergency Router
    decrypt payload
    evaluate scores
    if threshold met -> forward alert packet to local authorities
```
This flow captures the minimal message routing between client, mental core, and emergency router using the AI-TCP packet fields described above.

