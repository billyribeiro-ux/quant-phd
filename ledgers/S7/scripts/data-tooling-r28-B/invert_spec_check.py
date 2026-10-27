"""Round 28 re-check of the r16-invert-spec derivation: floor(log10(1/|x|)) is L0-1 or L0 with L0 = len(str(q)) - len(str(p)),
inv = q/p in lowest terms, and the code's lead after the one-step correction is the decade of inv (exact integer tests).
Usage: python -I invert_spec_check.py <checkout>"""
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "tools"))
import fetch_data as fd  # noqa: E402

rng = random.Random(20261030)
n = bad = 0
for _ in range(200_000):
    nd = rng.randint(1, 40)
    s = str(rng.randint(10 ** (nd - 1), 10**nd - 1)) if nd > 1 else str(rng.randint(1, 9))
    pt = rng.randint(0, len(s))
    v = s[:pt] + "." + s[pt:] if 0 < pt < len(s) else (s + ".0" if pt == len(s) else "0." + s)
    x = Fraction(v)
    if x == 0:
        continue
    inv = 1 / abs(x)
    p, q = inv.denominator, inv.numerator  # inv = q / p ... careful: 1/|x| = q/p with p = numerator of |x|
    p, q = abs(x).numerator, abs(x).denominator
    L0 = len(str(q)) - len(str(p))
    e = 0
    while inv >= Fraction(10) ** (e + 1):
        e += 1
    while inv < Fraction(10) ** e:
        e -= 1
    n += 1
    if e not in (L0 - 1, L0):
        bad += 1
    lead = L0
    if inv < Fraction(10) ** lead:
        lead -= 1
    if lead != e:
        bad += 1
print(f"spec: {n} inputs; floor(log10 inv) outside {{L0-1, L0}} or code lead != decade: {bad}")
