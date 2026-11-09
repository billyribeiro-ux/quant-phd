"""Recompute every L09 prose number from unrounded values (verifier script, CS2 slice c, round 1)."""
import math
import random
import sys
from fractions import Fraction

N = 2000
SEED = 90
OFFSETS = (0.0, 1e6, 1e9)


def stream(offset):
    rng = random.Random(SEED)
    return [offset + rng.random() for _ in range(N)]


def welford(xs):
    count, mean, ssd = 0, 0.0, 0.0
    for x in xs:
        count += 1
        delta = x - mean
        mean += delta / count
        ssd += delta * (x - mean)
    return ssd / (count - 1)


def two_pass(xs):
    mean = sum(xs) / len(xs)
    return sum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def naive(xs):
    t = 0.0
    tsq = 0.0
    for x in xs:
        t += x
        tsq += x * x
    n = len(xs)
    return (tsq - t * t / n) / (n - 1)


def exact(xs):
    v = [Fraction(x) for x in xs]
    n = len(v)
    m = sum(v, Fraction(0)) / n
    return sum(((x - m) ** 2 for x in v), Fraction(0)) / (n - 1)


def rel(est, ex):
    return abs(Fraction(est) - ex) / ex


res = {}
print("mant_dig", sys.float_info.mant_dig, "python", sys.version.split()[0])
for off in OFFSETS:
    xs = stream(off)
    ex = exact(xs)
    print(f"offset {off!r}: exact sample variance (unrounded float) {float(ex)!r}")
    print(f"   exact = {float(ex):.17g}; (n-1)*exact = {float((N - 1) * ex):.10f}; S_n exact = {float((N-1)*ex):.10f}")
    rw = rel(welford(xs), ex)
    r2 = rel(two_pass(xs), ex)
    rn = rel(naive(xs), ex)
    res[off] = (float(rw), float(r2), float(rn))
    print(f"   rel Welford {float(rw)!r}  two-pass {float(r2)!r}  naive {float(rn)!r}")
    print(f"   welford est {welford(xs)!r}  naive est {naive(xs)!r}  two-pass est {two_pass(xs)!r}")
    if off == 1e9:
        tsq = 0.0
        for x in xs:
            tsq += x * x
        print(f"   running sum of squares (float) = {tsq!r}  unrounded-ish {tsq:.10e}")
        print(f"   exact sum of squares of floats = {float(sum(Fraction(x)**2 for x in xs)):.10e}")
        print(f"   math.ulp(2e21) = {math.ulp(2e21)!r}")
        print(f"   math.ulp(tsq) = {math.ulp(tsq)!r}")
        ssd_exact = float((N - 1) * ex)
        print(f"   sum sq dev exact = {ssd_exact!r}")

print("ratios naive/Welford (from unrounded relative errors):")
for off, (rw, r2, rn) in res.items():
    print(f"   offset {off!r}: {rn / rw:.6g}")
print("E2: exact var * rel Welford at offset 0 =", float(exact(stream(0.0))) * res[0.0][0])
