use x25519_dalek::{EphemeralSecret, PublicKey};
use rand::rngs::OsRng;

pub struct SessionResumption {
    pub old_public: PublicKey,
    pub new_private: EphemeralSecret,
    pub new_public: PublicKey,
}

impl SessionResumption {
    pub fn new(old_public: PublicKey) -> Self {
        let new_private = EphemeralSecret::new(OsRng);
        let new_public = PublicKey::from(&new_private);
        Self { old_public, new_private, new_public }
    }
}
