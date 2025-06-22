# RFC 007: Dynamic Context Flow in AI-TCP

## Overview

Dynamic Context Flow (DCF) defines a mechanism for real-time adjustment of shared memory and processing focus among collaborating AI agents in the AI-TCP protocol. This enables agents to shift priorities and maintain coherent interactions even when context changes rapidly.

## Objectives

- Enable flexible memory recall and forgetting mechanisms
- Dynamically route payloads to relevant AI nodes based on evolving task context
- Ensure synchronization of context states across distributed agents

## Key Components

### 1. Context Anchor Tokens (CAT)

Each packet includes optional Context Anchor Tokens that label its contextual relevance. These may reference:
- User session identifiers
- Current task thread or phase
- Previously shared payload identifiers

### 2. Shared Context Store (SCS)

An optional shared memory structure (local or remote) where relevant context snapshots are stored. AI agents may:
- Retrieve prior snapshots using CATs
- Commit new context blocks
- Invalidate outdated branches

### 3. Flow Priority Table (FPT)

A transient routing structure maintained by each AI agent or AI-TCP core. It maps:
- Incoming packet types → context domains → agent roles
- Urgency modifiers to interrupt long context chains

## Operational Rules

- Agents receiving packets with CATs MUST check local and SCS for matching context.
- If match is found, agent appends to the same context thread.
- If no match and FPT exists, reroute or instantiate a new thread.
- CATs and FPTs are ephemeral but MUST be included in trace logs.

## Use Cases

- Multi-AI collaboration on evolving user queries
- Dynamic goal re-prioritization under external inputs
- Human-in-the-loop editing with evolving context

## Compliance

DCF is optional but RECOMMENDED for all agents participating in long-running or stateful AI-TCP interactions.

## Appendix

Example CAT block (YAML):
```yaml
context_anchors:
  session_id: user-XYZ
  task: rfc_editing
  parent_packet: 00312a
```
