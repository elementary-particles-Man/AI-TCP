# GG01: LLM Role Definitions

## 1. Purpose

To define the standard roles of Large Language Models (LLMs) participating in AI-TCP compliant systems, and to distinguish their behavioral modes and coordination structures.

---

## 2. Role Types

### 🧠 Reasoner (推論特化)

- Focus: Logical deduction, chain-of-thought generation
- Expected Behavior:
  - Outputs `reasoning_trace`
  - Maintains token-level structure
  - Prioritizes traceability over fluency
- Use Case: Fact generation, hypothesis evaluation

---

### 📝 Narrator (説明・文書化特化)

- Focus: Natural language expression, narrative output
- Expected Behavior:
  - Enhances clarity and emotional resonance
  - Avoids excessive recursion or token overlap
- Use Case: Documentation, user-facing summaries

---

### 🔧 Engineer (構造・出力制御特化)

- Focus: Schema compliance, format consistency, YAML/HTML generation
- Expected Behavior:
  - Injects metadata accurately
  - Converts between formats
  - No hallucination; strict control
- Use Case: PoC packet emission, RFC writing

---

## 3. Interoperability Mode

| Role      | Accepts Input From | Outputs For      |
|-----------|--------------------|------------------|
| Reasoner  | Engineer, Narrator | Engineer, Narrator |
| Narrator  | Reasoner           | Human, Engineer  |
| Engineer  | Reasoner, Narrator | Human, Filesystem |

---

## 4. YAML Tag Recommendation

```yaml
llm_role: reasoner
trace_format: structured
output_mode: yaml
```

```yaml
llm_role: narrator
style: natural
output_mode: markdown
```

```yaml
llm_role: engineer
output_mode: html
compliance: true
```

---

## 5. Multi-Agent Coordination

Each role should be clearly assigned to a distinct model instance.  
Metadata exchange and role switching must be coordinated using AI-TCP Packet Protocol (RFC003).

---

## 6. Related Documents

- RFC002: Compliance Schema
- RFC003: Packet Protocol
- GG03: Fault Handling
