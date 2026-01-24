# civic-recall-pipeline

**Transparent, auditable reference model of a civic-content ranking system**

This repository contains an **audit-first reference implementation** of a simplified
civic-content ranking pipeline. It is designed to demonstrate *how* ranking decisions
can be made **legible, reviewable, and contestable** — not to optimize engagement or
predict user behavior.

---

## What this is

This project is a **reference model**, not a production system.

It shows, end-to-end:

1. **Recall** — how content is admitted into consideration (by bucket, not virality)
2. **Eligibility** — how *narrow, explicit exclusions* are applied
3. **Scoring** — how public-interest scores are computed with transparent multipliers
4. **Ranking** — how final selection occurs under simple, inspectable constraints

Every decision produces a **structured audit log**, which can be converted into a
**human-readable summary** explaining *what happened to each post, and why*.

---

## What this is not

- ❌ Not a production recommendation system  
- ❌ Not an engagement-optimized or ad-driven model  
- ❌ Not a machine-learned black box  
- ❌ Not a claim about how any specific platform operates  

This code intentionally favors **clarity over performance** and **explainability over scale**.

---

## Why this exists

Public debate about content ranking often fails because:

- Decisions are **opaque**
- Explanations are **post-hoc or informal**
- Audits are **impossible without internal access**

This project demonstrates that a ranking pipeline can be:

- Deterministic
- Explicit in its trade-offs
- Auditable *after the fact*
- Explainable to non-engineers

---

## For press & regulators (short)

This repository provides a **concrete, inspectable artifact** for discussions about
algorithmic accountability.

It allows reviewers to see:

- Where discretion exists
- Where exclusions are applied
- Where demotion occurs (and where it does not)
- How alternative policy choices would change outcomes

No access to proprietary data or systems is required.

---

## Outputs

The pipeline produces:

- `audit_log.json` — machine-readable decision trace
- Human-readable summaries explaining outcomes per item
- Deterministic rankings reproducible from inputs

These artifacts are suitable for:
- Oversight review
- Expert analysis
- Journalistic inspection
- Policy comparison

---

## Repository structure (v0.1)
├── civic_recall_pipeline.py      # Core pipeline
├── audit_log.json                # Structured audit output (example)
├── audit_summary.py              # Human-readable summary generator
├── README.md
├── LICENSE
└── docs/                         # (planned)

---

## Versioning

- **v0.1** — Initial audit-first reference release  
- Future versions may add:
  - Policy-mapping notes
  - Alternative constraint models
  - Visualization of decision flow

---

## License

MIT — free to use, adapt, and critique.
