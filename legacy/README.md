# Legacy Implementations of AI-TCP

This directory contains previous proof-of-concept (PoC) implementations of the AI-TCP protocol in Python and Go. These implementations served as initial explorations and prototypes for various aspects of the protocol design.

With the decision to establish Rust as the canonical and primary implementation language for AI-TCP, these legacy versions are preserved here for historical reference, architectural comparison, and potential extraction of specific algorithms or logic that may be re-implemented in Rust.

## Comparison: Legacy (Python/Go) vs. Current (Rust)

| Feature/Aspect       | Legacy Implementations (Python/Go)                               | Current Implementation (Rust)                                    |
| :------------------- | :--------------------------------------------------------------- | :--------------------------------------------------------------- |
| **Primary Language** | Python, Go                                                       | Rust                                                             |
| **Purpose**          | Rapid prototyping, concept validation, initial feature exploration | Canonical, production-grade implementation, performance, security |
| **Key Strengths**    | Development speed, ecosystem for scripting/web services          | Memory safety, performance, concurrency, strong type system      |
| **Packet Structure** | Varied (e.g., custom serialization, JSON, protobuf)              | Standardized FlatBuffers (`KAIRO/schema/ai_tcp_packet.fbs`)      |
| **Cryptography**     | Library-dependent, potentially less rigorous integration         | Deeply integrated, leveraging `ed25519-dalek`, `chacha20poly1305` |
| **Concurrency**      | Python GIL limitations, Go goroutines                            | Rust's ownership model, `tokio` for async                       |
| **Error Handling**   | Language-specific exceptions/error returns                       | Rust's `Result` and `Option` types, robust error propagation    |
| **Performance**      | Generally lower than compiled languages                          | High performance, close to bare metal                            |
| **Memory Safety**    | Garbage collection, runtime checks                               | Compile-time guarantees, no garbage collector                    |
| **Target Use Case**  | Experimentation, simple CLI tools                                | Core protocol engine, high-throughput services                   |

## Contents:

*   `python/`: Contains Python-based PoC implementations.
*   `go/`: Contains Go-based PoC implementations.
