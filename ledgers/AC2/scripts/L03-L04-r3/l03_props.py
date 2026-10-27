"""Round-3 verifier: exact-fraction checks of L03 Propositions 2.2, 3.2, 3.4 and the witness.

Usage: .venv/bin/python -I ledgers/AC2/scripts/L03-L04-r3/l03_props.py
"""

from __future__ import annotations

import random
from fractions import Fraction as F

rng = random.Random(20261027)


def rnd() -> F:
    return F(rng.randint(-400, 400), rng.randint(1, 60))


def pos() -> F:
    return F(rng.randint(1, 400), rng.randint(1, 60))


# Proposition 2.2: ROIC(t2) = (1-t2)/(1-t1) ROIC(t1) for the same firm-year, average IC not depending on tau.
bad22 = 0
for _ in range(20000):
    oi = rnd()
    avg = pos()
    t1 = F(rng.randint(0, 99), 100)
    t2 = F(rng.randint(0, 99), 100)
    r1 = oi * (1 - t1) / avg
    r2 = oi * (1 - t2) / avg
    if r1 != 0 and r2 / r1 != (1 - t2) / (1 - t1):
        bad22 += 1
    if r2 != (1 - t2) * oi / avg:
        bad22 += 1
print("Prop 2.2 exact failures (20000 draws):", bad22)

# Proposition 3.2: average of IC = average E + average D - average C (exact, any signs).
bad32 = 0
for _ in range(20000):
    e0, e1, d0, d1, c0, c1 = rnd(), rnd(), rnd(), rnd(), rnd(), rnd()
    ic0 = e0 + d0 - c0
    ic1 = e1 + d1 - c1
    if (ic0 + ic1) / 2 != (e0 + e1) / 2 + (d0 + d1) / 2 - (c0 + c1) / 2:
        bad32 += 1
print("Prop 3.2 exact failures (20000 draws, signs free):", bad32)

# Proposition 3.4 as stated: IC_{t-1} > 0, IC_t > 0, NOPAT > 0.
# First sentence: IC_t > IC_{t-1} implies avg-based ROIC > year-end ROIC.
# Second sentence: IC_t < IC_{t-1} implies the inequality reverses (avg-based < year-end).
fail_first = fail_second = 0
n_first = n_second = 0
for _ in range(20000):
    ic_prev = pos()
    ic_t = pos()
    nopat = pos()
    avg = (ic_prev + ic_t) / 2
    r_avg = nopat / avg
    r_end = nopat / ic_t
    if ic_t > ic_prev:
        n_first += 1
        if not r_avg > r_end:
            fail_first += 1
    elif ic_t < ic_prev:
        n_second += 1
        if not r_avg < r_end:
            fail_second += 1
print(f"Prop 3.4 first sentence: {n_first} draws, failures {fail_first}")
print(f"Prop 3.4 second sentence (reversal): {n_second} draws, failures {fail_second}")

# Witness from the page: IC_{t-1} = 10, IC_t = -5, NOPAT = 1.
ic_prev, ic_t, nopat = F(10), F(-5), F(1)
avg = (ic_prev + ic_t) / 2
print("witness avg", avg, "ROIC avg", nopat / avg, "ROIC year-end", nopat / ic_t,
      "reversal holds (avg < end)?", nopat / avg < nopat / ic_t)

# Page's worked solution: 900 -> 1000, NOPAT 100.
print("P2 example:", F(100) / F(950), F(100) / F(1000), float(F(100) / F(950)), float(F(100) / F(1000)))

# Remark 2.3 algebra: 1 - NI/OI = 1 - (1 - I/OI)(1 - tau) when NI = (OI - I)(1 - tau).
bad23 = 0
for _ in range(20000):
    oi = pos()
    i = rnd()
    tau = F(rng.randint(0, 99), 100)
    ni = (oi - i) * (1 - tau)
    if 1 - ni / oi != 1 - (1 - i / oi) * (1 - tau):
        bad23 += 1
print("Remark 2.3 algebra failures:", bad23)
