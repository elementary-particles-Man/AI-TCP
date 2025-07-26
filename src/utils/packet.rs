use flatbuffers::{FlatBufferBuilder, WIPOffset};
use super::aitcp::AITcpPacket;
use super::aitcp::AITcpPacketArgs;

#[derive(Debug)]
pub enum PacketError {
    Flatbuffers(String),
    Other(String),
}

#[allow(dead_code)]
#[allow(unused_imports)]
mod aitcp {
    include!(concat!(env!("OUT_DIR"), "/AITCP/ai_tcp_packet_generated.rs"));
    include!(concat!(env!("OUT_DIR"), "/aitcp/ephemeral_session_generated.rs"));
}

pub fn build_packet<'a>(builder: &'a mut FlatBufferBuilder, version: u8, ephemeral_key: Vec<u8>, nonce: Vec<u8>, encrypted_sequence_id: Vec<u8>, encrypted_payload: Vec<u8>, signature: Vec<u8>, header: Option<Vec<u8>>, payload: Option<Vec<u8>>, footer: Option<Vec<u8>>) -> WIPOffset<AITcpPacket<'a>> {
    let ephemeral_key_offset = builder.create_vector(&ephemeral_key);
    let nonce_offset = builder.create_vector(&nonce);
    let encrypted_sequence_id_offset = builder.create_vector(&encrypted_sequence_id);
    let encrypted_payload_offset = builder.create_vector(&encrypted_payload);
    let signature_offset = builder.create_vector(&signature);

    let header_offset = header.map(|h| builder.create_vector(&h));
    let payload_offset = payload.map(|p| builder.create_vector(&p));
    let footer_offset = footer.map(|f| builder.create_vector(&f));

    let args = AITcpPacketArgs {
        version,
        ephemeral_key: Some(ephemeral_key_offset),
        nonce: Some(nonce_offset),
        encrypted_sequence_id: Some(encrypted_sequence_id_offset),
        encrypted_payload: Some(encrypted_payload_offset),
        signature: Some(signature_offset),
        header: header_offset,
        payload: payload_offset,
        footer: footer_offset,
    };
    AITcpPacket::create(builder, &args)
}

pub fn serialize_packet(packet: WIPOffset<AITcpPacket>) -> Vec<u8> {
    let mut builder = FlatBufferBuilder::new();
    builder.finish(packet, None);
    builder.finished_data().to_vec()
}

pub fn deserialize_packet(bytes: &[u8]) -> Result<AITcpPacket, PacketError> {
    let packet = flatbuffers::root::<AITcpPacket>(bytes);
    Ok(packet)
}
