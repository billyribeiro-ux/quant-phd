"""Check Theorem 2.3 closed sum against backward induction, and Lemma 2.2 iff, on a grid (run with -I)."""
import itertools
import math


def tree(S, K, r, t, s, n):
    h = t / n
    u = math.exp(s * math.sqrt(h))
    d = 1 / u
    R = math.exp(r * h)
    q = (R - d) / (u - d)
    v = [max(S * u**j * d ** (n - j) - K, 0.0) for j in range(n + 1)]
    for _ in range(n):
        v = [(q * v[j + 1] + (1 - q) * v[j]) / R for j in range(len(v) - 1)]
    return v[0], q, u, d, R


def closed(S, K, r, t, s, n):
    V, q, u, d, R = tree(S, K, r, t, s, n)
    tot = sum(
        math.comb(n, k) * q**k * (1 - q) ** (n - k) * max(S * u**k * d ** (n - k) - K, 0) for k in range(n + 1)
    )
    return math.exp(-r * t) * tot, V


worst = 0.0
for n, (S, K, r, t, s) in itertools.product(
    (1, 2, 5, 20, 100), [(100, 100, 0.05, 1, 0.2), (100, 120, 0.03, 2, 0.3), (50, 40, 0.1, 0.5, 0.25)]
):
    c, V = closed(S, K, r, t, s, n)
    worst = max(worst, abs(c - V))
print("Theorem 2.3 max |closed - backward| =", worst)

bad = 0
for r, s, h in itertools.product((0.01, 0.05, 0.3, 1.0), (0.05, 0.2, 0.5, 2.0), (1e-4, 0.01, 0.04, 0.25, 1.0, 4.0)):
    d = math.exp(-s * math.sqrt(h))
    R = math.exp(r * h)
    u = math.exp(s * math.sqrt(h))
    lhs = 0 < d < R < u
    rhs = h < s * s / (r * r)
    if lhs != rhs:
        bad += 1
        print("Lemma 2.2 mismatch", r, s, h, lhs, rhs)
print("Lemma 2.2 grid mismatches (r>0, sigma>0):", bad)
