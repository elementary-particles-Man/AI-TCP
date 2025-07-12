# AI-TCP Core RFC

- Ephemeral DH Session Handshake
- Encrypted Sequence ID (LE)
- FlatBuffers packet schema: ai_tcp_packet_generated.fbs
- End-to-End Signature with Ed25519
- Reconnection / Resumption flow
- Signature verification at Node level

## Secure API Endpoint

The project provides an HTTP endpoint `/api/secure` used for secure task
exchange. Clients send a POST request containing a JSON body with the
following fields:

```json
{
  "task_id": "string",
  "payload": "string",
  "session_key": "string"
}
```

The `session_key` must be exactly 32 bytes. Requests with invalid key length
return an error.

On success the server responds with:

```json
{
  "status": "success",
  "received_task_id": "...",
  "processed_payload": "...",
  "validated_session_key": true
}
```

The session key is intended to be ephemeral and generated for each session.
