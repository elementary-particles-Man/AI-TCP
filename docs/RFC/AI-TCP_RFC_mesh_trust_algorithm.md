# AI-TCP Mesh Trust Algorithm RFC

This RFC describes how nodes calculate distributed trust scores across the mesh network. The reference implementation lives in `src/mesh_trust_calculator.rs`.

## Distributed Score Calculation

Each node combines its own self score, peer feedback and observed gossip agreement:

```rust
// src/mesh_trust_calculator.rs
let weight_self = 0.4;
let weight_peer = 0.4;
let weight_gossip = 0.2;
let peer_avg = peer_scores.iter().sum::<f64>() / peer_scores.len() as f64;
let mut trust_score = (weight_self * self_trust)
                    + (weight_peer * peer_avg)
                    + (weight_gossip * gossip_agreement);
```

## Sybil Resistance & Peer Review

A minimum number of peer reviews is required per scope. If not met, the trust score is halved to reduce influence from potential Sybil nodes.

## Hysteresis Handling

`mesh_scope_manager.rs` applies hysteresis so scope changes only occur after the score remains above or below thresholds for several cycles. Trust computation should therefore retain recent history rather than react immediately.
