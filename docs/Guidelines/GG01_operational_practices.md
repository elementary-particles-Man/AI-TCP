# GG01: Operational Best Practices for AI-TCP

## 1. Purpose

This guideline provides best practices for deploying, configuring, and managing systems that implement the AI-TCP protocol. It is designed to supplement the RFC series by offering operational insights that ensure reliability, interpretability, and security.

## 2. Scope

These recommendations apply to any system participating in AI-TCP exchanges, including:

- Autonomous reasoning agents (LLMs, agents, toolchains)
- Relay routers or protocol intermediaries
- Monitoring or logging components

## 3. Recommended Practices

### 3.1 Packet Validation Before Dispatch

All outgoing packets should be validated against RFC003 schema. Implement runtime checks to prevent malformed reasoning_trace or graph_payload.

### 3.2 Trace Logging

Maintain full `reasoning_trace` logs with timestamps and step integrity. Trace data should be non-editable post-commit and optionally mirrored to a separate audit sink.

### 3.3 Flow Separation by Namespace

Use `meta.origin` and `llm_profile.id` to segment traffic flows. This helps maintain contextual isolation and simplifies trace debugging.

### 3.4 AI-TCP Versioning and Compatibility

Every `llm_profile.version` should be semver-compliant. Communicating systems must reject packets from incompatible protocol versions unless explicitly overridden.

### 3.5 Rate Limiting & Fallbacks

Introduce per-source rate limits to avoid overloading LLM endpoints. When unavailable, fallback policies (e.g., auto_redirect → defer) should be applied.

### 3.6 Redundancy & Replay Detection

Design components to tolerate duplicated packets and differentiate via `meta.timestamp`. Do not assume strict once-only delivery.

## 4. Deployment Recommendations

| Layer | Practice |
|-------|----------|
| Protocol Layer | RFC003 validation, rejection of malformed graph_payload |
| Runtime        | Soft TTL on context traces, fallback routing enabled |
| Monitoring     | Long-term storage of all `reasoning_trace` with hash integrity |
| Interop        | Test against both strict and lax schema variants |

## 5. Anti-Patterns to Avoid

- Skipping `step` numbers in trace logs
- Sending packets with empty `llm_profile`
- Graphs without `mmd:` prefix
- Editing `reasoning_trace` after commit

## 6. Reference

- RFC 001–004
- YAML 1.2
- Semantic Versioning 2.0.0
