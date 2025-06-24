# Guide to Graph Payload Versioning in AI-TCP

## 1. Rationale for Versioning Mermaid Payloads

The `graph_payload` in AI-TCP, typically rendered using Mermaid, serves as a visual representation of an AI agent's mental model, causal chain, or internal state. As the complexity and semantics of these graphs evolve, a robust versioning system becomes critical to prevent misinterpretation between different agents or system versions.

Versioning ensures that a receiving agent can:
- **Verify Compatibility:** Quickly determine if it can safely parse and understand an incoming graph's structure and semantics.
- **Prevent Silent Failures:** Avoid errors that might arise from attempting to render a graph with deprecated syntax or unknown node types.
- **Enable Graceful Degradation:** Allow an agent to request a different version of a graph or handle it in a legacy-compatible mode.
- **Support Auditing:** Provide a clear, traceable record of which graph structure was used at a specific point in a communication sequence.

---

## 2. Field Specification

To manage graph versions, a dedicated field is introduced. This field should be included in the header of the `.mmd.md` file or within the associated AI-TCP packet's metadata.

- **Field Name:** `graph_payload_version`
- **Format:** [Semantic Versioning 2.0.0](https://semver.org/) (e.g., `MAJOR.MINOR.PATCH`).
  - **MAJOR:** Incremented for incompatible changes to the graph's fundamental structure or meaning.
  - **MINOR:** Incremented for new, backward-compatible additions or features.
  - **PATCH:** Incremented for backward-compatible bug fixes or clarifications.

**Example:**
```yaml
graph_payload_version: "1.0.0"

3. Compatibility Expectations and Policies
Agents must adhere to strict compatibility rules based on the graph_payload_version.

Scenario

Sender Version

Receiver Version

Expected Behavior

Signal Frame Action (Recommended)

Major Mismatch

2.0.0

1.5.0

Hard Fail. The receiver must not attempt to process the graph. It is considered fundamentally incompatible.

Send fail with reason_code: "GRAPH_INCOMPATIBLE_VERSION".

Minor Mismatch (Sender Newer)

1.2.0

1.1.0

Backward-Compatible. The receiver should process the graph, ignoring any unrecognized nodes or syntax introduced in v1.2.0.

Send warn with reason_code: "GRAPH_PARTIAL_SUPPORT".

Minor Mismatch (Receiver Newer)

1.1.0

1.2.0

Forward-Compatible. The receiver fully understands the graph. No issues expected.

Proceed normally. ack if requested.

Patch Mismatch

1.1.3

1.1.2

Fully Compatible. No functional difference is expected.

Proceed normally. ack if requested.

4. Upgrade/Downgrade Flow and Risks
Negotiation Flow: If a receiving agent encounters a major version mismatch, it should use the signal_frame (RFC 016) to issue a fail signal. The sending agent, upon receiving this, may attempt to downgrade the graph to a version compatible with the receiver and re-transmit.

Rendering Risks:

Forward-Compatibility Risk: An older agent processing a newer minor version of a graph might render it without error but miss crucial new context represented by unknown elements. This can lead to subtle logical failures.

Lack of Enforcement Risk: If version checks are not strictly enforced, agents may attempt to render incompatible graphs, leading to unpredictable behavior, rendering failures, or silent misinterpretation of the AI's intended state.

5. Markdown Example of a Versioned .mmd.md File
To ensure version information is tightly coupled with the graph itself, it should be included as YAML frontmatter within the .mmd.md file.

---
graph_payload_version: "1.1.0"
author: "agent-planner-04"
last_updated: "2025-06-25T08:00:00Z"
description: "Causal chain for DMC session phase 2 reframing."
---
```mermaid
flowchart TD
    A[Start: User expresses self-doubt] --> B{Reframe Perfectionism};
    B -- "as 'sincerity'" --> C[Focus on Action];
    C --> D[End: User's self-evaluation shifts];

By adopting this versioning guide, the AI-TCP ecosystem can maintain a high degree of interoperability and reliability as the complexity of its visual communication layer evolves.