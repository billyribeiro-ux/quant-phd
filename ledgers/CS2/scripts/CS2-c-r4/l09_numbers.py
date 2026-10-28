"""Independent recomputation of CS2 L09 Lab 1 numbers (verifier round 4). Run: python -I l09_numbers.py"""
import math
import random
from fractions import Fraction

N = 2000
SEED = 90


def stream(off):
    rng = random.Random(SEED)
    return [off + rng.random() for _ in range(N)]


def exact(xs):
    v = [Fraction(x) for x in xs]
    n = len(v)
    m = sum(v, Fraction(0)) / n
    return sum(((x - m) ** 2 for x in v), Fraction(0)) / (n - 1)


def welford(xs):
    c = 0
    m = 0.0
    s = 0.0
    for x in xs:
        c += 1
        d = x - m
        m += d / c
        s += d * (x - m)
    return s / (c - 1)


def twopass(xs):
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def naive(xs):
    t = 0.0
    q = 0.0
    for x in xs:
        t += x
        q += x * x
    n = len(xs)
    return (q - t * t / n) / (n - 1)


for off in (0.0, 1e6, 1e9):
    xs = stream(off)
    e = exact(xs)
    print("offset", off, "exact", repr(float(e)))
    for name, f in (("W", welford), ("2p", twopass), ("naive", naive)):
        est = f(xs)
        rel = float(abs(Fraction(est) - e) / e)
        print("  ", name, "%.6e" % est, "rel %.3e" % rel)
    if off == 1e9:
        q = sum(x * x for x in xs)
        print("  sum of squares ~ %.4e, ulp %s, S_n exact %.2f" % (q, math.ulp(q), float((N - 1) * e)))
        t = 0.0
        qq = 0.0
        for x in xs:
            t += x
            qq += x * x
        print("  computed sum-of-squares error %.4e" % float(Fraction(qq) - sum(Fraction(x) ** 2 for x in xs)))
    if off == 0.0:
        w = welford(xs)
        print("  E2 abs error", float(abs(Fraction(w) - e)), "exact*printed rel", float(e) * 9.26e-16)
