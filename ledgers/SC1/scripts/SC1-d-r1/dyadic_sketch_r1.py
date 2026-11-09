# Checks the L02 A2 sketch: for t in [0,1], t_k = ceil(2^k t)/2^k is dyadic, lies in [t,1], is non-increasing and tends to t.
# Error bound: t_k - t < 2^-k, so at index 39 the gap is below 2^-39.
from fractions import Fraction as F
import math

def seq(t: F, K: int) -> list[F]:
    return [F(math.ceil(t * 2**k), 2**k) for k in range(K)]

bad = []
samples = [F(p, q) for q in range(1, 61) for p in range(0, q + 1)]
samples += [F(1, 3), F(2, 7), F(1, 10**6), F(999999, 1000000)]
for t in samples:
    s = seq(t, 40)
    for k, x in enumerate(s):
        if not (t <= x <= 1):
            bad.append(("range", t, k))
        if x.denominator & (x.denominator - 1):
            bad.append(("dyadic", t, k))
        if k and s[k] > s[k - 1]:
            bad.append(("monotone", t, k))
    if not (0 <= s[-1] - t < F(1, 2**39)):
        bad.append(("limit", t))
print("checked", len(samples), "rationals with 40 terms each; violations:", len(bad), bad[:5])
print("t=1 sequence:", [str(x) for x in seq(F(1), 4)])
print("t=0 sequence:", [str(x) for x in seq(F(0), 4)])
print("t=1/3 sequence:", [str(x) for x in seq(F(1, 3), 6)])
