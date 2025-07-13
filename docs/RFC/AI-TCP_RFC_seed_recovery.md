# AI-TCP Seed Node Recovery RFC

When all seed nodes become unreachable, isolated peers attempt recovery using cached trust data. The helper `restore_from_cache` in `src/mesh_address_allocator.rs` illustrates this flow.

## Fallback Flow

1. Read the local trusted peers cache.
2. Verify cached peers via self-signed WAU.
3. Promote a verifiable peer as a temporary seed.
4. Rebuild DHT and gossip tables from that peer.

This mechanism allows the mesh to survive extended outages without centralized coordination.
