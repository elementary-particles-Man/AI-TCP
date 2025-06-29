# AI-TCP: Autonomous Intelligence Transmission Control Protocol

**AI-TCP** is a proposed international protocol framework for secure, neutral, and traceable inter-LLM communication in the age of autonomous intelligence.  
It is designed to enable resilient coordination between large language models (LLMs) across geopolitical, institutional, and ethical boundaries, under human-governed supervision.

# This comment is added for Git commit verification. (4th time)

This repository contains the complete draft structure, technical specification, and governance proposal for AI-TCP, as well as foundational documents for its inclusion in the "Magi System"—a tri-LLM distributed decision-making architecture.

## 📂 Repository Structure

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

- `graph_sender.py` – copy an AI-TCP YAML packet to `output/` and print its graph and trace.
- `graph_receiver.py` – watch `input/` for YAML packets and display their contents.
- `scripts/convert_mmd_to_images.js` – render `.mmd` files from `mermaid_blocks/` into `generated_images/` using [mmdc](https://github.com/mermaid-js/mermaid-cli).

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

