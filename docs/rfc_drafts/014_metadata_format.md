# RFC 014: Metadata Format Specification

## 1. Introduction

This RFC defines the standard metadata header used in all AI-TCP packets. The header ensures every packet carries minimal routing, auditing, and processing information in a consistent manner. These fields support packet routing, validation, and lifecycle management between cooperating Large Language Models (LLMs).

## 2. Required Fields

| Field             | Type            | Description                                              |
| ----------------- | --------------- | -------------------------------------------------------- |
| `packet_id`       | string          | Unique identifier of this packet                         |
| `version`         | string          | Protocol or packet version identifier                    |
| `sender_id`       | string          | Originating agent or node identifier                     |
| `recipient_id`    | string          | Intended recipient agent or node                         |
| `timestamp_utc`   | ISO 8601 string | Coordinated Universal Time of packet creation            |
| `intent_category` | enum            | One of: `trace`, `intent`, `conflict`, `confirm`, `meta` |
| `priority_level`  | integer         | Range 0–3 (0=lowest, 3=highest)                          |

## 3. Optional Fields

| Field            | Type    | Description                                        |
| ---------------- | ------- | -------------------------------------------------- |
| `response_to`    | string  | References `packet_id` this packet replies to      |
| `expires_in_sec` | integer | Validity duration in seconds                       |
| `tags`           | list    | Arbitrary labels for routing or filtering          |
| `location_hint`  | string  | Suggested geographic or network region             |
| `signature_hash` | string  | Cryptographic verification hash of header contents |

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

## 6. Extensibility and Constraints

* Additional metadata fields MAY be added using `snake_case` naming.
* Unknown fields MUST be ignored by compliant agents unless explicitly required by future RFCs.
* `priority_level` values outside 0–3 SHOULD trigger rejection.
* Time fields MUST use UTC to avoid ambiguity.
* Versioning of the metadata format allows parsers to adapt to changes over time.

## 7. Status

Draft – Last updated: 2025-06-24
