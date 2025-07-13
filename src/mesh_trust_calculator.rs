//! mesh_trust_calculator.rs
//! Implements Peer Review / Gossip based distributed trust score calculation.
//! Handles WAU (Who Are You) authentication and Sybil attack resistance.

pub struct TrustScoreCalculator {}

impl TrustScoreCalculator {
    pub fn new() -> Self { Self {} }

    pub fn calculate_trust_score(
        self_trust: f64,
        peer_scores: &[f64],
        gossip_agreement: f64,
        scope: Scope,
    ) -> f64 {
        let weight_self = 0.4;
        let weight_peer = 0.4;
        let weight_gossip = 0.2;
        let min_peer_reviews = match scope {
            Scope::Personal => 1, // Only self-assessment needed
            Scope::Family => 3,   // Needs 3 peer reviews
            _ => 5, // Default for higher scopes
        };

        let peer_avg: f64 = if peer_scores.is_empty() { 0.0 } else { peer_scores.iter().sum::<f64>() / peer_scores.len() as f64 };

        let mut trust_score = (weight_self * self_trust) +
                              (weight_peer * peer_avg) +
                              (weight_gossip * gossip_agreement);

        // Sybil attack resistance: Halve trust if insufficient peer reviews
        if peer_scores.len() < min_peer_reviews {
            trust_score *= 0.5;
        }

        trust_score.clamp(0.0, 1.0)
    }

    pub fn verify_wa_u(trust_score: f64, scope: Scope) -> bool {
        let required_threshold = match scope {
            Scope::Personal => 0.25,
            Scope::Family => 0.50,
            Scope::Group => 0.75,
            Scope::Community => 0.90,
            Scope::World => 0.99,
        };
        trust_score >= required_threshold
    }
}
