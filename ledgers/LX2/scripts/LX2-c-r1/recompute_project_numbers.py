"""Independent recomputation of every number stated on course/modules/LX/LX2/project.html (LX2 slice c, round 1).

Uses only the page text as the specification: forecast(t) = 100 + 2t, hit iff |e| <= 2, bias = sum(e)/H, hit rate = hits/H.
Uses exact Fraction arithmetic. The Lab 3 realised series is regenerated with random.Random(20261103).randint(-3, 3)
for t = 1..36, shifted by -6 from t = 28, independently of the lab file (no import of the lab code).
Run as: python3 -I -W error ledgers/LX2/scripts/LX2-c-r1/recompute_project_numbers.py
"""

import random
from fractions import Fraction


def f(t):
    return 100 + 2 * t


def hit(e):
    return abs(e) <= 2


def half_up(x, places):
    q = Fraction(10) ** places
    v = abs(x) * q + Fraction(1, 2)
    m = v.numerator // v.denominator
    s = "-" if x < 0 and m != 0 else ""
    return f"{s}{m // 10**places}.{m % 10**places:0{places}d}"


out = []

# Lab 1 (rung 1): months 13..20
r1 = [125, 131, 128, 132, 138, 133, 140, 135]
e1 = [f(13 + i) - y for i, y in enumerate(r1)]
h1 = [hit(e) for e in e1]
out.append(("L1 errors", e1))
out.append(("L1 hits", sum(h1), "of", len(r1), "rate", half_up(Fraction(sum(h1), len(r1)), 4)))
out.append(("L1 bias", half_up(Fraction(sum(e1), len(r1)), 4), "sum", sum(e1)))
out.append(("L1 edge months", [13 + i for i, e in enumerate(e1) if abs(e) == 2]))
strict_hits = sum(1 for e in e1 if abs(e) < 2)
out.append(("L1 strict-rule hits", strict_hits, half_up(Fraction(strict_hits, 8), 4)))

# Lab 2 (rung 2): months 13..18
r2 = [127, 126, 124, 131, 136, 141]
e2 = [f(13 + i) - y for i, y in enumerate(r2)]
h2 = [hit(e) for e in e2]
out.append(("L2 errors", e2))
out.append(("L2 hits", sum(h2), "of", len(r2), "rate", half_up(Fraction(sum(h2), len(r2)), 4)))
out.append(("L2 bias", half_up(Fraction(sum(e2), len(r2)), 4), "sum", sum(e2)))
out.append(("L2 edge months", [13 + i for i, e in enumerate(e2) if abs(e) == 2]))
out.append(("L2 hit-count-over-8 (claimed 0.5000)", half_up(Fraction(sum(h2), 8), 4)))
out.append(("L2 mean-abs-error bias (claimed 2.8333)", half_up(Fraction(sum(abs(e) for e in e2), len(e2)), 4)))

# Lab 3 (rung 3): seeded
rng = random.Random(20261103)
real = {}
for t in range(1, 37):
    noise = rng.randint(-3, 3)
    real[t] = 100 + 2 * t + noise - (6 if t >= 28 else 0)
err = {t: f(t) - real[t] for t in range(1, 37)}
val = list(range(13, 37))
hits = [t for t in val if hit(err[t])]
out.append(("L3 realised 1..36", [real[t] for t in range(1, 37)]))
out.append(("L3 validation errors 13..36", [err[t] for t in val]))
out.append(("L3 hits", len(hits), "of", len(val), "rate", half_up(Fraction(len(hits), 24), 4), "exact", Fraction(len(hits), 24)))
out.append(("L3 bias", half_up(Fraction(sum(err[t] for t in val), 24), 4), "sum", sum(err[t] for t in val)))
out.append(("L3 edge months", [t for t in val if abs(err[t]) == 2]))
mx = max(abs(err[t]) for t in val)
out.append(("L3 max abs error", mx, "months", [t for t in val if abs(err[t]) == mx]))
cal = [err[t] for t in range(1, 13)]
out.append(("L3 calibration errors 1..12", cal, "sum", sum(cal), "bias", half_up(Fraction(sum(cal), 12), 4)))
out.append(("L3 strict-rule hits", sum(1 for t in val if abs(err[t]) < 2)))
out.append(("L3 month-13..27 errors sum", sum(err[t] for t in range(13, 28)), "hits", sum(1 for t in range(13, 28) if hit(err[t])), "rate", half_up(Fraction(sum(1 for t in range(13, 28) if hit(err[t])), 15), 4)))
out.append(("L3 month-28..36 errors sum", sum(err[t] for t in range(28, 37)), "hits", sum(1 for t in range(28, 37) if hit(err[t])), "bias", half_up(Fraction(sum(err[t] for t in range(28, 37)), 9), 4)))
out.append(("L3 post-28 errors min/max", min(err[t] for t in range(28, 37)), max(err[t] for t in range(28, 37))))
out.append(("L3 errors 25..36 sum (rolling bias at month 36)", sum(err[t] for t in range(25, 37)), half_up(Fraction(sum(err[t] for t in range(25, 37)), 12), 4)))
out.append(("L3 rolling-12 bias check", half_up(Fraction(sum(err[t] for t in range(25, 37)), 12), 4)))

for line in out:
    print(*line)
