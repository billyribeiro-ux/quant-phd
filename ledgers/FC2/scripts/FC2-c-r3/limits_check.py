"""Verifier check (FC2 slice c, round 3): Lemma 2.2 limits on L08 at the Lab 1 strikes, using double precision.

Run: .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r3/limits_check.py
"""

import math

from scipy.special import ndtr


def bs(S: float, K: float, r: float, t: float, s: float) -> float:
    root = s * math.sqrt(t)
    d1 = (math.log(S / K) + (r + s * s / 2) * t) / root
    d2 = d1 - root
    return float(S * ndtr(d1) - K * math.exp(-r * t) * ndtr(d2))


for K in (80.0, 100.0, 120.0, 100.0 * math.exp(0.05)):
    L = max(100.0 - K * math.exp(-0.05), 0.0)
    print(f"K={K!r} C(1e3)={bs(100.0, K, 0.05, 1.0, 1e3)!r} S=100.0 C(1e-6)={bs(100.0, K, 0.05, 1.0, 1e-6)!r} L={L!r}")
