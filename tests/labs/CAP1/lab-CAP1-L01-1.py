"""Lab 1: Peer review specification scanner and identification flaw classifier."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PaperAudit:
    title: str
    has_reverse_causality: bool
    has_lookahead_leakage: bool
    has_mechanical_identity: bool
    has_clustered_se: bool
    n_sample_splits: int


def classify_referee_recommendation(audit: PaperAudit) -> tuple[str, list[str]]:
    fatal_flaws: list[str] = []
    major_flaws: list[str] = []

    if audit.has_lookahead_leakage:
        fatal_flaws.append("FATAL: Signal formation uses future information (look-ahead bias).")
    if audit.has_mechanical_identity:
        fatal_flaws.append("FATAL: Result is driven by an accounting identity rather than economic behavior.")
    if audit.has_reverse_causality:
        major_flaws.append("MAJOR: Endogeneity via reverse causality unaddressed by instrument or design.")
    if not audit.has_clustered_se:
        major_flaws.append("MAJOR: Standard errors fail to account for cross-sectional or serial correlation.")
    if audit.n_sample_splits < 2:
        major_flaws.append("MINOR: Lacks sub-period temporal stability checks.")

    if fatal_flaws:
        decision = "REJECT (Unsalvageable Identification Flaws)"
    elif len(major_flaws) >= 2:
        decision = "REVISE & RESUBMIT (Substantive Econometric Overhaul Required)"
    elif major_flaws:
        decision = "MINOR REVISION (Address Clustered Inference & Robustness)"
    else:
        decision = "ACCEPT (Empirically Credible)"

    return decision, fatal_flaws + major_flaws


def main() -> None:
    papers = [
        PaperAudit("Paper A (Lookahead Momentum)", False, True, False, True, 3),
        PaperAudit("Paper B (Accounting Artifact)", False, False, True, True, 2),
        PaperAudit("Paper C (Unclustered Panel)", True, False, False, False, 1),
        PaperAudit("Paper D (Clean Factor Design)", False, False, False, True, 4),
    ]

    for p in papers:
        decision, comments = classify_referee_recommendation(p)
        print(f"Audit: {p.title}")
        print(f"Recommendation: {decision}")
        for c in comments:
            print(f"  - {c}")
        print()


main()
