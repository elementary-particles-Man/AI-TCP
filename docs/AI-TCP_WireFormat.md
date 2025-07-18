# AI-TCP Wire Format Specification

This document details the on-the-wire format of AI-TCP packets, as defined by FlatBuffers schemas. The primary schema for the AI-TCP packet structure is located at `KAIRO/schema/ai_tcp_packet.fbs`.

## 1. Core Packet Structure (`AITcpPacket`)

The fundamental unit of communication in AI-TCP is the `AITcpPacket`, which is designed for end-to-end encryption and authentication. Its structure is defined as follows:

```flatbuffers
// KAIRO/schema/ai_tcp_packet.fbs
namespace AITCP;

table AITcpPacket {
  version:ubyte;                  // Protocol version
  ephemeral_key:[ubyte] (required);  // Ephemeral public key for this packet
  nonce:[ubyte] (required);          // Nonce for ChaCha20-Poly1305
  encrypted_sequence_id:[ubyte] (required);  // Encrypted sequence ID
  encrypted_payload:[ubyte] (required);      // Encrypted payload
  signature:[ubyte] (required);              // Ed25519 signature over the whole packet
  header:[ubyte];                // Optional unencrypted header for metadata exchange
  payload:[ubyte];               // Optional plain payload for small control messages
  footer:[ubyte];                // Optional footer bytes for trailing data
}

root_type AITcpPacket;
```

### Field Descriptions:

*   **`version`**: A single byte indicating the protocol version.
*   **`ephemeral_key`**: The ephemeral public key used for key exchange and derivation of symmetric encryption keys for this specific packet. This is a `required` field.
*   **`nonce`**: A cryptographic nonce, essential for the ChaCha20-Poly1305 authenticated encryption algorithm. This is a `required` field.
*   **`encrypted_sequence_id`**: An encrypted identifier for the packet's sequence within a session. This is a `required` field.
*   **`encrypted_payload`**: The core of the packet, containing the encrypted logical header and data payload. The contents of this field are opaque until decrypted. This is a `required` field.
*   **`signature`**: An Ed25519 digital signature covering the entire packet, ensuring authenticity and integrity. This is a `required` field.
*   **`header` (Optional)**: An unencrypted byte vector intended for metadata exchange that does not require encryption, such as routing hints or public session identifiers.
*   **`payload` (Optional)**: A plain (unencrypted) byte vector for small control messages or other data that does not require confidentiality. This is distinct from the `encrypted_payload`.
*   **`footer` (Optional)**: Additional unencrypted bytes at the end of the packet for trailing data or protocol extensions.

## 2. Ephemeral Session Model (`EphemeralSession`)

The `EphemeralSession` FlatBuffers schema defines the structure for managing temporary session states, crucial for key management and session resumption. Its definition is found in `KAIRO/schema/ephemeral_session.fbs`.

```flatbuffers
namespace aitcp;

table EphemeralSession {
  session_id:string;
  public_key:[ubyte];
  expiration_unix:long;
}

root_type EphemeralSession;
```

### Field Descriptions:

*   **`session_id`**: A unique string identifier for the ephemeral session.
*   **`public_key`**: The public key associated with this session, used for cryptographic operations within the session context.
*   **`expiration_unix`**: A Unix timestamp (long integer) indicating when the session is no longer valid.

## 3. Encryption and Authentication

AI-TCP packets are designed with strong cryptographic primitives:

*   **End-to-End Encryption**: The primary data (`encrypted_payload`) is encrypted using algorithms like ChaCha20-Poly1305, ensuring confidentiality. The `ephemeral_key` and `nonce` fields facilitate this.
*   **Digital Signatures**: The `signature` field, generated using Ed25519, provides strong authentication and integrity protection for the entire packet, preventing tampering and ensuring the sender's identity.

The logical structure of the header and payload (e.g., packet type, sequence number, source/destination addresses) is encapsulated within the `encrypted_payload` and must be decrypted to be accessed. The optional `header` and `payload` fields are exceptions for specific unencrypted data.
