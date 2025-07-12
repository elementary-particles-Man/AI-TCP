use x25519_dalek::{EphemeralSecret, PublicKey};
use rand::rngs::OsRng;

pub struct EphemeralResumption {
    pub session_id: String,
    pub old_public: PublicKey,
    pub new_private: EphemeralSecret,
    pub new_public: PublicKey,
}

impl EphemeralResumption {
    pub fn new(session_id: String, old_public: PublicKey) -> Self {
        let new_private = EphemeralSecret::new(OsRng);
        let new_public = PublicKey::from(&new_private);
        Self {
            session_id,
            old_public,
            new_private,
            new_public,
        }
    }
}
