use std::collections::HashMap;
use std::time::{Duration, Instant};

const SESSION_LIFETIME_SECONDS: u64 = 300; // A session is valid for 5 minutes

/// Represents a secure session with a shared key.
pub struct Session {
    pub key: [u8; 32],
    created_at: Instant,
}

impl Session {
    /// Creates a new session with a given key.
    fn new(key: [u8; 32]) -> Self {
        Self {
            key,
            created_at: Instant::now(),
        }
    }

    /// Checks if the session has exceeded its lifetime.
    fn is_expired(&self) -> bool {
        self.created_at.elapsed() > Duration::from_secs(SESSION_LIFETIME_SECONDS)
    }
}

/// Manages secure sessions, providing creation, retrieval, and cleanup.
pub struct SessionManager {
    sessions: HashMap<String, Session>,
}

impl SessionManager {
    pub fn new() -> Self {
        SessionManager {
            sessions: HashMap::new(),
        }
    }

    /// Retrieves an existing session key or creates a new one if it doesn't exist or is expired.
    pub fn get_or_create_session_key(&mut self, session_id: &str) -> &[u8; 32] {
        self.cleanup_expired_sessions();
        
        let session = self.sessions
            .entry(session_id.to_string())
            .or_insert_with(|| {
                let mut key = [0u8; 32];
                // Using a CSPRNG to generate a secure random key.
                // Note: rand crate needs to be added to Cargo.toml
                rand::RngCore::fill_bytes(&mut rand::thread_rng(), &mut key);
                Session::new(key)
            });
        
        &session.key
    }

    /// Removes all expired sessions from the manager.
    fn cleanup_expired_sessions(&mut self) {
        self.sessions.retain(|_id, session| !session.is_expired());
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread::sleep;

    #[test]
    fn test_session_creation_and_reuse() {
        let mut manager = SessionManager::new();
        let session_id = "session-123";

        let key1_ptr = manager.get_or_create_session_key(session_id) as *const u8;
        let key2_ptr = manager.get_or_create_session_key(session_id) as *const u8;

        assert_eq!(key1_ptr, key2_ptr, "Session key should be reused for the same ID");
        assert_eq!(manager.sessions.len(), 1);
    }

    #[test]
    fn test_session_expiration_and_cleanup() {
        let mut manager = SessionManager::new();
        let session_id = "session-expiring";

        manager.get_or_create_session_key(session_id);
        assert_eq!(manager.sessions.len(), 1);

        // Advance time past expiration
        sleep(Duration::from_secs(SESSION_LIFETIME_SECONDS + 1));

        // Accessing a session should trigger cleanup
        let _ = manager.get_or_create_session_key("another-session");
        assert_eq!(manager.sessions.len(), 1, "Expired session should be cleaned up");
        assert!(manager.sessions.get(session_id).is_none(), "Expired session should be removed");
    }

    #[test]
    fn test_multiple_sessions() {
        let mut manager = SessionManager::new();
        manager.get_or_create_session_key("session-A");
        manager.get_or_create_session_key("session-B");
        manager.get_or_create_session_key("session-C");
        assert_eq!(manager.sessions.len(), 3);
    }
}
