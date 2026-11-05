"""Independent re-derivation of every number on LX2 project.html (round 10, slice c).

Uses only fractions and an independent rounding path (Decimal with ROUND_HALF_UP on the exact Fraction value).
Run: python -I -W error rederive_c_r10.py
"""

import random
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from fractions import Fraction


def r4(x: Fraction, mode=ROUND_HALF_UP) -> str:
    d = (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal("0.0001"), rounding=mode)
    return str(d)


def fc(t: int) -> int:
    return 100 + 2 * t


# ---- Lab 1: months 13..20 (illustrative values written in the file)
L1 = (125, 131, 128, 132, 138, 133, 140, 135)
e1 = {t: fc(t) - y for t, y in zip(range(13, 21), L1)}
print("L1 errors", [e1[t] for t in range(13, 21)], "sum", sum(e1.values()))
h1 = [t for t in e1 if abs(e1[t]) <= 2]
print("L1 hits", len(h1), "rate", r4(Fraction(len(h1), 8)), "bias", r4(Fraction(sum(e1.values()), 8)))
print("L1 edge", [t for t in e1 if abs(e1[t]) == 2])
print("L1 strict hits", sum(1 for t in e1 if abs(e1[t]) < 2), "rate", r4(Fraction(sum(1 for t in e1 if abs(e1[t]) < 2), 8)))
print("L1 hit rate 1/8 step", r4(Fraction(1, 8)))
print("L1 forecast at 13,14:", fc(13), fc(14), "errors", e1[13], e1[14])
print("L1 M2 agreement with L3 month 18:")

# ---- Lab 2: months 13..18
L2 = (127, 126, 124, 131, 136, 141)
e2 = {t: fc(t) - y for t, y in zip(range(13, 19), L2)}
print("L2 errors", [e2[t] for t in range(13, 19)])
h2 = [t for t in e2 if abs(e2[t]) <= 2]
print("L2 hits", len(h2), "rate", r4(Fraction(len(h2), 6)), "bias", r4(Fraction(sum(e2.values()), 6)), "exact", Fraction(sum(e2.values()), 6))
print("L2 edge", [t for t in e2 if abs(e2[t]) == 2])
print("L2 hit count over 8:", r4(Fraction(len(h2), 8)), " mean abs error:", r4(Fraction(sum(abs(v) for v in e2.values()), 6)))
print("L2 agreement with L3 at month 13 only:", [t for t in range(13, 19) if False])

# ---- Lab 3: seed 20261103, months 1..36
rng = random.Random(20261103)
real = {}
noise = {}
for t in range(1, 37):
    noise[t] = rng.randint(-3, 3)
    real[t] = 100 + 2 * t + noise[t] + (-6 if t >= 28 else 0)
err = {t: fc(t) - real[t] for t in range(13, 37)}
print("L3 realised 13..36", [real[t] for t in range(13, 37)])
print("L3 errors 13..36", [err[t] for t in range(13, 37)])
hits = [t for t in err if abs(err[t]) <= 2]
print("L3 hits", len(hits), "rate", r4(Fraction(len(hits), 24)), "exact", Fraction(len(hits), 24))
print("L3 bias", r4(Fraction(sum(err.values()), 24)), "sum", sum(err.values()))
print("L3 edge", [t for t in err if abs(err[t]) == 2])
mx = max(abs(v) for v in err.values())
print("L3 max abs", mx, "months", [t for t in err if abs(err[t]) == mx])
cal = {t: fc(t) - real[t] for t in range(1, 13)}
print("L3 calibration sum", sum(cal.values()), "bias", r4(Fraction(sum(cal.values()), 12)))
print("integer sums k in [-60,60] that print 0.9167 over 12:", [k for k in range(-60, 61) if r4(Fraction(k, 12)) == "0.9167"])
print("sum 13..27", sum(err[t] for t in range(13, 28)), "hits 13..27", sum(1 for t in range(13, 28) if abs(err[t]) <= 2))
print("bias 13..27 over 15", r4(Fraction(sum(err[t] for t in range(13, 28)), 15)), "rate", r4(Fraction(13, 15)))
print("sum 28..36", sum(err[t] for t in range(28, 37)), "bias over 9", r4(Fraction(sum(err[t] for t in range(28, 37)), 9)), "hits", sum(1 for t in range(28, 37) if abs(err[t]) <= 2))
print("min/max 28..36 errors", min(err[t] for t in range(28, 37)), max(err[t] for t in range(28, 37)))
print("min/max 13..27 errors", min(err[t] for t in range(13, 28)), max(err[t] for t in range(13, 28)))
print("rolling 12 at 36 (25..36)", sum(err[t] for t in range(25, 37)), r4(Fraction(sum(err[t] for t in range(25, 37)), 12)))
print("strict-band L3 hits", sum(1 for t in err if abs(err[t]) < 2), "rate", r4(Fraction(sum(1 for t in err if abs(err[t]) < 2), 24)))
print("L3 13/24 half-even vs half-up:", r4(Fraction(13, 24)), r4(Fraction(13, 24), ROUND_HALF_EVEN))
print("ties at 4 places among printed values:")
vals = [Fraction(13, 24), Fraction(51, 24), Fraction(sum(err.values()), 24), Fraction(len(h2), 6), Fraction(sum(e2.values()), 6), Fraction(sum(calibration_list := [cal[t] for t in range(1, 13)]), 12), Fraction(13, 15), Fraction(-3, 15), Fraction(54, 9), Fraction(56, 12), Fraction(1, 8), Fraction(2, 8), Fraction(4, 8)]
for v in vals:
    s = v * 10**4
    frac = s - (s.numerator // s.denominator)
    print("  ", v, "frac part of 10^4 * v =", frac, "TIE" if frac == Fraction(1, 2) else "")
print("L1 bias exact", Fraction(sum(e1.values()), 8), "=0.2500?", r4(Fraction(sum(e1.values()), 8)))
print("Exemplar derived: 13/15=0.8667", r4(Fraction(13, 15)), "-3/15=-0.2000", r4(Fraction(-3, 15)), "54/9=6.0000", r4(Fraction(54, 9)), "56/12=4.6667", r4(Fraction(56, 12)))
print("Exemplar 0/9 =", r4(Fraction(0, 9)), "6 of 24 =", r4(Fraction(6, 24)))
print("Lab3 rate 13/24", r4(Fraction(13, 24)), "Lab3 bias 51/24", r4(Fraction(51, 24)))
