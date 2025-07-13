# AI-TCP Mesh Seed Node Testing RFC

This RFC describes the test scenarios for verifying Seed Node recovery,
trusted_peers cache fallback, and quorum-based temporary Seed Node promotion.

## Key Points
- Isolated Node self-signature with WAU
- Quorum Peer Review flow
- DHT/Gossip re-establishment
- Test patterns for failure/recovery cycles

This complements seed_node_recovery_test.rs.
