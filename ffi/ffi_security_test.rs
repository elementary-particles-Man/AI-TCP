#[test]
fn test_replay_attack_guard() {
    use rust_core::replay_attack_guard::ReplayAttackGuard;
    let mut guard = ReplayAttackGuard::new();
    assert_eq!(guard.is_replay(1), false);
    assert_eq!(guard.is_replay(1), true);
}
