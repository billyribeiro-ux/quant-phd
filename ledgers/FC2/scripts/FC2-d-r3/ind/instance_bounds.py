"""Independent check of the generator's claims (instance.py docstring lines 1-21) over seeds 0..999.

Prints: planted-kind counts; strict (no tolerance) Theorem 2.2 bound violations of generated quotes; parity residual
maximum (strictly below 1/2 required); convexity violations on clean draws; half-cent exact values present.
"""
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1] + "/course/modules/FC/FC2/grader")
from instance import _second_difference, make_instance  # noqa: E402

PPM = 1_000_000
N = 1000
kinds: dict[str, int] = {}
strict_viol = []
max_resid = Fraction(0)
clean_convex_viol = 0
half_cent_seen = 0
for seed in range(N):
    inst = make_instance(seed)
    kinds[inst["planted_kind"]] = kinds.get(inst["planted_kind"], 0) + 1
    spot, df = inst["spot_cents"], inst["df_ppm"]
    K, C, P = inst["strikes_cents"], inst["call_cents"], inst["put_cents"]
    for k in range(6):
        disc = Fraction(K[k] * df, PPM)
        gap = Fraction(C[k]) - Fraction(P[k]) - (Fraction(spot) - disc)
        max_resid = max(max_resid, abs(gap))
        if gap.denominator != 1 and (2 * gap).denominator == 1:
            half_cent_seen += 1
        bad = []
        if C[k] > spot:
            bad.append("C<=S")
        if C[k] < max(spot - disc, Fraction(0)):
            bad.append("C>=max(S-Kdf,0)")
        if P[k] < 0:
            bad.append("P>=0")
        if P[k] > disc:
            bad.append("P<=Kdf")
        if P[k] < max(disc - spot, Fraction(0)):
            bad.append("P>=max(Kdf-S,0)")
        if bad:
            strict_viol.append((seed, k, bad, float(C[k] - max(spot - disc, 0)), float(P[k] - disc)))
    if inst["planted_kind"] != "convexity":
        for j in range(1, 5):
            if _second_difference(K, C, j) < 0:
                clean_convex_viol += 1
print("planted kinds over 0..999:", dict(sorted(kinds.items())))
print("max |parity gap| over all quotes (must be < 1/2 for every strike):", float(max_resid))
print("half-cent exact gaps present (must be 0 by the rejection rule):", half_cent_seen)
print("clean-draw convexity violations (must be 0):", clean_convex_viol)
print("strict bound violations (quotes outside Theorem 2.2 with no tolerance):", len(strict_viol))
for row in strict_viol[:12]:
    print("  seed %d strike index %d %s  margin C-lower=%.6f P-upper=%.6f" % (row[0], row[1], row[2], row[3], row[4]))
