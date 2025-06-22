# RFC 011: LLM Role Design in AI-TCP

## Status
Draft

## Abstract
This document defines the separation of duties and interaction patterns for large language models within the AI‑TCP protocol suite. It outlines how models such as GPT, Codex, and Gemini coordinate tasks, delegate responsibilities, and recover from failures in multi‑LLM workflows.

---

## 1. Design Principles
- **Clear Responsibility Boundaries** – Each model type should focus on a well defined capability to maximize reliability and traceability.
- **Deterministic Packet Handling** – Roles align to specific phases of the AI‑TCP packet lifecycle: generation, validation, and narration.
- **Redundancy Through Overlap** – Where feasible, roles can overlap to provide fallbacks if one model becomes unavailable.

## 2. Role Separation and Responsibilities
| Role  | Primary Focus      | Typical Responsibilities                             |
|-------|--------------------|------------------------------------------------------|
| **Codex**  | Static processing | Parsing, validating packet structure, and handling code‑like reasoning traces. |
| **GPT**    | Supervision      | Coordinating task flow, issuing directives, and verifying final outputs. |
| **Gemini** | Narrative        | Producing fluent summaries or external‑facing documentation from validated traces. |

## 3. Task Delegation Logic
1. **Directive Issuance** – GPT receives a human or system directive and creates an initial packet.
2. **Structural Validation** – Codex validates the packet against compliance rules and may enrich it with code or schema references.
3. **Narrative Production** – Gemini transforms validated traces into human‑readable text or narrative summaries.
4. **Feedback Loop** – If inconsistencies are detected at any stage, the packet is rerouted back to GPT for adjustment or clarification.

## 4. Fallback and Redundancy Scenarios
- If Codex fails validation, GPT can invoke an alternate model with similar parsing abilities.
- If GPT supervision becomes unreachable, Gemini may continue narrative tasks but must mark the packet as unsupervised.
- All models should log failure states in the `reasoning_trace` for later review and replay.

## 5. Discussion
This separation of roles allows different LLM families to specialize without overlapping responsibilities. By defining clear interaction points, AI‑TCP can orchestrate complex workflows while keeping model behaviors transparent. Future expansions may introduce additional roles (e.g., planning engines or domain experts) that follow the same delegation logic.

## 6. References
- RFC 001: AI‑TCP Protocol Overview
- RFC 003: Packet Structure Definition
- RFC 005: Multi‑AI Directive Protocol

---

*End of RFC 011*
