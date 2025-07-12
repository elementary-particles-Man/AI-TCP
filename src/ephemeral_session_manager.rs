use rand::rngs::OsRng;
use x25519_dalek::{EphemeralSecret, PublicKey};

pub struct EphemeralSession {
    pub private: EphemeralSecret,
    pub public: PublicKey,
}

impl EphemeralSession {
    pub fn new() -> Self {
        let private = EphemeralSecret::new(OsRng);
        let public = PublicKey::from(&private);
        Self { private, public }
    }
}
