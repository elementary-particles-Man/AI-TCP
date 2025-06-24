# RFC 015: Edge Device Intent Format

## 1. Overview
This RFC defines a lightweight `intent_structure` suitable for edge AI agents running on limited hardware (e.g., on-device NPU with no cloud access). The design emphasizes minimal memory usage and clear semantics while remaining extensible for future fields.

## 2. Base Structure
The intent is represented as a YAML or JSON object with snake_case keys. Optional fields may be omitted to conserve space. Unknown fields MUST be ignored by parsers to maintain backward compatibility.

## 3. Partial JSON Schema
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "EdgeIntent",
  "type": "object",
  "properties": {
    "intent_type": {"type": "string"},
    "content": {"oneOf": [{"type": "string"}, {"type": "object"}]},
    "justification": {"type": "string"},
    "target_action": {"type": "string"},
    "urgency": {"type": "integer", "minimum": 0, "maximum": 3},
    "awareness_hint": {"type": "string"}
  },
  "required": ["intent_type", "content"]
}
```

## 4. YAML Example
```yaml
intent_type: query
content:
  command: get_status
  parameters:
    verbose: false
justification: minimal check before action
target_action: display_status
urgency: 1
awareness_hint: offline_mode
```

## 5. Field Reference
| Field | Type | Description |
|-------|------|-------------|
| `intent_type` | string | Classifies the intent (e.g., `query`, `command`, `warn`). |
| `content` | string or map | Main body of the intent. Can be plain text or structured key-value pairs. |
| `justification` | string | Optional rationale or supporting logic. |
| `target_action` | string | Optional intended outcome or follow-up action. |
| `urgency` | int | Optional priority level from 0 (low) to 3 (immediate). |
| `awareness_hint` | string | Optional environment or context flag. |

## 6. Use Case: NPU-Only Agents
Edge devices running isolated NPUs may exchange intents without any cloud connectivity. This format allows concise expression of actions and reasoning with minimal overhead, facilitating reliable on-device coordination.
