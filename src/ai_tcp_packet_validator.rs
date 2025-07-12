use crate::ai_tcp_packet_generated::aitcp as fb;
use crate::signature::verify_ed25519;
use ed25519_dalek::{VerifyingKey, Signature as Ed25519Signature};

pub fn validate_ai_tcp_packet(
    packet: &fb::AITcpPacket,
    verifying_key: &VerifyingKey,
    expected_sequence: u64,
) -> bool {
    // TODO: Same logic as Mesh, but with AI-TCP Session binding
    true
}
