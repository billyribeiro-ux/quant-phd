"""Theorem 2.3 sum vs backward induction, vega by finite difference, strict monotonicity grid, Lemma 2.2 limits (stdlib only)."""
import math
from math import comb


def Phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def C(S, K, r, tau, sig):
    root = sig * math.sqrt(tau)
    d1 = (math.log(S / K) + (r + sig * sig / 2) * tau) / root
    d2 = d1 - root
    return S * Phi(d1) - K * math.exp(-r * tau) * Phi(d2)


def tree_sum(n, S=100.0, K=100.0, r=0.05, sig=0.2, tau=1.0):
    h = tau / n
    u = math.exp(sig * math.sqrt(h))
    d = 1 / u
    R = math.exp(r * h)
    q = (R - d) / (u - d)
    s = sum(comb(n, k) * q**k * (1 - q) ** (n - k) * max(S * u**k * d ** (n - k) - K, 0.0) for k in range(n + 1))
    return math.exp(-r * tau) * s


def tree_bi(n, S=100.0, K=100.0, r=0.05, sig=0.2, tau=1.0):
    h = tau / n
    u = math.exp(sig * math.sqrt(h))
    d = 1 / u
    R = math.exp(r * h)
    q = (R - d) / (u - d)
    v = [max(S * u**j * d ** (n - j) - K, 0.0) for j in range(n + 1)]
    for _ in range(n):
        v = [(q * v[j + 1] + (1 - q) * v[j]) / R for j in range(len(v) - 1)]
    return v[0]


worst = 0.0
for n in (1, 2, 5, 10, 25, 50, 100, 200, 400):
    worst = max(worst, abs(tree_sum(n) - tree_bi(n)))
print("Theorem 2.3 sum vs backward induction, max abs diff over n in {1,...,400}:", worst)
print("Theorem 2.3 sum vs backward induction, n=400 (sum):", tree_sum(400), "closed:", C(100, 100, 0.05, 1, 0.2))

# vega by central finite difference vs S phi(d1) sqrt(tau)
def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

for sig in (0.05, 0.2, 0.4, 1.0):
    h = 1e-6
    fd = (C(100, 100, 0.05, 1, sig + h) - C(100, 100, 0.05, 1, sig - h)) / (2 * h)
    d1 = (math.log(1.0) + (0.05 + sig * sig / 2)) / sig
    print("vega sigma", sig, "fd", fd, "formula", 100 * phi(d1))

# strict monotonicity on a grid, and limits
grid = [10 ** (-6 + 7 * i / 4000) for i in range(4001)]
vals = [C(100, 100, 0.05, 1, s) for s in grid]
print("strictly increasing on 4001-point log grid of [1e-6, 1e7]:", all(b > a for a, b in zip(vals, vals[1:])))
print("C(1e-6)", C(100, 100, 0.05, 1, 1e-6), "C(1e7)", C(100, 100, 0.05, 1, 1e7))
print("K=120 C(1e-6)", C(100, 120, 0.05, 1, 1e-6), "C(1e7)", C(100, 120, 0.05, 1, 1e7))
