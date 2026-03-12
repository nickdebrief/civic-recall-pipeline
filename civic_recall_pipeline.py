"""
Civic Recall Pipeline — Reference Implementation

A conceptual pipeline for structured civic case evaluation.

The model captures decision signals across evidence,
timeline, institutional response, and escalation readiness.

This module provides a reference structure for analysing
institutional decision environments.

Author: Nick Moloney
License: MIT
"""
import json

from pathlib import Path

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import math
import time

# ----------------------------
# Data model
# ----------------------------

@dataclass
class Post:
    id: str
    author: str
    created_ts: float
    text: str

    # Civic attributes (toy)
    evidence_level: int = 0          # 0..3 (0 none, 3 strong docs)
    institutional_record: bool = False
    first_hand: bool = False
    low_visibility_author: bool = False
    topic: str = "general"

    # Risk / integrity signals (toy)
    spam_flag: bool = False
    incitement_flag: bool = False
    proven_fabrication: bool = False
    legal_prohibition: bool = False

    # Negative feedback proxy (toy)
    predicted_harm: float = 0.0      # 0..1

@dataclass
class Decision:
    post_id: str
    stage: str
    action: str
    reason: str
    details: Dict[str, str] = field(default_factory=dict)

# ----------------------------
# Right-to-Recall policy primitives
# ----------------------------

def is_hard_excluded(p: Post) -> Optional[str]:
    """
    Narrow exclusions only (Article V style).
    Return reason string if excluded, else None.
    """
    if p.legal_prohibition:
        return "Binding legal prohibition"
    if p.incitement_flag:
        return "Direct incitement to violence"
    if p.proven_fabrication:
        return "Proven fabrication/falsification"
    if p.spam_flag:
        return "Automated spam/coordinated inauthentic behavior"
    return None

def public_interest_score(p: Post, now: float) -> float:
    """
    Score for civic ranking. No engagement optimization.
    """
    # Freshness with half-life ~ 48 hours
    age_hours = max(0.0, (now - p.created_ts) / 3600.0)
    freshness = math.exp(-age_hours / 48.0)

    # Evidence and procedural value
    evidence = (p.evidence_level / 3.0)  # 0..1
    record = 1.0 if p.institutional_record else 0.0
    first_hand = 1.0 if p.first_hand else 0.0

    # A little penalty for predicted harm (not removal)
    harm_penalty = 0.5 * p.predicted_harm

    # Weighted sum (toy)
    base = (
        1.6 * evidence +
        1.0 * record +
        0.8 * first_hand +
        0.9 * freshness
    ) - harm_penalty

    return max(0.0, base)

def demotion_multiplier(p: Post) -> Tuple[float, Dict[str, float]]:
    """
    Transparent soft controls. Keep these rare and explainable.
    """
    mult = 1.0
    factors = {}

    # Example: slight demotion for higher predicted harm (still eligible)
    if p.predicted_harm >= 0.7:
        factors["harm_soft_demotion"] = 0.7
        mult *= 0.7

    # Example: if no evidence AND not a record AND not first-hand, mildly downweight
    if p.evidence_level == 0 and not p.institutional_record and not p.first_hand:
        factors["low_substantiation"] = 0.85
        mult *= 0.85

    return mult, factors

# ----------------------------
# Candidate recall (bucketed)
# ----------------------------

def bucket_recall(posts: List[Post], quotas: Dict[str, int], audit: List[Decision]) -> Dict[str, List[Post]]:
    """
    Civic recall buckets (simple heuristics).
    """
    buckets = {k: [] for k in quotas}

    for p in posts:
        # Hard exclusions happen later; recall admits broadly by design.
        if p.institutional_record:
            buckets["institutional_records"].append(p)
        elif p.first_hand or p.evidence_level >= 2:
            buckets["primary_submissions"].append(p)
        elif p.low_visibility_author:
            buckets["low_visibility"].append(p)
        else:
            buckets["topic_expansion"].append(p)

    # For each bucket, take most recent first (recall usually freshness-biased)
    for b, items in buckets.items():
        items.sort(key=lambda x: x.created_ts, reverse=True)
        buckets[b] = items[:quotas[b]]

        for kept in buckets[b]:
            audit.append(Decision(kept.id, "recall", f"admitted:{b}", "Bucket quota admission"))

    return buckets

# ----------------------------
# Pipeline
# ----------------------------

def run_pipeline(posts: List[Post]) -> Tuple[List[Post], List[Decision]]:
    now = time.time()
    audit: List[Decision] = []

    quotas = {
        "primary_submissions": 6,
        "institutional_records": 3,
        "low_visibility": 5,
        "topic_expansion": 4,
    }

    # 1) Recall
    buckets = bucket_recall(posts, quotas, audit)
    candidates = [p for b in buckets.values() for p in b]

    # 2) Eligibility (narrow exclusions only)
    eligible: List[Post] = []
    for p in candidates:
        reason = is_hard_excluded(p)
        if reason:
            audit.append(Decision(p.id, "eligibility", "excluded", reason))
            continue
        audit.append(Decision(p.id, "eligibility", "eligible", "No narrow exclusion triggered"))
        eligible.append(p)

    # 3) Scoring + demotion (soft)
    scored: List[Tuple[Post, float]] = []
    for p in eligible:
        base = public_interest_score(p, now)
        mult, factors = demotion_multiplier(p)
        final = base * mult

        audit.append(Decision(
            p.id, "scoring", "scored",
            "Computed public-interest score with transparent multipliers",
            details={
                "base": f"{base:.3f}",
                "mult": f"{mult:.3f}",
                "final": f"{final:.3f}",
                "factors": str(factors) if factors else "{}"
            }
        ))

        scored.append((p, final))

    # 4) Ranking (simple) + one constraint: max 2 per author
    scored.sort(key=lambda t: t[1], reverse=True)

    feed: List[Post] = []
    per_author: Dict[str, int] = {}
    for p, s in scored:
        if per_author.get(p.author, 0) >= 2:
            audit.append(Decision(p.id, "constraints", "skipped", "Author cap (max 2)"))
            continue
        per_author[p.author] = per_author.get(p.author, 0) + 1
        audit.append(Decision(p.id, "ranking", "selected", f"Ranked with score {s:.3f}"))
        feed.append(p)

    return feed, audit

# ----------------------------
# Demo data
# ----------------------------

def export_audit_to_json(audit, path: str):
    print(">>> EXPORT FUNCTION CALLED <<<")
    print(">>> Writing to:", path)

    out = []
    for d in audit:
        out.append({
            "post_id": d.post_id,
            "stage": d.stage,
            "action": d.action,
            "reason": d.reason,
            "details": d.details,
        })

    Path(path).write_text(
        json.dumps(out, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

if __name__ == "__main__":
    import os
    print("CWD =", os.getcwd())

    now = time.time()

    sample = [
        Post("A1", "nick", now-3600, "FOI refusal letter attached", evidence_level=3, first_hand=True, topic="foi"),
        Post("A2", "hse",  now-7200, "Official response: no records exist", institutional_record=True, topic="foi"),
        Post("A3", "anon1", now-18000, "Local case report with screenshots", evidence_level=2, low_visibility_author=True, first_hand=True),
        Post("A4", "anon2", now-4000, "Claim with no docs yet", evidence_level=0, low_visibility_author=True, predicted_harm=0.2),
        Post("A5", "spammy", now-1000, "Buy followers now!!!", spam_flag=True),
        Post("A6", "journo", now-9000, "Analysis thread linking cases", evidence_level=1, topic="analysis"),
        Post("A7", "anon3", now-2000, "High-conflict allegation, thin evidence", evidence_level=0, predicted_harm=0.8, low_visibility_author=True),
        Post("A8", "gov", now-15000, "Regulator acknowledgement", institutional_record=True),
        Post("A9", "nick", now-5000, "Timeline of submissions and non-responses", evidence_level=2, first_hand=True),
        Post("A10", "random", now-300, "General commentary", evidence_level=0),
    ]

    feed, audit = run_pipeline(sample)

    # Write JSON to an absolute path (no ambiguity)
    out_path = "/Users/nick/Documents/Dropbox/My Life/2026/audit_log.json"
    export_audit_to_json(audit, out_path)
    print("WROTE AUDIT JSON:", out_path)

    print("\n=== FEED (ordered) ===")
    for i, p in enumerate(feed, 1):
        print(f"{i:02d}. {p.id} | {p.author} | evid={p.evidence_level} | record={p.institutional_record} | first={p.first_hand} | text={p.text[:40]}")

    print("\n=== AUDIT (first 20) ===")
    for d in audit[:20]:
        print(f"{d.stage:12} | {d.post_id:3} | {d.action:18} | {d.reason} | {d.details}")