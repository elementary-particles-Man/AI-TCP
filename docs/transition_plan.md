# AI-TCP API Transition Plan: From OpenAI Compatibility to Native AI-TCP

This document outlines the strategic plan for transitioning from the OpenAI-API compatibility layer to the native AI-TCP protocol. The goal is to guide developers through a smooth migration process while highlighting the significant advantages of the native AI-TCP API.

---

## 1. Executive Summary

The AI-TCP native API represents the future of secure, high-performance, and auditable AI communication. While an OpenAI-API compatibility layer was initially provided to ease adoption, it does not fully leverage the underlying KAIRO core's capabilities. This plan details a phased approach to encourage and facilitate migration to the native AI-TCP SDKs, ensuring developers can harness the full power of the platform.

---

## 2. Rationale for Transition

Migrating to the native AI-TCP API offers several critical benefits:

- **Enhanced Security:** Direct integration with the KAIRO core provides transparent, end-to-end encryption, signing, and secure session management, which are not fully exposed or optimized through the compatibility layer.
- **Superior Performance:** The native API is designed to optimize data flow, leveraging KAIRO's efficient compression (LZ4) and optimized packet handling, leading to lower latency and higher throughput.
- **Auditable Transactions (VoV):** Native AI-TCP packets are inherently auditable via the Voice of Verification (VoV) logging, ensuring integrity and non-repudiation for every transaction.
- **Future-Proofing:** All new features, performance enhancements, and security updates will be developed for the native AI-TCP API first.
- **Clear Incentive:** The native API will offer measurable improvements in latency, throughput, and security, providing a strong incentive for migration.
- **Stability:** The timeline is designed to ensure platform stability and give developers ample time to adapt.

---

## 3. Transition Phases

### Phase 1: Native API Launch & Compatibility (Current Phase)

- **Duration:** 6 months from the official launch of the first stable native SDKs.
- **Status:**
    - The native AI-TCP API (`/api/v1/aitcp`) is the **recommended** endpoint.
    - An OpenAI-API compatible endpoint is provided for backward compatibility.
- **Actions:**
    - All new documentation and tutorials will focus exclusively on the native API.
    - Performance benchmarks comparing the native API and the compatibility layer will be published.
    - The `aitcp-cli migrate` tool will be introduced to assist in automated code conversion.

### Phase 2: Deprecation of Compatibility Layer

- **Duration:** 6 months, starting after Phase 1 concludes.
- **Status:**
    - The OpenAI-API compatibility layer will be officially deprecated.
    - New feature development will cease for the compatibility layer.
    - Warning headers will be added to responses from the compatibility layer, advising migration.
- **Actions:**
    - Active outreach to developers still using the compatibility layer.
    - Enhanced support for migration queries.
    - Regular reminders about the upcoming removal.

### Phase 3: Removal of Compatibility Layer

- **Duration:** Immediate, after Phase 2 concludes.
- **Status:**
    - The OpenAI-API compatibility layer endpoints will be removed.
    - Requests to these endpoints will result in an HTTP 410 Gone status code.
- **Actions:**
    - Final communication regarding the complete removal.
    - Continued support for native AI-TCP API usage.

---

## 4. Migration Tools and Support

To facilitate a smooth transition, the following tools and resources will be provided:

### 4.1. AI-TCP SDKs

Official SDKs for popular languages (Go, Python, Rust) will provide idiomatic access to the native AI-TCP API, abstracting the complexities of KAIRO integration.

### 4.2. `aitcp-cli migrate` Tool

A command-line interface (CLI) tool designed to automate the migration of existing codebases from OpenAI API calls to native AI-TCP SDK calls.

- **Purpose:** Reduce manual effort and potential errors during the migration process.
- **Functionality:**
    - Scans a project directory for code using the OpenAI client libraries (e.g., Python `openai` library).
    - Automatically refactors the code to use the equivalent native AI-TCP SDK methods.
    - Provides a report of all changes made.
- **Example Usage:**
  ```bash
  aitcp-cli migrate --path ./my_project --from openai --to aitcp-native
  ```