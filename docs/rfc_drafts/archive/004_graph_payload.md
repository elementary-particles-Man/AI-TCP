RFC 004: Graph Payload Specification
Status: Draft
Version: 1.0
1. Abstract
This document provides the formal specification for the graph_payload component within an AI-TCP packet. It defines how Mermaid-based graphs are used as a primary mechanism for conveying structured intent, logical flows, and causal relationships between AI agents.
2. Rationale: Why Graphs for Meaning Sharing?
While reasoning_trace provides a linear, step-by-step account of an AI's logic, the graph_payload offers a holistic, non-linear map of its "thought process." This visual representation is superior for conveying:
Causality and Dependency: Edges clearly define how one concept or state leads to another.
Complex Relationships: Subgraphs and clusters can represent complex, nested ideas that are difficult to describe sequentially.
Rapid Comprehension: Both humans and other AIs can parse the overall structure of a graph much faster than a long textual trace, making it ideal for high-level intent synchronization.
3. Specification
The graph_payload is an object containing at least one key, graph_structure.
Location: payload.graph_structure
Format: A string containing valid Mermaid syntax.
Prefix Requirement: The string MUST begin with the mmd: prefix to be identified as a Mermaid payload by parsers.
4. Mermaid Syntax and Constraints
To ensure maximum interoperability and readability, the following conventions MUST be followed:
Directionality: Always declare a flowchart direction (e.g., flowchart TD) for clarity.
Node IDs: Use descriptive, human-readable IDs for nodes (e.g., InitialState instead of A).
Labels: Edge labels should be concise and describe the action or relationship of the transition.
Styling: classDef should be used to define roles for nodes (e.g., source, process, decision), enhancing visual clarity.
Compatibility: Use <br> for line breaks within labels to ensure proper rendering across all platforms, including Obsidian and GitHub.
5. Example graph_payload
payload:
  graph_structure: |
    mmd:flowchart TD
        classDef source fill:#eee;
        A[Initial Request]:::source --> B{Analysis};
        B --> C[Conclusion];
