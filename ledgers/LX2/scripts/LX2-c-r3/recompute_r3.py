# Independent recomputation for LX2 project.html round 3 (own Fraction code; does not import any lab twin).
# Run: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r3/recompute_r3.py
import random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP


def r4(x: Fraction) -> str:
    d = (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    return str(d)


def f(t: int) -> int:
    return 100 + 2 * t


# Lab 1 (page lines 135, 163-199): months 13..20
R1 = [125, 131, 128, 132, 138, 133, 140, 135]
e1 = [f(13 + i) - r for i, r in enumerate(R1)]
h1 = sum(1 for e in e1 if abs(e) <= 2)
print("L1 errors", e1, "hits", h1, "of", len(R1), "rate", r4(Fraction(h1, len(R1))),
      "bias", r4(Fraction(sum(e1), len(R1))), "sum", sum(e1))
print("L1 edge months", [13 + i for i, e in enumerate(e1) if abs(e) == 2])
print("L1 strict-band hits", sum(1 for e in e1 if abs(e) < 2), "rate", r4(Fraction(sum(1 for e in e1 if abs(e) < 2), 8)))

# Lab 2 (page lines 244, 294-304): months 13..18
R2 = [127, 126, 124, 131, 136, 141]
e2 = [f(13 + i) - r for i, r in enumerate(R2)]
h2 = sum(1 for e in e2 if abs(e) <= 2)
print("L2 errors", e2, "hits", h2, "of", len(R2), "rate", r4(Fraction(h2, 6)), "bias", r4(Fraction(sum(e2), 6)),
      "sum", sum(e2))
print("L2 edge", [13 + i for i, e in enumerate(e2) if abs(e) == 2])
print("L2 mean abs error", r4(Fraction(sum(abs(e) for e in e2), 6)), "hit count over 8", r4(Fraction(h2, 8)))
print("L2 strict hits", sum(1 for e in e2 if abs(e) < 2), "one-sided hits", sum(1 for e in e2 if e <= 2))

# Lab 1 vs Lab 2 vs Lab 3 realised agreement (page line 89)
rng = random.Random(20261103)
noise = {}
REAL3 = {}
for t in range(1, 37):
    n = rng.randint(-3, 3)
    noise[t] = n
    REAL3[t] = 100 + 2 * t + n + (-6 if t >= 28 else 0)
print("L3 realised 13..20", [REAL3[t] for t in range(13, 21)])
print("L3 realised 13..18", [REAL3[t] for t in range(13, 19)])
print("L1 agrees with L3 at months", [13 + i for i, r in enumerate(R1) if REAL3[13 + i] == r])
print("L2 agrees with L3 at months", [13 + i for i, r in enumerate(R2) if REAL3[13 + i] == r])

# Lab 3 (page lines 338-477)
err = {t: f(t) - REAL3[t] for t in range(1, 37)}
val = {t: err[t] for t in range(13, 37)}
H = len(val)
hits = [t for t in val if abs(val[t]) <= 2]
print("L3 validation H", H, "hits", len(hits), "rate", r4(Fraction(len(hits), H)))
print("L3 bias", r4(Fraction(sum(val.values()), H)), "sum", sum(val.values()))
print("L3 edge", [t for t in val if abs(val[t]) == 2])
mx = max(abs(val[t]) for t in val)
print("L3 max abs", mx, "months", [t for t in val if abs(val[t]) == mx])
cal = [err[t] for t in range(1, 13)]
print("L3 calibration sum", sum(cal), "bias", r4(Fraction(sum(cal), 12)))
s1 = [t for t in range(13, 28)]
s2 = [t for t in range(28, 37)]
print("13-27 n", len(s1), "sum", sum(err[t] for t in s1), "bias", r4(Fraction(sum(err[t] for t in s1), 15)),
      "hits", sum(1 for t in s1 if abs(err[t]) <= 2), "rate", r4(Fraction(sum(1 for t in s1 if abs(err[t]) <= 2), 15)))
print("28-36 n", len(s2), "sum", sum(err[t] for t in s2), "bias", r4(Fraction(sum(err[t] for t in s2), 9)),
      "hits", sum(1 for t in s2 if abs(err[t]) <= 2), "errs", [err[t] for t in s2])
print("13-27 errors", [err[t] for t in s1], "range", min(err[t] for t in s1), max(err[t] for t in s1))
print("strict band hits (validation)", sum(1 for t in val if abs(val[t]) < 2), "rate", r4(Fraction(sum(1 for t in val if abs(val[t]) < 2), 24)))
print("one-sided hits (validation)", sum(1 for t in val if val[t] <= 2))
roll36 = sum(err[t] for t in range(25, 37))
print("rolling 12m bias at 36 sum", roll36, "bias", r4(Fraction(roll36, 12)))
print("months 13..36 errors", [err[t] for t in range(13, 37)])
print("post-change min/max", min(err[t] for t in s2), max(err[t] for t in s2))
# Calibration window errors for the exemplar A line 536 check
print("calibration errors", cal)
