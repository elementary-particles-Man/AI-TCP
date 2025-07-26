use ed25519_dalek::{Keypair, SigningKey, VerifyingKey, Signature};
use rand::rngs::OsRng;
use hex::{encode, decode};
use std::fs;
use std::path::Path;
use serde::{Serialize, Deserialize};
use chrono::{DateTime, Utc};
use ed25519_dalek::Signer;
use ed25519_dalek::Verifier;

#[derive(Debug, Serialize, Deserialize)]
pub struct AgentConfig {
    pub id: String,
    pub public_key: String,
    pub secret_key: String,
}

#[derive(Debug)]
pub enum CryptoError {
    Io(std::io::Error),
    Hex(hex::FromHexError),
    Signature(ed25519_dalek::SignatureError),
    Serde(serde_json::Error),
    Other(String),
}

impl From<std::io::Error> for CryptoError {
    fn from(err: std::io::Error) -> Self {
        CryptoError::Io(err)
    }
}

impl From<hex::FromHexError> for CryptoError {
    fn from(err: hex::FromHexError) -> Self {
        CryptoError::Hex(err)
    }
}

impl From<ed25519_dalek::SignatureError> for CryptoError {
    fn from(err: ed25519_dalek::SignatureError) -> Self {
        CryptoError::Signature(err)
    }
}

impl From<serde_json::Error> for CryptoError {
    fn from(err: serde_json::Error) -> Self {
        CryptoError::Serde(err)
    }
}

pub fn generate_keypair() -> Result<(String, String), CryptoError> {
    let mut csprng = OsRng{};
    let signing_key = SigningKey::generate(&mut csprng);
    let public_key_hex = encode(signing_key.verifying_key().as_bytes());
    let secret_key_hex = encode(signing_key.to_bytes());
    Ok((public_key_hex, secret_key_hex))
}

pub fn save_agent_config(config: &AgentConfig, path: &Path) -> Result<(), CryptoError> {
    let json = serde_json::to_string_pretty(config)?;
    fs::write(path, json)?;
    Ok(())
}

pub fn load_agent_config(id: &str) -> Result<AgentConfig, CryptoError> {
    let file_name = format!("agent_configs/{}.json", id);
    let path = Path::new(&file_name);
    if !path.exists() {
        return Err(CryptoError::Other(format!("Agent config for {} not found", id)));
    }
    let json = fs::read_to_string(path)?;
    let config: AgentConfig = serde_json::from_str(&json)?;
    Ok(config)
}

pub fn sign_payload(payload: &[u8], secret_hex: &str) -> Result<String, CryptoError> {
    let secret_bytes = decode(secret_hex)?;
    let signing_key = SigningKey::from_bytes(&secret_bytes)
        .map_err(|e| CryptoError::Signature(e))?;
    let signature = signing_key.sign(payload);
    Ok(encode(signature.to_bytes()))
}

pub fn verify_signature(payload: &[u8], signature_hex: &str, public_hex: &str) -> Result<bool, CryptoError> {
    let public_bytes = decode(public_hex)?;
    let verifying_key = VerifyingKey::from_bytes(&public_bytes)
        .map_err(|e| CryptoError::Signature(e))?;
    let signature_bytes = decode(signature_hex)?;
    let signature = Signature::from_bytes(&signature_bytes)
        .map_err(|e| CryptoError::Signature(e))?;
    Ok(verifying_key.verify(payload, &signature).is_ok())
}