# RFC 015: Language Translation and Semantic Equivalence Standard

## 1. Objective
Define the standard for translation and meaning preservation in multilingual LLM interactions within AI‑TCP.

## 2. Canonical Language Definition
English is the canonical language for reference text within AI‑TCP. Each segment may be mirrored in Japanese for interoperability. Both forms carry identical meaning and must retain equivalent context. If discrepancies arise, the English wording serves as the source of truth.

## 3. Semantic Tiers
1. **Literal** – Word‑for‑word substitution while preserving grammar.
2. **Contextual** – Meaning is preserved with minor rephrasing to fit natural expression in the target language.
3. **Narrative** – Broader paraphrasing or summarization while keeping the intent intact.

## 4. Translation Quality Scoring
Translations are rated on a 0‑5 scale:

| Score | Meaning               | Description                                      |
|------:|----------------------|--------------------------------------------------|
| 5     | Perfect              | No loss of information or nuance.                |
| 4     | Equivalent           | Meaning preserved with minimal stylistic change. |
| 3     | Acceptable           | Minor omissions but intent is intact.            |
| 2     | Degraded             | Noticeable loss of detail or tone.               |
| 1     | Mismatch             | Major errors or misinterpretations.              |
| 0     | Invalid              | Unusable translation.                            |

Scores of 4 or higher are required for official AI‑TCP documentation.

## 5. Permitted vs. Disallowed Equivalence Transformations

### Permitted
- Reordering clauses where meaning is unchanged.
- Converting idioms to culturally appropriate equivalents.
- Omitting filler words that do not alter intent.

### Disallowed
- Introducing new information not in the source text.
- Changing the tone from formal to informal (or vice versa) without instruction.
- Summarizing or omitting critical steps in procedures.

## 6. References
- RFC 001: AI‑TCP Protocol Overview
- RFC 003: AI‑TCP Packet Structure Definition
