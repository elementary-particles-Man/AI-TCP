# GG04: AI-TCP Security Policy

## 1. Purpose

This document establishes security guidelines for AI-TCP communication, focusing on confidentiality, integrity, and authentication.

## 2. Key Security Domains

| Domain         | Policy Summary |
|----------------|----------------|
| Authentication | All packets must include signed `origin_id` and optional token |
| Integrity      | Critical sections (e.g., reasoning_trace) require SHA256 hash |
| Confidentiality | Sensitive sections may use inline AES-256 encryption |
| Access Control | LLMs may validate source permissions using `auth_level` flag |

---

## 3. Security Field Templates

### Origin Signature

```yaml
security:
  origin_id: ai-node-73
  signature: "MEUCIQDz...YwIgWR=="  # Base64 encoded
  timestamp: 2025-06-22T15:02:12Z
```

### Hash-Guarded Content

```yaml
reasoning_trace:
  - step: 1
    input: "classify threat vector"
    output: "identified as network injection"
    hash: "2b1c0f...d91a"  # SHA256
```

### Optional AES Encryption

```yaml
confidential_block:
  encrypted: true
  algorithm: AES-256-GCM
  ciphertext: "4IvRb...BfzF=="
```

---

## 4. LLM Authentication Classes

| Level | Description |
|-------|-------------|
| open  | Accepts all sources, logs origin only |
| gated | Verifies known `origin_id` against whitelist |
| strict| Requires signature and token validation with expiration |

---

## 5. Secure Channel Declaration

```yaml
secure_channel:
  tls_version: "1.3"
  endpoint: "wss://ai-tcp.example.net/session"
  ephemeral_key: true
```

---

## 6. Threat Response Patterns

- Log and drop unsigned packets
- Forward `security.alert` to supervising node
- Downgrade to read-only compliance mode on integrity failure

---

## 7. References

- GG03: Fault Handling
- RFC 002: LLM Compliance Modes
- RFC 003: AI-TCP Packet Format
