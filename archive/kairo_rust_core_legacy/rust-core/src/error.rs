use std::fmt;

#[derive(Debug)]
pub enum KairoError {
    InvalidPacket(String),
    // Add other error types as needed
}

impl fmt::Display for KairoError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            KairoError::InvalidPacket(msg) => write!(f, "Invalid Packet: {}", msg),
        }
    }
}

impl std::error::Error for KairoError {}