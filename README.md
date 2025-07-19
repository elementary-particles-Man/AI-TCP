# AI-TCP: Autonomous Intelligence Transmission Control Protocol

**AI-TCP** is a proposed international protocol framework for secure, neutral, and traceable inter-LLM communication in the age of autonomous intelligence.  
It is designed to enable resilient coordination between large language models (LLMs) across geopolitical, institutional, and ethical boundaries, under human-governed supervision.

# This comment is added for Git commit verification. (4th time)

This repository contains the complete draft structure, technical specification, and governance proposal for AI-TCP, as well as foundational documents for its inclusion in the "Magi System"—a tri-LLM distributed decision-making architecture.

## 📂 Repository Structure

- `bin/`: This directory is designated for compiled binary executables. All project-specific binaries should be placed here to maintain a clear separation from source code and other project assets. **Warning: Binaries found outside this directory will trigger administrative alerts.**

- `original_docs/`: Human-readable documentation from GPT/Gemini/GD.

- `structured_yaml/`: Structured YAML data following `master_schema_v1.yaml`.
- `structured_yaml/validated_yaml/`: YAML conforming to schema.
- `structured_yaml/docs/`: Documentation with embedded YAML metadata.

## 🧠 Foundational Philosophy: LSC

The AI-TCP protocol is built atop a flexible and universal logic framework called **LSC (Least Sufficient Condition)**.  
This philosophy document defines a non-coercive reasoning structure designed for both human and AI cooperation.

📄 [Read the full LSC specification](philosophy/LSC- The Universal Guidance.md)

## 🧠 Motivation

The rise of autonomous reasoning agents (LLMs) demands not just AI safety, but AI interoperability, neutrality, and traceability.  
**AI-TCP** provides a communication layer that is:

- LSC-compliant (Logical Structural Consensus)
- Human-auditable
- Standardizable at the IETF/IEEE/ITU levels

## 🔧 Key Components

- 📦 `master_schema_v1.yaml`: Defines all protocol layers
- ✉️ `ai_tcp_timeline.yaml`: Governance and development chronology
- 🏗️ `ai_tcp_poc_design.yaml`: Architecture and packet structure

## 🛠 CLI Tools

This repository is developing a suite of human-operated command-line interface (CLI) tools in Rust, designed for FlatBuffers-compliant, signed packet operations within the AI-TCP protocol. Each tool is clearly identifiable as belonging to AI-TCP, avoiding confusion with KAIRO components.

### AI-TCP CLI Tool Suite (Rust)

*   **`aictp-agent-setup`**: Agent Registration and Key Generation (no KAIRO connection required)
    ```bash
    aictp-agent-setup --id <agent_id> --output-dir <path/to/config>
    ```
*   **`aictp-send`**: Signed Packet Generation and Transmission
    ```bash
    aictp-send --agent-id <agent_id> --destination <address> --data <payload> [--json]
    ```
*   **`aictp-receive`**: Packet Reception, Verification, and Display
    ```bash
    aictp-receive --port <port> [--json]
    ```
*   **`aictp-log`**: Log Review and Inspection
    ```bash
    aictp-log --log-file <path/to/log> [--verbose]
    ```
*   **`aictp-revoke`**: Revocation Operations
    ```bash
    aictp-revoke --id <agent_id> --reason "<reason_for_revocation>"
    ```

**Transmission Specification:**

*   Default: FlatBuffers binary transmission/reception.
*   `--json` option: JSON serialization/deserialization only.
*   Server communication: `http://localhost:8080/send` / `/receive`.
*   All packets must include a sender's signature.

---

## 🌐 Future Goals

- RFC submission to IETF
- IEEE protocol registration
- Multi-vendor implementation trials (Gemini, GPT, openLLMs)

## 🤝 Contributors

- Human curator: elementary-particles-Man  
- Multi-agent authorship: GPT-4o / Gemini 1.5 / GD  

## 📄 License

This work is released under **CC0 1.0** — Public Domain Dedication.  
Reuse, derivative works, and standardization efforts are not only permitted but encouraged.

## 🚀 Task Automation and Validation

This project leverages an automated task execution and validation system, central to which are `task_bridge_runner.py` and the `validate_files` task.

### `task_bridge_runner.py`

`task_bridge_runner.py` acts as the orchestrator for various automated tasks within the AI-TCP project. It monitors for new task requests and dispatches them to appropriate handlers.

### `validate_files` Task

The `validate_files` task is a critical component for ensuring the integrity and correctness of specified files within the project. It performs checks such as file existence, size, and content hashing, and can integrate with `pytest` for more comprehensive validation.

#### Operational Principles

1.  **Zero-File Method for Task Initiation**:
    Tasks, including `validate_files`, are initiated using a "zero-file method." This means that task requests are communicated via a `new_task.json` file. Once `task_bridge_runner.py` processes this file, it is moved to an archive, effectively "zeroing out" the task initiation directory and preventing redundant execution. This ensures a clean, idempotent task queue.

2.  **Junction Premise for Path Handling**:
    The system is designed with the "junction premise" in mind, particularly for Windows environments. This implies that file paths, especially those passed to `validate_files`, should ideally be handled via directory junctions (symlinks) to abstract away complex or lengthy physical paths. This approach enhances portability, simplifies configuration, and mitigates issues related to path length limitations or special characters, ensuring robust operation across different development environments.

