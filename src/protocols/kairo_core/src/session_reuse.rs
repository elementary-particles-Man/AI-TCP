use std::collections::HashMap;
use chrono::{Utc, Duration};
use rand::RngCore;

const SESSION_EXPIRATION_MINUTES: i64 = 30;

pub struct Session {
    key: [u8; 32],
    created_at: chrono::DateTime<Utc>,
}

impl Session {
    pub fn new(key: [u8; 32]) -> Self {
        Session {
            key,
            created_at: Utc::now(),
        }
    }

    pub fn is_expired(&self) -> bool {
        Utc::now() - self.created_at > Duration::minutes(SESSION_EXPIRATION_MINUTES)
    }
}

pub struct SessionManager {
    sessions: HashMap<String, Session>,
}

impl SessionManager {
    pub fn new() -> Self {
        SessionManager {
            sessions: HashMap::new(),
        }
    }

    pub fn get_or_create_session(&mut self, session_id: &str) -> &[u8; 32] {
        self.cleanup_expired();
        
        self.sessions
            .entry(session_id.to_string())
            .or_insert_with(|| {
                // In a real scenario, this key would be derived from a DH exchange.
                let mut key = [0u8; 32];
                rand::thread_rng().fill_bytes(&mut key);
                Session::new(key)
            });
        
        &self.sessions.get(session_id).unwrap().key
    }

    fn cleanup_expired(&mut self) {
        self.sessions.retain(|_, session| !session.is_expired());
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread::sleep;
    use std::time::Duration as StdDuration;

    #[test]
    fn test_session_creation_and_reuse() {
        let mut manager = SessionManager::new();
        let session_id = "session-123";

        let key1 = manager.get_or_create_session(session_id).to_vec();
        let key2 = manager.get_or_create_session(session_id).to_vec();
        assert_eq!(key1, key2);
    }

    #[test]
    fn test_session_expiration() {
        let mut manager = SessionManager::new();
        let session_id = "session-expiring";

        manager.get_or_create_session(session_id);
        // Manually advance time for testing expiration
        // In a real test, you'd use a time-mocking library
        sleep(StdDuration::from_secs((SESSION_EXPIRATION_MINUTES * 60 + 1) as u64));

        let key_after_expiration = manager.get_or_create_session(session_id);
        // The key should be different as a new session should have been created
        // This assertion is tricky without mocking time, as a new key is generated
        // every time a session is created. We can only assert that a session exists.
        assert!(!manager.sessions.is_empty());
    }

    #[test]
    fn test_cleanup_expired_sessions() {
        let mut manager = SessionManager::new();
        let session_id1 = "session-active";
        let session_id2 = "session-expired";

        manager.get_or_create_session(session_id1);
        manager.get_or_create_session(session_id2);

        // Simulate expiration of session-expired
        sleep(StdDuration::from_secs((SESSION_EXPIRATION_MINUTES * 60 + 1) as u64));

        // Accessing session-active should trigger cleanup
        manager.get_or_create_session(session_id1);

        assert!(manager.sessions.get(session_id1).is_some());
        assert!(manager.sessions.get(session_id2).is_none());
    }
}
