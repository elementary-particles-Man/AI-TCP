# RFC 014: Metadata Format Specification

## 1. Introduction
This RFC defines the minimal metadata header required for every AI‑TCP packet.
The header fields support packet routing, validation, and lifecycle management
between cooperating Large Language Models (LLMs).

## 2. Required Fields

| Field | Type | Notes |
|-------|------|------|
| `packet_id` | string | Unique identifier of this packet |
| `version` | string | AI‑TCP protocol or packet version |
| `sender_id` | string | Originating node or agent identifier |
| `recipient_id` | string | Intended recipient node or agent |
| `timestamp_utc` | ISO&nbsp;8601 string | Creation time in UTC |
| `intent_category` | enum | `trace`, `intent`, `conflict`, `confirm`, or `meta` |
| `priority_level` | integer | Range 0–3 (0=lowest, 3=highest) |

## 3. Optional Fields

| Field | Type | Notes |
|-------|------|------|
| `response_to` | string | References `packet_id` this packet answers |
| `expires_in_sec` | integer | Validity duration in seconds |
| `tags` | array | Free‑form labels for routing or filtering |
| `location_hint` | string | Suggested geographic or network region |
| `signature_hash` | string | Verification hash of header contents |

## 4. Partial JSON Schema
```json
{
  "type": "object",
  "required": [
    "packet_id",
    "version",
    "sender_id",
    "recipient_id",
    "timestamp_utc",
    "intent_category",
    "priority_level"
  ],
  "properties": {
    "packet_id": {"type": "string"},
    "version": {"type": "string"},
    "sender_id": {"type": "string"},
    "recipient_id": {"type": "string"},
    "timestamp_utc": {"type": "string", "format": "date-time"},
    "intent_category": {
      "type": "string",
      "enum": ["trace", "intent", "conflict", "confirm", "meta"]
    },
    "priority_level": {"type": "integer", "minimum": 0, "maximum": 3},
    "response_to": {"type": "string"},
    "expires_in_sec": {"type": "integer"},
    "tags": {"type": "array", "items": {"type": "string"}},
    "location_hint": {"type": "string"},
    "signature_hash": {"type": "string"}
  }
}
```

## 5. YAML Usage Example
```yaml
meta:
  packet_id: "123e4567-e89b-12d3-a456-426614174000"
  version: "1.0"
  sender_id: "node_a"
  recipient_id: "node_b"
  timestamp_utc: "2025-06-22T00:00:00Z"
  intent_category: intent
  priority_level: 1
  response_to: "122e4567-e89b-12d3-a456-426614174999"
  expires_in_sec: 3600
  tags: [demo, sample]
  location_hint: "datacenter-1"
  signature_hash: "aabbccddeeff"
```

## 6. Extensibility and Constraints
- Additional metadata fields MAY be added using `snake_case` naming.
- Unknown fields MUST be ignored by compliant agents unless explicitly required
  by future RFCs.
- `priority_level` values outside 0–3 SHOULD trigger rejection.
- Time fields MUST use UTC to avoid ambiguity.

## 7. Status
Draft – Last updated: 2025-06-22
