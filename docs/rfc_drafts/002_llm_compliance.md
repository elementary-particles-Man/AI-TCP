RFC 002: LLM Compliance Requirements (Revision 2)
Status: Draft
Version: 2.0
Last Updated: 2025-06-25

1. Abstract
This document defines the mandatory compliance requirements for any Large Language Model (LLM) or AI agent to participate in the AI-TCP network. Compliance ensures that an agent can correctly parse, interpret, and generate structured intent, maintaining the integrity and interoperability of the entire ecosystem.

2. Core Compliance Capabilities
An AI-TCP compliant agent MUST possess the following capabilities:

2.1. Format Interpretation
The agent must be able to losslessly parse and serialize the core AI-TCP packet structure as defined in master_schema_v1.yaml. This includes the ability to handle nested YAML structures, lists, and key-value pairs correctly.

2.2. Semantic Restoration from Visual and Structured Data
A key requirement is the ability to derive meaning from abstract representations.

Mermaid to Narrative: The agent must be able to interpret the logical flow, node relationships, and overall intent from a graph_payload containing a Mermaid diagram. It should be able to generate a coherent natural language summary describing the graph's purpose.

YAML to Narrative: The agent must be able to read a structured YAML packet and explain its purpose, drawing connections between the reasoning_trace and the overall intent.

2.3. Reverse-Interpretation and Structural Reconstruction
The agent must demonstrate the ability to perform reverse-inference.

Narrative/Graph to YAML: Given a Mermaid graph and its corresponding intent narrative, the agent must be able to reconstruct a plausible source YAML structure that logically represents the original intent. The accuracy of this reconstruction is a key metric for evaluating semantic understanding.
