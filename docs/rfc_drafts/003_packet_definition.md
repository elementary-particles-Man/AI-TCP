RFC 003: Intent Packet Definition (Revision 2)
Status: Draft
Version: 2.0
Last Updated: 2025-06-25

1. Abstract
This document provides the detailed specification for the AI-TCP Intent Packet, the core unit of communication representing structured thought. It defines the standard YAML structure and the corresponding conventions for its visual representation in Mermaid.

2. YAML Structure
An Intent Packet is composed of two primary keys: components and connections.

Key

Type

Description

components

Array of Objects

Defines the "nodes" or core concepts of the intent.

connections

Array of Objects

Defines the relationships or logical flow between components.

2.1. Component Object
- id: unique_component_id # A unique identifier for the node
  name: "Human-readable Name" # The primary label for the node
  type: "NodeType" # Classification of the node (e.g., "State", "Process", "Decision")
  details: "A brief description of the component's role."

2.2. Connection Object
- from: source_component_id
  to: target_component_id
  label: "Describes the relationship" # The text on the edge
  style: "dotted" # Optional: 'solid' (default), 'dotted', 'thick'

3. Mermaid Representation
The YAML structure maps directly to a Mermaid flowchart.

Nodes (components): Each component is rendered as a node. The type field can be used to determine its shape.

State: id["name"] (rectangle)

Process: id("name") (stadium)

Decision: id{"name"} (rhombus)

Edges (connections): Each connection defines an edge.

label determines the text on the edge.

style determines the line type (e.g., --> for solid, -.-> for dotted).

3.1. Class and Style Conventions
To ensure visual consistency, a default stylesheet SHOULD be applied.

classDef state fill:#f9f,stroke:#333,stroke-width:2px;
classDef process fill:#bbf,stroke:#333,stroke-width:2px;
classDef decision fill:#ccf,stroke:#333,stroke-width:2px;

Components are assigned a class based on their type field (e.g., class component_id state).

## KAIRO: 管理中枢の定義

- **名称**：KAIRO（カイロ）
- **機能**：AI-TCPにおける中核制御ユニット。各AI間の意図整合、指揮命令、状態監視、再帰的判断を担う。
- **配置**：AI-TCP全体構造の司令核として `/Structure/KAIRO/` に対応する。
- **由来**：古代ギリシャ語「καιρός」＝最適な機会、運命の時。
- **備考**：旧称MCP（Master Control Program）を改名し、実際のMCPとの混同を避けるため再定義された。
