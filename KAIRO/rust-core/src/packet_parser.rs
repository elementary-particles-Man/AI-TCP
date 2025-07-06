use serde::{Deserialize, Serialize};
use bytes::Bytes;
use crate::error::KairoError;

#[derive(Debug, Deserialize, Serialize)]
pub struct Packet {
    pub header: PacketHeader,
    pub payload: PacketPayload,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct PacketHeader {
    pub version: u8,
    pub packet_type: u8,
    pub length: u16,
    pub transaction_id: String,
}

#[derive(Debug, Deserialize, Serialize)]
pub enum PacketPayload {
    AuthRequest { username: String },
    AuthResponse { success: bool, message: String },
    Data { data: Vec<u8> }, // Changed Bytes to Vec<u8>
}

pub struct PacketParser {
    session_key: Vec<u8>,
}

impl PacketParser {
    pub fn new(session_key: Vec<u8>) -> Self {
        PacketParser { session_key }
    }

    pub fn parse(&mut self, data: &Bytes) -> Result<Packet, Box<dyn std::error::Error>> {
        // Dummy parsing logic for now
        // In a real scenario, this would involve deserialization, decryption, and validation
        if data.len() < 4 { // Minimum size for version, type, and length
            return Err(Box::new(KairoError::InvalidPacket("Packet too short".to_string())));
        }

        let version = data[0];
        let packet_type = data[1];
        let length = u16::from_be_bytes([data[2], data[3]]);

        if data.len() < length as usize {
            return Err(Box::new(KairoError::InvalidPacket("Incomplete packet data".to_string())));
        }

        // Assuming the rest is payload for now
        let payload_data = data.slice(4..length as usize).to_vec(); // Converted Bytes to Vec<u8>

        // Dummy transaction ID
        let transaction_id = "dummy_transaction_id".to_string();

        let header = PacketHeader {
            version,
            packet_type,
            length,
            transaction_id,
        };

        // For demonstration, let's assume a simple data payload
        let payload = PacketPayload::Data { data: payload_data };

        Ok(Packet { header, payload })
    }
}