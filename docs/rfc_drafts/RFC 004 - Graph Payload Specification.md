\# RFC 004: Graph Payload Specification

\*Status: Formal Specification\*  
\*Version: 1.0\*  
\*Last Updated: 2025-06-25\*  
\*Author: Gemini, based on a GPT-initiated framework\*

\---

\#\#\# 1\. Overview

This document provides the definitive formal specification for the \*\*Graph Payload\*\*, a core component of the Autonomous Intelligence Transmission Control Protocol (AI-TCP). The Graph Payload utilizes Mermaid syntax to represent an AI agent's internal state, logical flow, causal relationships, or decision-making processes in a format that is both human-readable and machine-interpretable.

It serves as the primary mechanism for transmitting complex, non-linear "intent" between agents, moving beyond simple data exchange to enable a shared, visual understanding of abstract concepts.

\#\#\# 2\. Syntax Specification

\#\#\#\# 2.1. The \`mmd:\` Prefix  
All Graph Payload content within an AI-TCP packet \*\*MUST\*\* be prefixed with \`mmd:\`. This prefix acts as a namespace identifier, signaling to any parsing agent that the subsequent string block is to be interpreted as Mermaid syntax.

\*\*Example in YAML:\*\*  
\`\`\`yaml  
graph\_payload:  
  graph\_structure: |  
    mmd:flowchart TD  
        A \--\> B

#### **2.2. Core Mermaid Syntax**

* **Diagram Type:** While Mermaid supports multiple diagram types, flowchart TD (Top-Down) is the recommended standard for ensuring maximum compatibility and logical clarity.  
* **Line Breaks:** To ensure consistent rendering across all platforms (especially GitHub and Obsidian), line breaks within node labels **MUST** be represented by the HTML tag \<br\>.  
* **Character Encoding:** Content must be UTF-8 encoded.

### **3\. Component Roles (Nodes and Edges)**

To standardize interpretation, specific classes and styles are defined for nodes and edges.

#### **3.1. Node Classes (classDef)**

A standard set of CSS classes should be used to define the role of a node within the graph. This allows for consistent visual representation and helps parsing AIs to understand a node's function at a glance.

| Class Name | Suggested Style | Role Description | YAML type Mapping |
| :---- | :---- | :---- | :---- |
| source | fill:\#eee,stroke:\#333 | The origin of a process or data flow (e.g., user input). | Source, Input |
| process | fill:\#bbf,stroke:\#333 | An active processing, analysis, or transformation step. | Process, Action |
| decision | fill:\#ccf,stroke:\#333 | A branching point where a decision is made. | Decision, Condition |
| state | fill:\#f9f,stroke:\#333 | A stable state, result, or conclusion. | State, Output, Conclusion |

#### **3.2. Edge Types**

The style of an edge indicates the nature of the relationship between two nodes.

| Edge Style | Mermaid Syntax | Relationship Description |
| :---- | :---- | :---- |
| **Solid Line** | \--\> | Represents a direct, causal, or sequential relationship. |
| **Dotted Line** | \-.-\> | Represents a conditional, informational, or indirect link. |

### **4\. Payload Conversion Models**

The Graph Payload is a central part of a multi-format conversion pipeline that ensures intent can be understood across different modalities.

flowchart TD  
    A\[Canonical Intent\<br\>\<b\>(YAML)\</b\>\] \--\>|Codex: \`yaml\_to\_mermaid.go\`| B(Graph Payload\<br\>\<b\>(Mermaid)\</b\>);  
    B \--\>|Browser/Obsidian| C{Visual Representation\<br\>\<b\>(SVG/HTML)\</b\>};  
    B \--\>|Gemini/GPT| D\[Semantic Interpretation\<br\>\<b\>(Narrative)\</b\>\];

1. **YAML to Mermaid:** The canonical definition of an intent is a structured YAML file. This is converted into a Graph Payload by tools like yaml\_to\_mermaid.go.  
2. **Mermaid to Visual:** The Mermaid code is rendered into a visual diagram (SVG) by compliant viewers like Obsidian or browser-based libraries.  
3. **Mermaid to Narrative:** An AI agent receives the Mermaid code and interprets its structure and labels to generate a human-readable narrative, explaining the intent.

### **5\. Semantic Layer Binding**

The components of a Graph Payload are not arbitrary; they are directly bound to the source YAML structure.

* A Mermaid **node id** (e.g., InitialState) MUST correspond to a component's id in the source YAML's components array.  
* A Mermaid **node label** SHOULD correspond to the component's name and/or details.

This binding ensures that the graph is a faithful representation of the underlying structured data.

### **6\. Validation & Interoperability**

* **Syntactic Validation:** A receiving agent MUST validate that the payload content is valid Mermaid syntax.  
* **Versioning:** Agents MUST respect the graph\_payload\_version field. A major version mismatch is a hard failure and must be handled via a fail signal (see RFC 016).

### **7\. Graph Payload Lifecycle**

1. **Generation:** An agent creates a YAML intent and converts it to a versioned Graph Payload.  
2. **Transmission:** The payload is embedded in an AI-TCP packet and sent.  
3. **Interpretation:** The receiving agent parses the Mermaid syntax, validates its version, and interprets its semantic meaning.  
4. **Action/Response:** The agent acts upon the interpreted intent and may respond with its own packet.  
5. **Archiving:** The transmitted graph, along with its Observation Capsule (RFC 017), is archived for audit purposes.

### **8\. Versioning & Future Extensions**

This document specifies v1.0 of the Graph Payload. Future versions may include support for more complex diagram types (sequenceDiagram, stateDiagram-v2) or interactive elements. All changes will be managed according to RFC versioning policies.

### **9\. Example Payload**

**Source YAML (intent\_001.yaml):**

id: intent\_001  
name: "DMC Session for Anxiety and Self-Doubt"  
components:  
  \- id: "Phase1"  
    name: "Empathy & Specification"  
    type: "State"  
...  
connections:  
  \- from: "Phase1"  
    to: "Phase2"  
    label: "Enables Articulation"  
...

**Generated Graph Payload:**

graph\_payload:  
  graph\_payload\_version: "1.0.0"  
  graph\_structure: |  
    mmd:flowchart TD  
        classDef state fill:\#f9f;  
        Phase1\["Phase1\<br\>Empathy & Specification"\]:::state  
        Phase2\["Phase2\<br\>Cognitive Reframing"\]  
        Phase1 \--\>|Enables Articulation| Phase2;  
