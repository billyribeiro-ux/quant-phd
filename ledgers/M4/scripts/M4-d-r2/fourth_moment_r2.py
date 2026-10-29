"""Verifier round 2: the cross-moment E[r1^2 r2^2] under one shared chi-square W (the page's model) and under one W
per asset (mutant n02), relative to S11 S22 + 2 S12^2.

Usage: .venv/bin/python -I ledgers/M4/scripts/M4-d-r2/fourth_moment_r2.py
Predictions: shared W gives E[s] E[s] ... = E[s^2] = (nu-2)/(nu-4) (nu > 4); per-asset W gives E[s1] E[s2] = 1.
The Monte Carlo estimator has infinite variance for nu <= 8, so the sample values are indicative only.
"""

import math
import random

S11, S12, S22 = 0.0004, 0.00036, 0.0009
L11 = math.sqrt(S11)
L21 = S12 / L11
L22 = math.sqrt(S22 - L21 * L21)
base = S11 * S22 + 2 * S12 * S12
for nu in (5, 9):
    rng = random.Random(7)
    n = 300000
    shared = per_asset = 0.0
    for _ in range(n):
        z1, z2 = rng.gauss(0, 1), rng.gauss(0, 1)
        u1, u2 = L11 * z1, L21 * z1 + L22 * z2
        s = (nu - 2) / rng.gammavariate(nu / 2, 2.0)
        shared += (s * u1 * u1) * (s * u2 * u2)
        s1 = (nu - 2) / rng.gammavariate(nu / 2, 2.0)
        s2 = (nu - 2) / rng.gammavariate(nu / 2, 2.0)
        per_asset += (s1 * u1 * u1) * (s2 * u2 * u2)
    print(f"nu={nu}: shared W ratio {shared / n / base:.3f} (predicted {(nu - 2) / (nu - 4):.3f}); "
          f"per-asset W ratio {per_asset / n / base:.3f} (predicted 1)")
