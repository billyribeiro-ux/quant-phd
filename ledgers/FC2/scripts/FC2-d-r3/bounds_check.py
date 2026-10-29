"""Round-3: check every generated chain (seeds 0-49) against the model-free bounds of L05 Theorem 2.2 (with 1/2-cent slack)."""
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "course/modules/FC/FC2/grader"))
import instance  # noqa: E402

PPM = 1_000_000
tot = {"none": [0, 0], "parity": [0, 0], "convexity": [0, 0]}
examples = []
for s in range(50):
    i = instance.make_instance(s)
    S, df = i["spot_cents"], i["df_ppm"]
    bad = []
    for K, C, P in zip(i["strikes_cents"], i["call_cents"], i["put_cents"]):
        DK = Fraction(K * df, PPM)
        if P < 0:
            bad.append(("P<0", K, P))
        if C < max(S - DK, 0) - Fraction(1, 2):
            bad.append(("C<lower", K, C))
        if P > DK + Fraction(1, 2):
            bad.append(("P>DK", K, P))
        if P < max(DK - S, 0) - Fraction(1, 2):
            bad.append(("P<lower", K, P))
    kind = i["planted_kind"]
    tot[kind][0] += 1
    if bad:
        tot[kind][1] += 1
        if kind == "none" and len(examples) < 6:
            examples.append((s, bad[:2]))
print("chains per planted kind [total, with a bound violation]:", tot)
print("examples of clean-chain bound violations (seed, [(rule, strike, quote)]):")
for e in examples:
    print("  ", e)
