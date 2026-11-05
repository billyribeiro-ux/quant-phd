"""Recompute L08 exact walk quantities and the Brownian values (standard library only).

Usage: python -I l08_check.py
"""
import math
from fractions import Fraction


def end_at_least(n: int, m: int) -> int:
    return sum(math.comb(n, (n + s) // 2) for s in range(-n, n + 1, 2) if s >= m)


def max_at_least(n: int, m: int) -> int:
    return end_at_least(n, m) + end_at_least(n, m + 1)


def truncated_mean(n_steps: int) -> Fraction:
    total = Fraction(0)
    for k in range(n_steps):
        total += 1 - Fraction(max_at_least(k, 1), 2**k)
    return total


print("E[min(nu_1,16)] exact =", truncated_mean(16), "=", float(truncated_mean(16)))
print("179587/32768 =", 179587 / 32768, "equal:", truncated_mean(16) == Fraction(179587, 32768))
print("E[min(nu_1,64)] =", f"{float(truncated_mean(64)):.6f}")
print("E[min(nu_1,256)] =", f"{float(truncated_mean(256)):.6f}")
print("erfc(1/sqrt2)=", f"{math.erfc(1 / math.sqrt(2)):.10f}", "erfc(0.5)=", f"{math.erfc(0.5):.10f}")
f = lambda a, h: a / (math.sqrt(2 * math.pi) * h * math.sqrt(h)) * math.exp(-a * a / (2 * h))
print("f_1(1)=", f"{f(1, 1):.6f}", "f_1(2)=", f"{f(1, 2):.6f}")
print("sum_k odd hit counts", [512, 384, 288, 224, 180], sum([512, 384, 288, 224, 180]))
