"""Round-2 re-derivation of every L09 number (lab 1 stream, worked examples, misconception ratios)."""

import math
import random
from fractions import Fraction

N, SEED = 2000, 90


def stream(offset):
    rng = random.Random(SEED)
    return [offset + rng.random() for _ in range(N)]


def welford(xs):
    count, mean, m2 = 0, 0.0, 0.0
    for x in xs:
        count += 1
        d = x - mean
        mean += d / count
        m2 += d * (x - mean)
    return m2 / (count - 1)


def two_pass(xs):
    mean = sum(xs) / len(xs)
    return sum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def naive(xs):
    t = 0.0
    tq = 0.0
    for x in xs:
        t += x
        tq += x * x
    n = len(xs)
    return (tq - t * t / n) / (n - 1)


def exact(xs):
    v = [Fraction(x) for x in xs]
    n = len(v)
    m = sum(v, Fraction(0)) / n
    return sum(((x - m) ** 2 for x in v), Fraction(0)) / (n - 1)


def rel(est, ex):
    return float(abs(Fraction(est) - ex) / ex)


res = {}
for off in (0.0, 1e6, 1e9):
    xs = stream(off)
    ex = exact(xs)
    e = {"welford": welford(xs), "two_pass": two_pass(xs), "naive": naive(xs)}
    res[off] = (xs, ex, e)
    print(f"offset {off!r}: exact unrounded {float(ex):.17g}; exact*1 6dp {float(ex):.6f}")
    for k, v in e.items():
        print(f"   {k:9s} est {v:.10e} rel {rel(v, ex):.6e}")

# Unrounded checks used on the page
xs0, ex0, e0 = res[0.0]
print("E2 unrounded exact variance (offset 0):", repr(float(ex0)))
print("E2 unrounded Welford rel error (offset 0):", repr(rel(e0["welford"], ex0)))
print("E2 absolute error product:", float(ex0) * rel(e0["welford"], ex0))
print("E2 product from printed 9.26e-16 and 0.087281:", 9.26e-16 * 0.087281)

xs9, ex9, e9 = res[1e9]
# Running sum of squares, naive, at offset 1e9 (unrounded)
tq = 0.0
t = 0.0
for x in xs9:
    t += x
    tq += x * x
print("sum of squares (float running) at 1e9:", repr(tq), "  sum x:", repr(t))
exact_sumsq = sum(Fraction(x) ** 2 for x in xs9)
print("exact sum of squares at 1e9 (Fraction):", float(exact_sumsq), " as 10-digit:", f"{float(exact_sumsq):.10e}")
print("exact S_n = (n-1)*s^2 at 1e9:", float(ex9 * (N - 1)), " 1999*0.08728110093 =", 1999 * 0.08728110093)
print("(n-1)*exact var at offset 0:", float(res[0.0][1] * (N - 1)))
print("math.ulp(2e21) =", math.ulp(2e21), " 2**18 =", 2**18)
print("ulp check: 2e21 in [2^70, 2^71):", 2**70 <= 2e21 < 2**71)
print("S_n exact at offset 1e9 (true sum sq dev):", float(sum((Fraction(x) - sum(Fraction(y) for y in xs9) / N) ** 2 for x in xs9)))

# Ratios for misconception 2 (unrounded and printed)
for off in (0.0, 1e6, 1e9):
    _, ex, e = res[off]
    rw = rel(e["welford"], ex)
    rn = rel(e["naive"], ex)
    print(f"ratio naive/welford at {off!r}: unrounded {rn/rw:.4f}  from printed values")
print("printed ratios: 7.286e-15/9.258e-16 =", 7.286e-15 / 9.258e-16, " 1.418e-2/8.852e-11 =", 1.418e-2 / 8.852e-11, " 1/7.449e-8 =", 1 / 7.449e-8)

# Misconception 3 example and M-problems
print("S_3 for 1,2,3:", sum((x - 2) ** 2 for x in (1, 2, 3)))
