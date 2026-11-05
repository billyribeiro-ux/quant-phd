"""Recompute the L07 exact tails (discrete tail identity) and the Phi/erfc values (standard library only).

Usage: python -I l07_check.py
"""
import math


def end_at_least(n: int, m: int) -> int:
    return sum(math.comb(n, (n + s) // 2) for s in range(-n, n + 1, 2) if s >= m)


for n in (4, 16, 64, 256, 1024):
    m = math.isqrt(n)
    tail = (end_at_least(n, m) + end_at_least(n, m + 1)) / 2**n
    print(f"N={n} m={m} P(M_N>=m)={tail:.6f} exact={end_at_least(n, m) + end_at_least(n, m + 1)}/2^{int(math.log2(n))}")
print("2(1-Phi(1)) =", f"{math.erfc(1 / math.sqrt(2)):.10f}")
print("1-Phi(1) =", f"{0.5 * math.erfc(1 / math.sqrt(2)):.10f}")
print("sqrt(2/pi) =", f"{math.sqrt(2 / math.pi):.6f}")
print("E[M_1] check sqrt(2/pi) vs 2*phi(0):", math.sqrt(2 / math.pi), 2 / math.sqrt(2 * math.pi))
print("E2 21778/2^16 =", f"{21778 / 2**16:.6f}", "count check", end_at_least(16, 4), end_at_least(16, 5))
