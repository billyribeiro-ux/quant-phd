"""Independent recomputation of every number in CS2 L09 (Lab 1 output, interpretation, misconception 2, E2, E1, R1 example).

Run: python3 -I -W error ledgers/CS2/scripts/CS2-c-r4/l09_numbers_r4.py
"""
import math
import random
from fractions import Fraction

N = 2000
SEED = 90


def draws() -> list[float]:
    rng = random.Random(SEED)
    return [rng.random() for _ in range(N)]


def stream(offset: float) -> list[float]:
    # offset + u, computed as float addition exactly as the twin does
    return [offset + u for u in draws()]


def exact_var(xs: list[float]) -> Fraction:
    vals = [Fraction(x) for x in xs]
    n = len(vals)
    m = sum(vals, Fraction(0)) / n
    return sum(((v - m) ** 2 for v in vals), Fraction(0)) / (n - 1)


def welford(xs: list[float]) -> float:
    c, m, s = 0, 0.0, 0.0
    for x in xs:
        c += 1
        d = x - m
        m += d / c
        s += d * (x - m)
    return s / (c - 1)


def two_pass(xs: list[float]) -> float:
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def naive(xs: list[float]) -> float:
    t = 0.0
    tq = 0.0
    for x in xs:
        t += x
        tq += x * x
    n = len(xs)
    return (tq - t * t / n) / (n - 1)


def rel(est: float, ex: Fraction) -> float:
    return float(abs(Fraction(est) - ex) / ex)


for off in (0.0, 1e6, 1e9):
    xs = stream(off)
    ex = exact_var(xs)
    w, tp, nv = welford(xs), two_pass(xs), naive(xs)
    print(f"offset {off!r}: exact {float(ex)!r} ({float(ex):.13f})")
    print(f"  welford {w!r} rel {rel(w, ex)!r}")
    print(f"  twopass {tp!r} rel {rel(tp, ex)!r}")
    print(f"  naive   {nv!r} rel {rel(nv, ex)!r}")
    if off == 1e9:
        sum_sq_exact = sum((Fraction(x) ** 2 for x in xs), Fraction(0))
        tq = 0.0
        t = 0.0
        for x in xs:
            t += x
            tq += x * x
        print(f"  exact sum of squares {float(sum_sq_exact)!r} ({float(sum_sq_exact):.6e})")
        print(f"  computed running sum of squares {tq!r}; difference from exact {float(Fraction(tq) - sum_sq_exact)!r} ({float(Fraction(tq) - sum_sq_exact):.4e})")
        print(f"  (n-1)*exact var = {float((N - 1) * ex):.6f}")
        print(f"  math.ulp(2e21) = {math.ulp(2e21)!r}; math.ulp(sum_sq) = {math.ulp(float(sum_sq_exact))!r}")
        print(f"  computed running sum of x (t) = {t!r}; exact sum = {float(sum((Fraction(x) for x in xs), Fraction(0)))!r}")

# Misconception 2 factors, unrounded
xs0, xs6, xs9 = stream(0.0), stream(1e6), stream(1e9)
for name, xs in (("0", xs0), ("1e6", xs6), ("1e9", xs9)):
    ex = exact_var(xs)
    w = welford(xs)
    nv = naive(xs)
    rw, rn = rel(w, ex), rel(nv, ex)
    print(f"factor naive/welford at {name}: {rn / rw:.6g}  (rw={rw:.6e}, rn={rn:.6e})")

# E2: absolute error of Welford at offset 0 (unrounded)
ex0 = exact_var(xs0)
w0 = welford(xs0)
abs_err = abs(Fraction(w0) - ex0)
print(f"E2 absolute error at offset 0: {float(abs_err)!r} ({float(abs_err):.6e})")
print(f"E2 exact variance unrounded float {float(ex0)!r}; rel err unrounded {rel(w0, ex0)!r}")
print(f"E2 product rel*exact = {rel(w0, ex0) * float(ex0):.6e}")

# Small-sample checks from the page
print("M1 mean/S8:", sum([2, 4, 4, 4, 5, 5, 7, 9]) / 8, sum((x - 5) ** 2 for x in [2, 4, 4, 4, 5, 5, 7, 9]), 32 / 7, 32 / 8)
print("R3 check:", 4 * 0.6**2 + 6 * 0.4**2, (4 * 0.6**2 + 6 * 0.4**2) / 10)
print("R1 example:", Fraction(1) + Fraction(3, 4) * 1, Fraction(3) * Fraction(1, 4))
print("P3 check ab/(a+b): ", "n/a (algebra)")
