RFC 005: Advanced PoC Use Cases
Status: Draft
Version: 1.0
1. Abstract
This document defines the specifications for advanced Proof-of-Concept (PoC) use cases designed to test the negotiation and coordination capabilities of the AI-TCP protocol. These scenarios move beyond simple data exchange to simulate complex, real-world multi-agent interactions.
2. Use Case #2: Negotiation
Objective: To demonstrate how two AIs with different internal axioms can use AI-TCP to negotiate a mutually acceptable outcome.
Scenario: A creative writing AI (e.g., Gemini) proposes a marketing slogan. A legal review AI (e.g., Legal-AI) flags it for potential trademark infringement.
Flow:
Proposal (Gemini): Sends an intent_packet. The graph_payload visualizes the slogan's components and their intended emotional impact.
Counter-Proposal (Legal-AI): Interprets the graph and identifies a conflict. It responds with a signal_frame of type warn and a revised graph_payload where the problematic node is highlighted and an alternative is proposed via a dotted-line edge.
Resolution (Gemini): Receives the counter-proposal, integrates the legal feedback, and sends a final, updated intent_packet that satisfies both creative and legal constraints.
3. Use Case #3: Third-Party Mediation
Objective: To demonstrate how a neutral third-party AI can resolve a conflict between two other agents.
Scenario: GPT and Gemini produce conflicting analyses of a dataset. Codex acts as a trusted mediator.
Flow:
Conflict: Both GPT and Gemini send packets with contradictory conclusions targeting the same analysis report.
Intervention (Codex): The Moderator-AI (Codex) observes the conflict and sends interrupt signals to both agents, halting their processes.
Analysis (Codex): Codex generates a new graph_payload. This "conflict map" visualizes the two divergent reasoning paths from the reasoning_trace of each agent's packet, clearly showing where their logic diverged.
Adjudication (Codex): Based on a predefined "safety-first" rule, Codex makes a final decision. It broadcasts a resolution packet containing the conflict map and the final, authoritative conclusion, along with fail signals to the non-selected agent's original packet. The reasoning_trace explicitly references the rule used for adjudication.
