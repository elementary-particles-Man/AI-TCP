# RFC 014: Metadata Format Specification

## 1. Overview
This RFC defines the standard metadata header used in all AI-TCP packets. The header ensures every packet carries minimal routing, auditing, and processing information in a consistent manner.

## 2. Required Fields
| Field | Type | Description |
|-------|------|-------------|
| `packet_id` | string | Unique identifier for the packet |
| `version` | string | Metadata format version identifier |
| `sender_id` | string | Originating agent or system |
| `recipient_id` | string | Intended recipient agent or system |
| `timestamp_utc` | ISO 8601 | Coordinated Universal Time of packet creation |
| `intent_category` | enum | One of: `trace`, `intent`, `conflict`, `confirm`, `meta` |
| `priority_level` | integer | Priority from `0` (lowest) to `3` (highest) |

## 3. Optional Fields
| Field | Type | Description |
|-------|------|-------------|
| `response_to` | string | Packet ID that this message replies to |
| `expires_in_sec` | integer | Time-to-live in seconds |
| `tags` | list | Arbitrary labels for routing or filtering |
| `location_hint` | string | Suggested geographic or network location |
| `signature_hash` | string | Cryptographic hash or signature for verification |

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
  packet_id: "pkt-001"
  version: "1.0"
  sender_id: "agent_A"
  recipient_id: "agent_B"
  timestamp_utc: "2025-07-01T12:00:00Z"
  intent_category: intent
  priority_level: 2
  response_to: "pkt-000"
  expires_in_sec: 3600
  tags: [demo, rfc014]
  location_hint: "eu-west"
  signature_hash: "abc123def"
```

## 6. Notes
- All required fields MUST appear in every metadata header.
- Optional fields MAY be omitted if not applicable.
- New fields can be added in future revisions, but implementations MUST ignore unknown keys for forward compatibility.
- Versioning of the metadata format allows parsers to adapt to changes over time.

*End of RFC 014*
