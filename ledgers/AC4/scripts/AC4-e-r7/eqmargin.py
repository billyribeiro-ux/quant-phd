"""Witness for the equal-margin comment: with equal budgeted margins m, exact R-V = AT*m (an integer),
so whole-cent roundings of R and V differ by AT*m, and the whole-cent flexed profit equals the exact one."""
import random
from fractions import Fraction
def rnd(x):  # nearest cent, halves up, x >= 0
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)
random.seed(1)
checked = 0
bad = 0
for _ in range(20000):
    s = random.randint(0, 500)
    q1, q2 = random.randint(0, 9), random.randint(0, 9)
    b1, b2 = random.randint(1, 300), random.randint(1, 300)
    bp1 = random.randint(0, 5000)
    m = bp1 - q1 * s
    bp2 = m + q2 * s  # equal budgeted margin for product 2
    if bp2 < 0:
        continue
    BT = b1 + b2
    AT = random.randint(0, 3000)
    R = Fraction(AT * (b1 * bp1 + b2 * bp2), BT)
    V = Fraction(AT * (b1 * q1 * s + b2 * q2 * s), BT)
    checked += 1
    if R - V != AT * m:
        bad += 1
    if rnd(R) - rnd(V) != AT * m:
        bad += 1
print("checked", checked, "violations", bad)
