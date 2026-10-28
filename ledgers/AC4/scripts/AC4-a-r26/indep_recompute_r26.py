"""Round 26 independent recomputation for AC4-a (L01, L02 numbers). Standard library only."""
import math, random
from fractions import Fraction as Fr

# --- L01: regenerate the seeded history from the lab's generator description (own code)
rng = random.Random(20261027)
rows = []
for _ in range(12):
    h = rng.randint(400, 1200)
    n = rng.randint(-40000, 40000)
    rows.append((h, 1800000 + 4250 * h + n))
hi = max(range(12), key=lambda i: (rows[i][0], -i)); lo = min(range(12), key=lambda i: (rows[i][0], i))
v = Fr(rows[hi][1] - rows[lo][1], rows[hi][0] - rows[lo][0]); F = rows[hi][1] - v * rows[hi][0]
res = [c - (F + v * h) for h, c in rows]
print("F_cents", float(F), "v_cents_per_hour", float(v), "v_USD", round(float(v) / 100, 4), "F_USD", round(float(F) / 100, 2))
print("max abs residual (cents)", max(abs(float(r)) for r in res), "nonzero", sum(1 for r in res if r != 0))
print("zero-residual months", [i + 1 for i, r in enumerate(res) if r == 0])
# Dollar figure for largest residual, month 1
print("month1 residual", float(res[0]), "hours", rows[0][0])
# noise identity: v-hat - 42.50 and F-hat - 18000 depend only on the two extreme months' noise
nH = rows[hi][1] - (1800000 + 4250 * rows[hi][0]); nL = rows[lo][1] - (1800000 + 4250 * rows[lo][0])
print("v identity check", v == 4250 + Fr(nH - nL, rows[hi][0] - rows[lo][0]))
print("F identity check", F == 1800000 + nH - rows[hi][0] * Fr(nH - nL, rows[hi][0] - rows[lo][0]))

# --- L01 R3: step supervisor, own brute force over 0..1200 whole hours
def step(h):
    return 0 if h == 0 else 4000 * math.ceil(h / 400)
errs = [(abs(step(h) - 10 * h), h) for h in range(0, 1201)]
mx = max(errs)[0]
print("R3 count points", len(errs), "max err", mx, "at", sorted(h for e, h in errs if e == mx), "pct of step", mx / 4000 * 100)
print("R3 line at 1,401,801 ->", [10 * h for h in (1, 401, 801)], "cost", [step(h) for h in (1, 401, 801)])

# --- L02: product
P, Vc, Fx, S = 2500, 1150, 120000, 2700000
m = P - Vc
def oi(q): return m * q - Fx - (S if q > 2000 else 0)
print("margin", m, "ratio", Fr(m, P), "BE single", Fr(Fx, m), float(Fr(Fx, m)), "ceil", math.ceil(Fr(Fx, m)))
print("OI88", oi(88) / 100, "OI89", oi(89) / 100, "OI2000", oi(2000) / 100, "OI2001", oi(2001) / 100, "OI2088", oi(2088) / 100, "OI2089", oi(2089) / 100)
neg = [q for q in range(0, 5001) if oi(q) < 0]
runs = []
for q in neg:
    if runs and runs[-1][1] == q - 1: runs[-1][1] = q
    else: runs.append([q, q])
print("loss runs", runs)
print("upper BE", float(Fr(Fx + S, m)), "lower BE", float(Fr(Fx, m)), "wrong formula", float(Fr(Fx + S, m)))
print("revenue BE USD", float(P * Fr(Fx, m)) / 100, "plan OI", oi(2500) / 100)
ms = 2500 - Fr(Fx + S, m)
print("MoS units", float(ms), "share %", float(ms / 2500 * 100), "DOL", float(Fr(m * 2500, oi(2500))), "1pct change %", (oi(2525) - oi(2500)) / oi(2500) * 100)
print("fixed +10000 moves BE by", float(Fr(10000, m)), "100.00 USD ->", float(Fr(10000, m)))
print("R2 deriv per cent", -120000 / 1350 ** 2, "per USD", -120000 / 1350 ** 2 * 100, "exact change 1 USD", 120000 / 1450 - 120000 / 1350)
print("M1 BE", 45000 / 30, "rev", 45000 / (30 / 80))
print("M2", 10000 / 7, math.ceil(10000 / 7), 7 * 1429 - 10000, 7 * 1428 - 10000)
print("E2 margin from first BE", 2500 - Fr(Fx, m) if False else float(2500 - Fr(Fx, m)))
print("R3 BE below 1000 margin 10:", 60000 / 10, "above:", 60000 / 20)
print("L02 Ex2.4", 60000 / 20, 60000 / (20 / 50), 50 * 3000, 60000 + 30 * 3000)
print("L01 Ex4.1", (30000 - 18000) / (1000 - 400), 30000 - 20 * 1000)
