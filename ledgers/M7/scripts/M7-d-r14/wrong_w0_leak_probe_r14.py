"""Probe for the failure-message rule: a wrong allocator that returns the starting portfolio with zero multipliers.

Used by the round-14 verifier to read the suite's failure text (never the expected answer). Not a solution.
"""

from typing import Any


def allocate(instance: dict[str, Any]) -> dict[str, Any]:
    w = [float(v) for v in instance["w0"]]
    n = len(w)
    zeros = [0.0] * n
    return {
        "weights": w,
        "multipliers": {"budget": 0.0, "lower": zeros, "upper": zeros, "sector": [0.0] * len(instance["sector_caps"]),
                        "turnover_plus": zeros, "turnover_minus": zeros, "turnover_total": 0.0},
        "certificate": {"primal_residual": 0.0, "stationarity_residual": 0.0, "dual_residual": 0.0,
                        "complementary_slackness": 0.0},
    }
