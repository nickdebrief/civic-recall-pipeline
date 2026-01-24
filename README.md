civic-recall-pipeline

Transparent, auditable reference model of a civic-content ranking system

---

## Overview

This repository contains an audit-first reference implementation of a civic-content ranking pipeline.

**Audience note:** This repository is written to be readable by journalists, regulators, civil-society reviewers, and non-technical audiences, as well as engineers.

It demonstrates — in plain code and plain language — how a platform could rank public-interest content while preserving:
- Transparency
- Procedural fairness
- Narrow, explainable exclusions
- A complete, reviewable decision trail

The pipeline is intentionally simple, explicit, and inspectable.
It is designed to be understood, not optimized.

See the `/docs` directory for example audit artifacts, including a plain-English audit summary and a machine-readable audit log.

---

## For press & regulators

This repository provides a transparent reference model for how content-ranking systems can be designed to support public accountability.

Modern ranking systems shape public discourse, yet their decision logic is typically opaque, proprietary, or framed as too complex to explain. This project demonstrates that ranking decisions can be made legible, reviewable, and contestable without exposing user data or platform-specific trade secrets.

What this model demonstrates
	- That content selection can be broken into explicit, inspectable stages  
  *(recall → eligibility → scoring → ranking)*
	-	That narrow exclusions (e.g. spam, legal prohibition) can be applied before ranking, and documented clearly
	-	That soft demotions can be disclosed as named factors, rather than hidden penalties
	-	That every decision can produce a machine-readable audit log, convertible into a plain-English explanation of what happened and why

What this model does not claim
	-	It does not describe how any specific platform currently operates
	-	It does not optimize engagement, growth, or advertising outcomes
	-	It does not rely on machine-learning opacity or behavioral prediction
	-	It does not require access to personal data to explain outcomes

---

## What this is

This project is:
	-	A reference model for civic-content ranking
	-	An explicit, stage-by-stage pipeline with no hidden logic
	-	A demonstration of how auditability can be built in by design
	-	A tool for discussion, oversight, critique, and education

It produces both:
	-	A machine-readable audit log (JSON)
	-	A human-readable audit summary (Markdown / TXT)

Every decision has a recorded reason.

---

## What this is not

This project is not:
	-	❌ A production recommender system
	-	❌ An engagement-optimized feed algorithm
	-	❌ A machine-learning model
	-	❌ A claim about how any real platform currently operates

It does not attempt to reverse-engineer proprietary systems.
It does not rely on opaque scoring or hidden signals.

This is a reference, not an accusation.

---

## Why this matters

For regulators, journalists, and civil-society reviewers, the key question is often not “what content went viral?” but:

Why was this content included, excluded, or deprioritized — and can that decision be independently reviewed?

This project shows that such explanations are technically feasible, even in simplified form, and that claims of “algorithmic complexity” should not preclude meaningful oversight.

The code is intentionally minimal. Its purpose is not performance, but demonstrability.

---

## Core design principles

	1.	Audit before optimization
Decisions are logged before they are justified or defended.
	2.	Explicit stages — no black boxes
Each step is named, bounded, and inspectable.
	3.	Narrow exclusions only
Content is excluded only for clearly defined, high-confidence reasons
(e.g. spam, legal prohibition, direct incitement).
	4.	Transparent soft demotion
Any demotion includes explicit multipliers and recorded factors.
	5.	Human-readable explanations matter
A plain-English audit summary is generated alongside raw logs.

---

## Pipeline stages

The pipeline proceeds through four explicit stages:

Recall → Eligibility → Scoring → Ranking

---

1. Recall (candidate admission)

Content is admitted into consideration via explicit buckets with quotas, such as:
	-	Primary submissions (first-hand, evidence-bearing)
	-	Institutional records
	-	Low-visibility authors
	-	Topic expansion

Recall is inclusive by design.
No content is excluded at this stage.

---

2. Eligibility (narrow exclusions)

Only hard, high-confidence exclusions apply, for example:
	-	Automated spam / coordinated inauthentic behavior
	-	Binding legal prohibitions
	-	Direct incitement to violence
	-	Proven fabrication

If excluded, the reason is logged and no further scoring occurs.

---

3. Scoring (public-interest oriented)

Eligible content receives a public-interest score, based on factors such as:
	-	Evidence strength
	-	Institutional relevance
	-	First-hand reporting
	-	Time sensitivity

Optional soft demotion multipliers may apply, but are always:
	-	Explicit
	-	Recorded
	-	Inspectable

No engagement metrics are used.

---

4. Ranking (simple, constrained)

Content is ranked by final score, with optional transparent constraints
(e.g. per-author caps).

Each selection or skip is logged with a reason.

---

## Auditability

Two complementary artifacts are produced:

1. Machine-readable audit log (JSON)
	-	Every decision, stage, reason, and factor
	-	Suitable for inspection, archival use, or external review

2. Human-readable audit summary (Markdown / TXT)
	-	One-page explanation of
“What happened to each post — and why”
	-	Designed for journalists, regulators, and non-technical reviewers

No decision exists without an explanation.

---

## Why this exists

Public-interest content systems increasingly affect:
	-	Democratic accountability
	-	Whistleblowing visibility
	-	Journalistic reach
	-	Regulatory oversight

Yet the logic governing visibility is often:
	-	Opaque
	-	Unreviewable
	-	Non-explainable after the fact

This project shows that another approach is possible —
one where ranking logic can be audited, explained, and challenged.

---

## Status
	-	Version: v0.1
	-	Nature: Reference / demonstrator
	-	Stability: Conceptually stable, intentionally minimal

Future versions may expand documentation, examples, and test fixtures,
but the core principles are expected to remain.

---

## License

MIT License — free to use, adapt, critique, or extend.
