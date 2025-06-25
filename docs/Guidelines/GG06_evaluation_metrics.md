GG06: Evaluation Metrics for AI-TCP PoCs
1. Purpose
This document defines the success criteria and evaluation metrics for AI-TCP Proof-of-Concept (PoC) tasks. It serves as a quantitative and qualitative benchmark for assessing the protocol's effectiveness.

2. Overall PoC Success Definition
A PoC is considered successful if it demonstrates a complete, verifiable, and lossless round-trip of structured intent. This means an intent, originating as a YAML structure, can be transformed into other representations (Mermaid, Narrative) and then be reverse-interpreted back into a YAML structure that is semantically equivalent to the original.

3. Key Evaluation Metrics
Metric

Target

Method

Success Threshold

Structural Match Rate

YAML ↔ YAML

Compares the key/value structure of the original YAML with the reverse-interpreted YAML.

> 95% structural correspondence (ignoring non-essential metadata).

Semantic Similarity

name, type, details fields

Use a cosine similarity score from a sentence-embedding model to compare the text content.

> 0.85 similarity score.

Graph Consistency

YAML ↔ Mermaid

Verify that all components and connections in the YAML are accurately represented in the generated Mermaid graph.

100% mapping of nodes and edges.

Narrative Alignment

Narrative ↔ Graph/YAML

A human reviewer or a separate AI agent confirms that the narrative accurately reflects the logic and intent of the structured data.

PASS/FAIL based on review.
