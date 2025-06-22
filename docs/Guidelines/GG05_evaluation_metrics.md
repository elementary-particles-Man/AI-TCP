# GG05: AI-TCP Evaluation Metrics

## 1. Purpose

This document defines key metrics for evaluating AI-TCP communications and PoC success thresholds.

---

## 2. PoC Success Criteria

| Criterion           | Description |
|---------------------|-------------|
| Schema Validation   | All YAML packets must conform to master schema |
| HTML Render Success | Correct transformation into human-readable HTML |
| Mermaid Graph Pass  | All `mmd:` blocks render correctly in standard viewers |
| Payload Integrity   | Hash and structure validation without error |
| Round-trip Proof    | AI-to-AI exchange returns meaningful reply |

---

## 3. Performance Metrics

| Metric                  | Definition |
|--------------------------|------------|
| Packet Completion Time   | Time from YAML emission to final rendered HTML |
| LLM Reasoning Depth      | Count of valid nested steps in reasoning_trace |
| Interoperability Score   | Compatibility rate between different AI agents |
| Fault Tolerance Index    | # of successful recoveries from induced faults |
| Security Enforcement Rate| % of packets meeting GG04 security requirements |

---

## 4. Compliance Modes Evaluation

Evaluation across compliance modes:

| Mode    | Baseline     | Full       | Secure      |
|---------|--------------|------------|-------------|
| Speed   | ✅ High       | 🟡 Medium  | 🔴 Low      |
| Robustness | 🟡 Medium  | ✅ High  | ✅ Very High |
| Traceability | 🔴 None  | ✅ Full   | ✅ Full      |

---

## 5. YAML Annotation Example

```yaml
evaluation:
  packet_valid: true
  mermaid_valid: true
  latency_ms: 142
  trace_depth: 6
  secure_pass: true
  interoperability: 0.92
  compliance_mode: "secure"
```

---

## 6. Reporting Format

All metrics must be reported in both YAML (for machine use) and Markdown/HTML (for human evaluation).  
Output must be timestamped and stored in `evaluation/` directory.

---

## 7. Related Documents

- GG03: Fault Handling
- GG04: Security Policy
- RFC003: Packet Format
