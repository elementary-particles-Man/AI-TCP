use std::collections::HashSet;

pub struct ReplayAttackGuard {
    seen_sequence: HashSet<u64>,
}

impl ReplayAttackGuard {
    pub fn new() -> Self { Self { seen_sequence: HashSet::new() } }

    pub fn is_replay(&mut self, seq: u64) -> bool {
        if self.seen_sequence.contains(&seq) {
            true
        } else {
            self.seen_sequence.insert(seq);
            false
        }
    }
}
