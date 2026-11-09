"""Search exact half-cent convexity ties where plain float arithmetic gives the wrong gross (verifier round 17)."""
import math
from fractions import Fraction as F

def exact_violation(ks, cs, j):
    lo, mi, hi = ks[j-1], ks[j], ks[j+1]
    return F(hi - mi, hi - lo) * cs[j-1] + F(mi - lo, hi - lo) * cs[j+1] - cs[j]

def float_violation(ks, cs, j):
    lo, mi, hi = ks[j-1], ks[j], ks[j+1]
    return ((hi - mi) / (hi - lo)) * cs[j-1] + ((mi - lo) / (hi - lo)) * cs[j+1] - cs[j]

hits = []
for k0 in range(1, 6):
    for d1 in range(1, 8):
        for d2 in range(1, 8):
            ks = [k0, k0 + d1, k0 + d1 + d2]
            for c0 in range(0, 12):
                for c2 in range(0, 12):
                    for c1 in range(0, 40):
                        ex = exact_violation(ks, [c0, c1, c2], 1)
                        if ex != F(-1, 2) and ex != F(1, 2) and ex.denominator != 1:
                            continue
                        if ex.denominator == 1:
                            continue
                        # exact half-cent tie: -ex is an odd multiple of 1/2
                        if (2 * ex).denominator != 1 or (2 * ex).numerator % 2 == 0:
                            continue
                        fl = float_violation(ks, [c0, c1, c2], 1)
                        # gross must be half-up of -ex; plain float gross:
                        want = math.floor(-ex + F(1, 2))
                        got = int((-fl + 0.5) // 1)
                        if got != want:
                            hits.append((ks, [c0, c1, c2], str(ex), repr(fl), want, got))
print("tie cases where plain float gross != exact gross:", len(hits))
for h in hits[:10]:
    print(h)
ok_ties = 0
