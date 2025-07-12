# AI-TCP Security RFC

- Replay Attack Mitigation
- Session Resumption Mechanism
- Ephemeral Key Rotation
- Signature Verification Flow
- FFI Binding considerations

## Session Resumption

The protocol allows resuming a dropped connection using an ephemeral key exchange. The FlatBuffers schema `ephemeral_session.fbs` describes the resumption request containing the `session_id`, the client's new public key and an expiration timestamp.

Upon receiving a resumption request the server rotates its own ephemeral key pair. It verifies the old public key associated with the session and responds with a new key. The resumed handshake mirrors the initial Diffie-Hellman exchange but binds the resumed connection to the original `session_id`.

This key rotation limits exposure of any long-lived credentials while still enabling seamless continuation of an interrupted session.
