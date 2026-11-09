"""Round 17: checks the Lab 1 interpretation sentence 'the width reaches 2^-53 at the 53rd halving and stays there,
because the two ends are adjacent floating-point numbers'. Runs Lab 1's bisection (noise 0.60, cost 0.13) and prints
the bracket width after halvings 52 to 60, and whether the two ends are adjacent floats at each step."""
import math

A, TV, TE, SD, C = 2.0, 1.0, 1.0, 0.60, 0.13


def ty(lam):
    return lam * lam * TE * TE / (lam * lam * TE + A * A * SD * SD)


def gap(lam):
    t = ty(lam)
    bs = (lam * TE + (1 - lam) * t) / (lam * (TV + TE) + (1 - lam) * (TV + t))
    r = t / (TV + t) - bs
    fu = (1 + r * r * (TV + t) * (1 / TV + 1 / t)) ** -0.5
    p = TV + TE
    sl = TE / p - bs
    bu = -A * bs / (lam * TE)
    vg = sl * sl * (1 / TV + 1 / TE) + bu * bu * SD * SD
    fi = (1 + p * vg) ** -0.5
    return fu - math.exp(A * C) * fi


lo, hi = 0.0, 1.0
for step in range(1, 61):
    mid = 0.5 * (lo + hi)
    if gap(mid) > 0:
        lo = mid
    else:
        hi = mid
    if step >= 52:
        print(f"halving {step}: width {hi - lo!r} adjacent {math.nextafter(lo, 2.0) == hi}")
print("2^-53 =", repr(2.0 ** -53))
