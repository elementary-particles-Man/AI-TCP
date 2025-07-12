#[test]
fn test_ephemeral_session() {
    use rust_core::ephemeral_session_manager::EphemeralSession;
    let session = EphemeralSession::new();
    assert!(session.public.as_bytes().len() == 32);
}
