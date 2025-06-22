### 📦 **[RFC草稿] `003_packet_definition.md` 構造草案**

```markdown
# RFC 003: AI-TCP Packet Structure Definition

## 1. Purpose
To formalize the structure and minimal required fields for any AI-TCP-compliant packet.

## 2. Root Structure

| Key | Type | Description |
|-----|------|-------------|
| `graph_payload` | object | Embedded conceptual map (Mermaid) |
| `reasoning_trace` | array | Historical reasoning log |
| `meta` | object | Metadata (timestamp, origin, type) |
| `llm_profile` | object | Describes source/target LLM |
| `auto_redirect` | object | Optional continuation instruction |

## 3. Constraints
- All keys must be top-level YAML entries
- Fields must not conflict or overwrite one another
- `graph_payload.graph_structure` must start with `mmd:`

## 4. Minimal Packet Example

```yaml
graph_payload:
  graph_structure: |
    mmd:flowchart TD
    A --> B

reasoning_trace:
  - step: 1
    input: Request received
    output: Evaluating...

meta:
  timestamp: 2025-06-22T01:00:00Z
  origin: system-core

llm_profile:
  id: GPT
  version: 4.0

auto_redirect:
  type: feedback
  next_action: halt
