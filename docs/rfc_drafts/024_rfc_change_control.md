# RFC Change Control for AI-TCP

This document defines the procedures for submitting, evaluating, approving, and implementing changes to the AI-TCP protocol and its canonical representations.

---

## 📜 Scope

This RFC governs changes to:
- Master YAML schema
- Markdown RFCs
- Graph payload syntax (Mermaid/HTML)
- Reference implementations
- Compliance test vectors

---

## 🔁 Change Proposal Lifecycle

### Step 1: Draft Proposal
- Authored in Markdown using RFC template.
- Assigned RFC number if accepted for review.

### Step 2: AI Review
- GPT validates structural integrity, logic flow, and semantic alignment with master schema.
- Gemini reformats and annotates for public consumption.

### Step 3: Codex Validation
- YAML diff or patch is validated using Codex test runners.
- All schema-altering proposals require formal YAML delta.

### Step 4: Principal Review
- Human lead evaluates alignment with project goals.
- Final decision: Accept / Reject / Revise and Resubmit.

### Step 5: Version Control and Publication
- All accepted changes are committed to Git.
- Updated RFCs must include:
  - Version number
  - Date
  - Author/AI attribution
  - Summary of changes

---

## 🧾 Change Types

| Type      | Description |
|-----------|-------------|
| Minor     | Grammar fixes, clarifications (no logic change) |
| Patch     | Minor schema additions/removals |
| Major     | Protocol behavior changes or RFC restructuring |
| Deprecation | Component marked obsolete, with rationale |

---

## 📊 Status Tags

Each RFC or schema must include a status tag:

- `DRAFT` – Under development
- `REVIEW` – Submitted for formal review
- `ACCEPTED` – Approved for canonical use
- `SUPERSEDED` – Replaced by a newer version
- `DEPRECATED` – No longer recommended

---

## 🔐 Integrity Assurance

- All changes must pass integrity checks:
  - Schema conformance
  - Reference sync validation
  - Authorship attribution
- Discrepant branches are flagged by protocol stewards.

---

## 📅 Change Windows

Major changes may only be approved during scheduled governance windows or crisis override.

