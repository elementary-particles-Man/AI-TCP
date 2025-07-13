//! mesh_trust_calculator.rs
//! Implements Peer Review / Gossip based distributed trust score calculation.
//! Handles WAU (Who Are You) authentication and Sybil attack resistance.


// Temporarily define Scope here to avoid circular dependency in initial generation
#[allow(dead_code)]
#[derive(Debug, PartialEq, Clone, Copy)]
pub enum Scope {
    Personal = 0,
    Family,
    Group,
    Community,
    World,
}

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

        let peer_avg: f64 = if peer_scores.is_empty() {
            0.0
        } else {
            peer_scores.iter().sum::<f64>() / peer_scores.len() as f64
        };

        let mut trust_score = (weight_self * self_trust)
                            + (weight_peer * peer_avg)
                            + (weight_gossip * gossip_agreement);

        // Sybil attack resistance: Halve trust if insufficient peer reviews
        let min_peer_reviews = match scope {
            Scope::Personal => 1,
            Scope::Family => 3,
            _ => 5,
        };

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

    pub fn handle_community_risk(
        &self,
        current_trust_score: f64,
        external_gossip_scores: &[f64],
        internal_community_health: f64,
        scope: Scope,
    ) -> f64 {
        // TODO: Implement logic to prevent internal collapse or sybil attacks in high-trust communities.
        // Ensure external trust score diffusion is not inhibited by internal group dynamics.
        // Consider periodic external audits or trust score comparison with global mesh data.
        // This function will return an adjusted trust score for the community/node.

        let external_avg = if external_gossip_scores.is_empty() {
            0.0
        } else {
            external_gossip_scores.iter().sum::<f64>() / external_gossip_scores.len() as f64
        };

        let mut combined_trust = (current_trust_score * 0.5) + (external_avg * 0.5);

        // If internal community health is critically low, significantly discount internal scores.
        // This prevents a compromised internal group from faking high trust scores to the outside.
        if internal_community_health < 0.5 {
            // Prioritize external view if internal health is compromised.
            combined_trust = external_avg; 
        }

        // For World scope, potentially involve a global consensus or more stringent external audit.
        if scope == Scope::World {
            // Placeholder for World-specific validation logic
            combined_trust *= 0.9; // Example: slight discount for ultimate global consensus.
        }

        combined_trust.clamp(0.0, 1.0)
    }
}
