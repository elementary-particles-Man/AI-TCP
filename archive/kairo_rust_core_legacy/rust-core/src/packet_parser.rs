use serde::{Deserialize, Serialize};
use bytes::Bytes;
use crate::error::KairoError;
use crate::ephemeral_session_generated::aitcp::EphemeralSession;
use flatbuffers::FlatBufferBuilder;

#[derive(Debug, Deserialize, Serialize)]
pub struct Packet {
    pub header: PacketHeader,
    pub payload: PacketPayload,
}

#[derive(Debug, Deserialize, Serialize)]
pub enum PacketType {
    AuthRequest = 0,
    AuthResponse = 1,
    Data = 2,
    FlatBuffersEphemeralSession = 3,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct PacketHeader {
    pub version: u8,
    pub packet_type: PacketType,
    pub length: u16,
    pub transaction_id: String,
}

#[derive(Debug, Deserialize, Serialize)]
pub enum PacketPayload {
    AuthRequest { username: String },
    AuthResponse { success: bool, message: String },
    Data { data: Vec<u8> },
    FlatBuffersEphemeralSession {
        session_id: String,
        public_key: Vec<u8>,
        expiration_unix: u64,
    },
}

pub struct PacketParser {
    session_key: Vec<u8>,
}

impl PacketParser {
    pub fn new(session_key: Vec<u8>) -> Self {
        PacketParser { session_key }
    }

    pub fn parse(&mut self, data: &Bytes) -> Result<Packet, Box<dyn std::error::Error>> {
        if data.len() < 4 {
            return Err(Box::new(KairoError::InvalidPacket("Packet too short".to_string())));
        }

        let version = data[0];
        let raw_packet_type = data[1];
        let length = u16::from_be_bytes([data[2], data[3]]);

        // Ensure the declared length is at least the size of the header (4 bytes)
        if length < 4 {
            return Err(Box::new(KairoError::InvalidPacket(format!("Invalid packet length: {} (must be at least 4)", length))));
        }

        if data.len() < length as usize {
            return Err(Box::new(KairoError::InvalidPacket("Incomplete packet data".to_string())));
        }

        let packet_type = match raw_packet_type {
            0 => PacketType::AuthRequest,
            1 => PacketType::AuthResponse,
            2 => PacketType::Data,
            3 => PacketType::FlatBuffersEphemeralSession,
            _ => return Err(Box::new(KairoError::InvalidPacket(format!("Unknown packet type: {}", raw_packet_type))))
        };

        let payload_data_slice = data.slice(4..length as usize);
        let payload;
        let transaction_id;

        match packet_type {
            PacketType::FlatBuffersEphemeralSession => {
                let ephemeral_session = match crate::ephemeral_session_generated::aitcp::root_as_ephemeral_session(&payload_data_slice) {
                    Ok(session) => session,
                    Err(e) => {
                        eprintln!("FlatBuffers parsing error: {:?}", e);
                        return Err(Box::new(KairoError::InvalidPacket(format!("FlatBuffers parsing error: {}", e))));
                    }
                };

                println!("Successfully parsed FlatBuffers EphemeralSession:");
                println!("  Session ID: {}", ephemeral_session.session_id().unwrap_or("[N/A]"));
                println!("  Public Key Length: {}", ephemeral_session.public_key().map_or(0, |key| key.len()));
                println!("  Expiration Unix: {}", ephemeral_session.expiration_unix());

                transaction_id = ephemeral_session.session_id().unwrap_or("").to_string();
                payload = PacketPayload::FlatBuffersEphemeralSession {
                    session_id: ephemeral_session.session_id().unwrap_or("").to_string(),
                    public_key: ephemeral_session.public_key().map_or(vec![], |k| k.bytes().to_vec()),
                    expiration_unix: ephemeral_session.expiration_unix(),
                };
            },
            _ => {
                transaction_id = "dummy_transaction_id".to_string();
                payload = PacketPayload::Data { data: payload_data_slice.to_vec() };
            }
        }

        let header = PacketHeader {
            version,
            packet_type,
            length,
            transaction_id,
        };

        Ok(Packet { header, payload })
    }

    pub fn build_ephemeral_session_packet(
        session_id: &str,
        public_key: &[u8],
        expiration_unix: u64,
    ) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
        let mut builder = FlatBufferBuilder::new();

        let session_id_fb = builder.create_string(session_id);
        let public_key_fb = builder.create_vector(public_key);

        let args = crate::ephemeral_session_generated::aitcp::EphemeralSessionArgs {
            session_id: Some(session_id_fb),
            public_key: Some(public_key_fb),
            expiration_unix,
        };

        let ephemeral_session_offset = crate::ephemeral_session_generated::aitcp::EphemeralSession::create(&mut builder, &args);
        builder.finish(ephemeral_session_offset, None);

        let flatbuffer_data = builder.finished_data().to_vec();

        let version: u8 = 1;
        let packet_type: u8 = PacketType::FlatBuffersEphemeralSession as u8;
        let length: u16 = (4 + flatbuffer_data.len()) as u16;

        let mut full_packet = Vec::with_capacity(length as usize);
        full_packet.push(version);
        full_packet.push(packet_type);
        full_packet.extend_from_slice(&length.to_be_bytes());
        full_packet.extend_from_slice(&flatbuffer_data);

        Ok(full_packet)
    }
}