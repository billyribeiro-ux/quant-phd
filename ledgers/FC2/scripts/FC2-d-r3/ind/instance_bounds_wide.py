"""Search seeds 0..19999 for generated quotes outside the strict Theorem 2.2 bounds, and the parity residual on
non-planted strikes (the docstring promises at most half a cent)."""
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1] + "/course/modules/FC/FC2/grader")
from instance import make_instance  # noqa: E402

PPM = 1_000_000
strict = []
worst_resid = Fraction(0)
worst_seed = None
for seed in range(20000):
    inst = make_instance(seed)
    spot, df = inst["spot_cents"], inst["df_ppm"]
    K, C, P = inst["strikes_cents"], inst["call_cents"], inst["put_cents"]
    planted = inst["planted_index"] if inst["planted_kind"] == "parity" else -1
    for k in range(6):
        disc = Fraction(K[k] * df, PPM)
        if C[k] < max(spot - disc, Fraction(0)) or C[k] > spot or P[k] < 0 or P[k] > disc or P[k] < max(disc - spot, Fraction(0)):
            strict.append((seed, k, float(C[k] - (spot - disc)), float(P[k] - disc)))
        if k != planted:
            r = abs(Fraction(C[k]) - Fraction(P[k]) - (Fraction(spot) - disc))
            if r > worst_resid:
                worst_resid, worst_seed = r, seed
print("seeds searched: 20000")
print("strict bound violations:", len(strict))
for row in strict[:10]:
    print("  seed %d idx %d C-(S-Kdf)=%.6f P-Kdf=%.6f" % row)
print("worst parity residual on non-planted strikes:", float(worst_resid), "at seed", worst_seed)
