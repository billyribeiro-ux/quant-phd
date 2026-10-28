"""Independent recomputation of CS2 L09-L11 numbers (verifier round 1, slice c)."""
import random
from fractions import Fraction
import math

# ---- L09: Welford, two-pass, naive at three offsets; recompute with own code
def stream(off, n=2000, seed=90):
    r = random.Random(seed)
    return [off + r.random() for _ in range(n)]

def exact_var(xs):
    v = [Fraction(x) for x in xs]
    n = len(v)
    m = sum(v, Fraction(0)) / n
    return sum(((x - m) ** 2 for x in v), Fraction(0)) / (n - 1)

def welford(xs):
    M = xs[0]; S = 0.0
    for n, x in enumerate(xs[1:], start=2):
        d = x - M
        M_new = M + d / n
        S = S + d * (x - M_new)
        M = M_new
    return S / (len(xs) - 1)

def twopass(xs):
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)

def naive(xs):
    s = 0.0; sq = 0.0
    for x in xs:
        s += x; sq += x * x
    n = len(xs)
    return (sq - s * s / n) / (n - 1)

for off in (0.0, 1e6, 1e9):
    xs = stream(off)
    ex = exact_var(xs)
    print("L09 offset", off, "exact", float(ex))
    for name, f in (("welford", welford), ("twopass", twopass), ("naive", naive)):
        est = f(xs)
        rel = abs(Fraction(est) - ex) / ex
        print("   ", name, "est", repr(est), "rel", float(rel), "%.3e" % float(rel))
    if off == 1e9:
        xs9 = xs
        # running sums at the end of the naive loop
        s = 0.0; sq = 0.0
        for x in xs9:
            s += x; sq += x * x
        print("   naive running sumsq", sq, "sum", s, "s*s/n", s * s / len(xs9), "diff", sq - s * s / len(xs9))
        print("   ulp of sumsq", math.ulp(sq), "2^18", 2**18)
        print("   true S_n approx", float(ex) * 1999)
        print("   naive exact-zero check (estimate == 0.0):", naive(xs9) == 0.0)
        print("   welford est", welford(xs9), "two-pass", twopass(xs9))
print("L09 exact unrounded", repr(float(exact_var(stream(0.0)))), "rel welford off0",
      float(abs(Fraction(welford(stream(0.0))) - exact_var(stream(0.0))) / exact_var(stream(0.0))))
ex0 = exact_var(stream(0.0))
print("E2 abs err welford off0", float(abs(Fraction(welford(stream(0.0))) - ex0)))
print("E2 product", float(ex0) * 9.25811790803366e-16)
print("E2 unrounded relerr literal product", 0.08728110122738864 * 9.25811790803366e-16)
# worked problems
print("M3 zero-one stream check", )
