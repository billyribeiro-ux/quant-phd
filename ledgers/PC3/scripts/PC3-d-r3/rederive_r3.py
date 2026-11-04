"""Independent recomputation of the numbers quoted on the cards and lessons in PC3 slice d (round 3).

usage: python -I rederive_r3.py
"""
import math
from fractions import Fraction as F
from itertools import product

H = 6


def stop_exp(outcomes, rule):  # type: ignore[no-untyped-def]
    def value(h):  # type: ignore[no-untyped-def]
        if len(h) == H or rule(h):
            return F(sum(h))
        return sum((p * value(h + (x,)) for x, p in outcomes), F(0))

    return value(())


RULES = [
    ("play all", lambda h: False),
    ("first win", lambda h: bool(h) and h[-1] > 0),
    ("first loss", lambda h: bool(h) and h[-1] < 0),
    ("total 100", lambda h: sum(h) >= 100),
    ("gain or loss 200", lambda h: sum(h) >= 200 or sum(h) <= -200),
]
BIASED = ((150, F(1, 2)), (-100, F(1, 2)))
FAIR = ((100, F(1, 2)), (-100, F(1, 2)))
print("L03 biased:", [(n, str(stop_exp(BIASED, r))) for n, r in RULES])
print("L03 fair:", [(n, str(stop_exp(FAIR, r))) for n, r in RULES])
cont = F(sum(100 * g for g in range(1, 7)), 6) - 100
print("L03 reroll continuation", cont, "value", sum(max(F(100 * f), cont) for f in range(1, 7)) / 6)
print("L03 best of 64 policies", max(sum((F(100 * f) if b[f - 1] else cont) for f in range(1, 7)) / 6 for b in product((0, 1), repeat=6)))

print("L01 product bounds", 20 * 2 * 300, 60 * 10 * 390, "ratio", F(234000, 12000))
print("L01 log widths", math.log(19.5), math.log(3) + math.log(5) + math.log(1.3))
print("L01 remainder/bound", 0.0046221254 / 0.0048728552, "miss share", 0.1289 / 1.6289)
print("L01 R3 numbers", math.log(1.5), math.log(2.5 / 1.01))
print("L01 geometric mean", math.sqrt(12000 * 234000))

A = F(3310, 1331)
print("L06 annuity 10%", A, float(A))
print("L06 break-even 10%", F(150000, 50) / A, float(F(150000, 50) / A))
print("L06 NPV at 200, 1200, 1300, 1600 (cents):", [float(-15000000 + u * 5000 * A * 3 / 3) for u in (200, 1200, 1300, 1600)])
print("L06 NPV exact at 200", -15000000 + 200 * 5000 * A, "at 1200", float(-15000000 + 1200 * 5000 * A))
print("L06 margin for break-even 1600 (cents)", float(F(15000000) / (1600 * A)), float(F(15000000) / (1600 * A) / 5000))


def ann(r: float) -> float:
    return sum(1 / (1 + r) ** t for t in (1, 2, 3))


b8, b10, b12 = 3000 / ann(0.08), 3000 / ann(0.10), 3000 / ann(0.12)
print("L06 break-evens", round(b8, 4), round(b10, 4), round(b12, 4))
print("L06 per-point average", (b12 - b8) / 4, "width", b12 - b8)
print("L06 M2 NPV", -100 + F(600, 11) + F(6000, 121), float(-100 + F(600, 11) + F(6000, 121)))
print("L06 M3 break-even", F(1000 * 1331, 4 * 3310), float(F(1000 * 1331, 4 * 3310)))
