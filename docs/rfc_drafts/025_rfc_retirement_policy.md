# RFC Retirement Policy for AI-TCP

This document outlines the policies, criteria, and procedures for retiring RFCs and protocol modules within the AI-TCP ecosystem.

---

## 🪦 Definition of Retirement

A document or module is considered "retired" when it is:
- No longer aligned with the current implementation.
- Superseded by a more recent, actively maintained standard.
- Obsolete due to architectural restructuring.

---

## 📜 Retirement Criteria

| Criterion | Description |
|----------|-------------|
| Obsolescence | The standard is outdated or replaced. |
| Redundancy  | Fully covered by another canonical document. |
| Invalidated | Proven incompatible or harmful. |
| Deprecated | Marked as discouraged for future use. |

---

## 🔁 Retirement Process

### Step 1: Proposal for Retirement
- Authored as a markdown RFC.
- Includes rationale, impact assessment, and replacement strategy (if any).

### Step 2: AI-TCP Steward Review
- Assessed for risk and dependency scope.
- Reviewed by lead AI(s) and human lead.

### Step 3: Decision and Tagging
- Status changed to `RETIRED` and archived under historical documents.
- Tagged with retirement reason and reference to successor (if applicable).

### Step 4: Implementation
- Deprecated identifiers removed from schema registry.
- Archive maintained in the `/retired/` directory.

---

## 🧭 Successor Mapping

Each retired RFC must include:
- Successor RFC ID (if available)
- Migration instructions or legacy compatibility notes
- Known implementation impact

---

## 🧩 Status Tags (Superset)

| Tag | Meaning |
|-----|---------|
| DRAFT | Under development |
| REVIEW | Under evaluation |
| ACCEPTED | Approved for use |
| SUPERSEDED | Replaced by newer version |
| RETIRED | Obsolete and archived |

---

## 🧪 Verification

- A retired document must pass:
  - Deprecation integrity checks
  - Linkage resolution (e.g., successors)
  - Final review by AI-human co-leads

---

## 📂 Archival Format

- File path: `/docs/rfc_retired/###_original_title.md`
- Metadata block must include:
  - Retirement date
  - Decision authority
  - Successor or reason for discontinuation

