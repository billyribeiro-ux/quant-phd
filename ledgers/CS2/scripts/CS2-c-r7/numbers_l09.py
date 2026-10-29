"""Round 7 verifier: re-derive every number in L09 prose from first principles (stdlib only)."""
import math
import random
import sys
from fractions import Fraction

N = 2000
SEED = 90


def stream(offset):
    rng = random.Random(SEED)
    return [offset + rng.random() for _ in range(N)]


def welford(xs):
    count = 0
    mean = 0.0
    m2 = 0.0
    for x in xs:
        count += 1
        delta = x - mean
        mean += delta / count
        m2 += delta * (x - mean)
    return m2 / (count - 1)


def two_pass(xs):
    mean = sum(xs) / len(xs)
    return sum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def naive(xs):
    total = 0.0
    total_sq = 0.0
    for x in xs:
        total += x
        total_sq += x * x
    n = len(xs)
    return (total_sq - total * total / n) / (n - 1)


def exact(xs):
    vals = [Fraction(x) for x in xs]
    n = len(vals)
    mean = sum(vals, Fraction(0)) / n
    return sum(((x - mean) ** 2 for x in vals), Fraction(0)) / (n - 1)


def rel(est, ex):
    return abs(Fraction(est) - ex) / ex


res = {}
for off in (0.0, 1e6, 1e9):
    xs = stream(off)
    ex = exact(xs)
    print(f"offset {off!r}: exact unrounded float={float(ex)!r} exact Fraction>{float(ex):.12f}")
    print(f"   exact*(n-1) unrounded = {float(ex * (N - 1))!r}; exact S_n (Fraction) = {float(ex * (N - 1)):.6f}")
    for name, m in (("Welford", welford), ("two-pass", two_pass), ("naive", naive)):
        e = m(xs)
        r = float(rel(e, ex))
        print(f"   {name:9s} est={e!r} relerr_unrounded={r!r} printed_est={e:.6e} printed_rel={r:.3e}")
        res[(off, name)] = (e, r)
    if off == 1e9:
        tot = sum(x * x for x in xs)
        tot_float = 0.0
        s_naive = 0.0
        for x in xs:
            s_naive += x * x
        print(f"   sum x^2 float = {s_naive!r}; exact sum x^2 = {float(sum(Fraction(x)**2 for x in xs)):.10e}")
        print(f"   ulp(2e21) = {math.ulp(2e21)!r}; ulp(sum) = {math.ulp(s_naive)!r}")
        print(f"   sys.float_info.mant_dig = {sys.float_info.mant_dig}")
        print(f"   1999*0.08728110093 = {1999*0.08728110093!r}")

# Ratios naive/Welford from unrounded relative errors
for off in (0.0, 1e6, 1e9):
    rn = res[(off, "naive")][1]
    rw = res[(off, "Welford")][1]
    print(f"ratio naive/Welford at offset {off!r}: {rn / rw!r}")
print("abs err Welford offset 0 =", float(Fraction(res[(0.0, 'Welford')][0]) - exact(stream(0.0))))
print("abs err Welford offset0 via rel*exact:", res[(0.0, 'Welford')][1] * float(exact(stream(0.0))))
