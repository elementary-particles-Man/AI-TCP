---
title: RFC Draft: AI-TCP Integration for Direct Mental Care PoC
version: 0.1
status: draft
language: en
---

# AI-TCP Implementation and Direct Mental Care System PoC

This document consolidates the core technical aspects required to build a proof of concept (PoC) for **AI-TCP** and the **Direct Mental Care System**. It is intended for international developers contributing to early prototypes.

## 1. AI-TCP Protocol Structure

AI-TCP operates on top of IPv6/TCP and introduces a semantic header to track reasoning and identity between large language model (LLM) nodes.

### 1.1 Packet Layout

```
+------------------+--------------------------------------------+
| TCP Header       | Standard TCP fields                        |
+------------------+--------------------------------------------+
| AI-TCP Header    | SessionID (128b)                           |
|                  | Source AI-ID (64b)                         |
|                  | Destination AI-ID (64b)                    |
|                  | Metadata { message_type, priority, ... }   |
|                  | Timestamp (ISO‑8601)                       |
|                  | Signature (digital)                        |
+------------------+--------------------------------------------+
| Payload          | LSC-compliant data / trace information     |
+------------------+--------------------------------------------+
```

### 1.2 Information Header Fields

- **ai_id** – unique identifier for each LLM node (public‑key hash or UUID).
- **reasoning_chain** – ordered record of steps leading to the current payload.
- **emotional_log** – optional PHQ‑9/GAD‑7 scores or sentiment values.

All fields are signed and timestamped to provide auditability.

## 2. Sentiment Analysis Trigger Routine

The Direct Mental Care System monitors user text via PHQ‑9 and GAD‑7 scoring. When values exceed preset thresholds (PHQ ≥ 15 or GAD ≥ 12) the system triggers an emergency routing sequence:

1. Scores are inferred by the mental_core engines (Copilot, GPT, Gemini).
2. The emotional_log is appended to the AI-TCP header.
3. Alerts are sent to the emergency_router module which can notify local AI monitors and optionally escalate to emergency services (119 in Japan).

## 3. LLM Integration Flow (YUBI × Copilot × Gemini)

1. **User Interface** – YUBI chat UI communicates with the mental_core via AI-TCP.
2. **Copilot SDK** – handles local device interactions and initial sentiment preprocessing.
3. **Gemini/GPT** – perform deep reasoning and maintain reasoning_chain logs.
4. Results and emotional_log entries are packaged in AI-TCP packets and routed to monitoring nodes or stored for analysis.

The flow ensures that multiple model vendors cooperate while preserving traceability.

## 4. Implementation Steps (PoC)

1. **Session Library** – Implement `AITCPSession` in Go, including header serialization, signing, and verification.
2. **Sentiment Module** – Build PHQ‑9/GAD‑7 scoring and threshold triggers. Output results to emotional_log.
3. **Integration Testbed** – Use Docker containers to simulate Copilot, GPT, and Gemini nodes exchanging messages via AI-TCP.
4. **Emergency Router** – Prototype a rule-based router that listens for elevated scores and dispatches alerts.
5. **Documentation & Logging** – Log reasoning_chain data in JSON‑LD format for future audit.

## 5. Future Work

- Complete YAML formalization of the packet spec.
- Publish updated drafts to the wider working group.
- Explore secure deployment options (TLS 1.3 or ChaCha20-Poly1305).

## 6. License

This document is released under CC0 1.0.
