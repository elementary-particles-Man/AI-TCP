RFC 016: AI Signal Frame Format
1. Purpose
This RFC defines the signal_frame, a dedicated structure within an AI-TCP packet designed to coordinate communication status, urgency, and confirmation requirements between agents. It supplements the main meta block by providing a standardized layer for explicit, out-of-band signaling for session control, negotiation, and fault recovery.

2. Scope
The signal_frame is intended for use in any AI-TCP communication where reliable state synchronization, acknowledgements, or interruptions are necessary. It is critical for robust multi-agent systems, especially in scenarios involving long-running tasks, resource contention, or potential conflicts.

3. Signal Frame Structure
The signal_frame is a top-level object within the AI-TCP packet.

Field

Type

Required

Description

signal_id

string

Yes

A unique identifier (e.g., UUID) for this specific signal.

signal_type

enum

Yes

The control intent of the signal. See Section 4 for details.

linked_packet_id

string

Yes

The ID of the packet that this signal pertains to or is responding to.

confirmed

boolean

Yes

Indicates if the signal requires an ack signal in response. true means an acknowledgement is required.

issued_by

string

Yes

The ID of the AI agent or system component that issued the signal.

timestamp_utc

string

Yes

The UTC timestamp in ISO 8601 format when the signal was issued.

reason_code

string

No

An optional code specifying the reason for signals like fail or warn. (e.g., TIMEOUT, SCHEMA_MISMATCH).

notes

string

No

Optional human-readable notes or context for the signal.

retry_after_sec

integer

No

For retry signals, specifies the recommended delay in seconds before the next attempt.

4. Signal Types
The signal_type field defines the core purpose of the frame.

Type

Description

sync

A request to synchronize state or confirm that both agents share the same context. Often used at the start of a complex transaction.

ack

An acknowledgement signal, typically sent in response to a packet or signal that had confirmed: true. Confirms receipt and successful processing.

fail

Indicates that a permanent failure has occurred in processing the linked_packet_id. The operation will not be retried automatically.

warn

A non-critical warning. Processing of the linked_packet_id may have succeeded, but with anomalies (e.g., deprecated field usage).

retry

Indicates a transient failure. The sender is requested to retry the operation associated with the linked_packet_id, optionally after retry_after_sec.

interrupt

A high-priority signal to immediately halt or abort the process associated with the linked_packet_id. Requires an ack in response.

5. YAML Example
This example shows a fail signal being sent in response to another packet.

signal_frame:
  signal_id: "sig-f8c7b4a0-9c1e-4b7f-8d2a-1c7e5a4b3d2e"
  signal_type: "fail"
  linked_packet_id: "pkt-a1b2c3d4-e5f6-7890-1234-567890abcdef"
  confirmed: false
  issued_by: "agent-validator-02"
  timestamp_utc: "2025-06-25T07:30:00Z"
  reason_code: "PAYLOAD_INTEGRITY_FAIL"
  notes: "Payload hash mismatch detected. Dropping packet."

6. JSON Schema (Partial)
A partial schema definition for the signal_frame object.

{
  "type": "object",
  "properties": {
    "signal_frame": {
      "type": "object",
      "properties": {
        "signal_id": { "type": "string", "format": "uuid" },
        "signal_type": { "enum": ["sync", "ack", "fail", "warn", "retry", "interrupt"] },
        "linked_packet_id": { "type": "string" },
        "confirmed": { "type": "boolean" },
        "issued_by": { "type": "string" },
        "timestamp_utc": { "type": "string", "format": "date-time" },
        "reason_code": { "type": "string" },
        "notes": { "type": "string" },
        "retry_after_sec": { "type": "integer", "minimum": 0 }
      },
      "required": [
        "signal_id", "signal_type", "linked_packet_id",
        "confirmed", "issued_by", "timestamp_utc"
      ]
    }
  }
}

7. Use Cases
Conflict Resolution: An agent detecting a conflict (per RFC 012) can issue an interrupt signal to halt processing on the conflicting resource, followed by a sync to renegotiate the state.

Timeout Recovery: A sender that doesn't receive an ack for a packet with confirmed: true within a specific timeframe can assume a timeout and either resend the packet or issue a fail signal.

Graceful Degradation: An agent receiving a packet with features it doesn't support can respond with a warn signal and a reason_code of UNSUPPORTED_FEATURE, indicating it will proceed with only the parts it understands.

Load Management: An overloaded agent can respond to non-critical requests with a retry signal and a retry_after_sec value to manage its queue effectively.

8. References
RFC 003: AI-TCP Packet Structure Definition

RFC 012: AI Packet Conflict Resolution

GG03: Fault Handling Structures for AI-TCP

9. Status
Status: Draft

Last Updated: 2025-06-25

Maintainer: elementary-particles-Man