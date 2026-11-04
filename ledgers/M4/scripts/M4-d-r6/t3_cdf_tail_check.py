"""Round-6 verifier (slice d): numeric check of the t(3) distribution function (card M4-c147) and tail (card M4-c149).

Integrates the t(3) density 2/(pi sqrt 3) (1 + t^2/3)^-2 numerically and compares with the closed forms on the cards.
Run: .venv/bin/python ledgers/M4/scripts/M4-d-r6/t3_cdf_tail_check.py
"""
import math


def dens(x):
    return 2 / (math.pi * math.sqrt(3)) * (1 + x * x / 3) ** -2


def cdf_closed(x):
    return 0.5 + (1 / math.pi) * (math.atan(x / math.sqrt(3)) + (x / math.sqrt(3)) / (1 + x * x / 3))


def cdf_numeric(x, lo=-400.0, n=400000):
    h = (x - lo) / n
    return sum(dens(lo + (i + 0.5) * h) for i in range(n)) * h


def tail_closed(x):
    return (2 / math.pi) * (math.atan(math.sqrt(3) / x) - x * math.sqrt(3) / (3 + x * x))


for x in (-2.0, 0.5, 1.7):
    print(f"F_V({x}) closed {cdf_closed(x):.8f} numeric {cdf_numeric(x):.6f}")
for x in (1.0, 10.0):
    print(f"P(|V|>{x}) closed {tail_closed(x):.8f} from closed cdf {1 - cdf_closed(x) + cdf_closed(-x):.8f}")
