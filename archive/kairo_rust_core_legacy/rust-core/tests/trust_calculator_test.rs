#[path = "../../../../src/mesh_trust_calculator.rs"]
mod mesh_trust_calculator;
use mesh_trust_calculator::{TrustScoreCalculator, Scope};

#[test]
fn calculates_trust_score_correctly() {
    let score = TrustScoreCalculator::calculate_trust_score(
        0.6,
        &[0.8],
        0.7,
        Scope::Personal,
    );
    assert!((score - 0.7).abs() < f64::EPSILON);
}

#[test]
fn applies_sybil_penalty_when_peer_reviews_insufficient() {
    let score = TrustScoreCalculator::calculate_trust_score(
        0.6,
        &[0.8, 0.7],
        0.9,
        Scope::Group,
    );
    assert!((score - 0.36).abs() < f64::EPSILON);
}
