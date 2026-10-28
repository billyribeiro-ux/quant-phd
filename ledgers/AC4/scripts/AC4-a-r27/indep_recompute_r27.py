"""Round 27 independent recomputation for AC4-a (hub, L01, L02), written from the page text, not from the lab code.

Generator reproduced with numpy-free stdlib random, seed 20261027, as the lab's stated generator.
Every number checked here is a number the pages state; the output is compared by the caller.
"""
from fractions import Fraction as Fr
import random
import sys

out = []


def check(name, got, want):
    ok = got == want
    out.append(f"{name}: {'OK' if ok else 'MISMATCH'} got={got} want={want}")


# ---- L01 section 4 worked split (Example 4.1)
vA, vB = 30000, 18000
v = Fr(vA - vB, 1000 - 400)
F = vA - v * 1000
check("Ex4.1 v-hat", v, 20)
check("Ex4.1 F-hat", F, 10000)
check("Ex4.1 check at B", F + v * 400, 18000)

# ---- L01 M2 (March 800h 52000; July 1400h 73000; fitted at 1100 h)
v2 = Fr(73000 - 52000, 1400 - 800)
F2 = 73000 - v2 * 1400
check("M2 v", v2, 35)
check("M2 F", F2, 24000)
check("M2 fitted at 1100", F2 + v2 * 1100, 62500)

# ---- L01 R3: step cost 4000 per 400 h or part; high-low on ends 0 h -> 0 USD and 1200 h -> 12000 USD
def step(h):
    return 0 if h == 0 else 4000 * (-(-h // 400))
vr = Fr(12000 - 0, 1200)
check("R3 v-hat", vr, 10)
errs = [(abs(step(h) - (10 * h)), h) for h in range(0, 1201)]
mx = max(e for e, _ in errs)
hs = sorted(h for e, h in errs if e == mx)
check("R3 max abs error", mx, 3990)
check("R3 argmax hours", hs, [1, 401, 801])
check("R3 share of step", Fr(mx, 4000), Fr(9975, 10000))
check("R3 step at 401 vs line", (step(401), 10 * 401), (8000, 4010))
check("R3 step at 801 vs line", (step(801), 10 * 801), (12000, 8010))

# ---- L01 lab: generator and high-low fit, recomputed from the seeded stream
rng = random.Random(20261027)
rows = []
for _ in range(12):
    h = rng.randint(400, 1200)
    n = rng.randint(-40000, 40000)
    rows.append((h, 1800000 + 4250 * h + n))
hi = max(range(12), key=lambda i: (rows[i][0], -i))
lo = min(range(12), key=lambda i: (rows[i][0], i))
Hh, Hc = rows[hi]
Lh, Lc = rows[lo]
vv = Fr(Hc - Lc, Hh - Lh)
FF = Hc - vv * Hh


def cents(x):
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


check("L01 fixed cents", cents(Fr(FF)), 1846389)
check("L01 variable USD/h 2dp", f"{float(vv):.2f}", "4198.96")
resid = [cents(Fr(c) - (FF + vv * h)) for h, c in rows]
check("L01 residuals", resid, [-51473, -34248, -10154, -31387, -50768, 0, 11065, -31690, -5127, 11016, 0, -2249])
check("L01 months nonzero", sum(1 for r in resid if r != 0), 10)
check("L01 largest abs residual", max(abs(r) for r in resid), 51473)
check("L01 extremes are months", (lo + 1, hi + 1), (6, 11))
check("L01 hours range min/max", (min(h for h, _ in rows), max(h for h, _ in rows)), (428, 1161))
check("L01 E1 month 6 cost USD", rows[5][1] / 100, 36435.46)
check("L01 E1 month 11 cost USD", rows[10][1] / 100, 67213.87)

# ---- L02 numbers (Lab 1 inputs as stated on the page: price 25.00, variable 11.50, fixed 1200, step 27000 above 2000)
m = Fr(2500 - 1150, 100)
check("L02 margin", m, Fr(27, 2))
Qs = Fr(1200) / m
check("L02 Q* rounded 2dp", f"{float(Qs):.2f}", "88.89")
check("L02 first whole unit (ceil)", -(-Qs.numerator // Qs.denominator), 89)


def oi(q):
    return m * q - 1200 - (27000 if q > 2000 else 0)


check("L02 OI(88)", float(oi(88)), -12.0)
check("L02 OI(89)", float(oi(89)), 1.5)
check("L02 OI(2000)", float(oi(2000)), 25800.0)
check("L02 OI(2001)", float(oi(2001)), -1186.5)
check("L02 upper zero", f"{float((1200 + 27000) / m):.2f}", "2088.89")
neg = [q for q in range(0, 5001) if oi(q) < 0]
runs = []
for q in neg:
    if runs and runs[-1][1] == q - 1:
        runs[-1][1] = q
    else:
        runs.append([q, q])
check("L02 loss runs", runs, [[0, 88], [2001, 2088]])
check("L02 revenue at BE USD", f"{float(25 * Qs):.2f}", "2222.22")
check("L02 OI at 2500", float(oi(2500)), 5550.0)
check("L02 safety units", f"{float(2500 - (1200 + 27000) / m):.2f}", "411.11")
check("L02 safety share %", f"{float((2500 - (1200 + 27000) / m) / 2500 * 100):.2f}", "16.44")
check("L02 DOL at 2500", f"{float(m * 2500 / oi(2500)):.2f}", "6.08")
check("L02 1pct change %", f"{float((oi(2525) - oi(2500)) / oi(2500) * 100):.2f}", "6.08")
check("L02 +100 USD fixed moves BE", f"{float(Fr(100) / Fr(27, 2)):.2f}", "7.41")
check("L02 E2 margin from first BE", f"{float(2500 - Qs):.2f}", "2411.11")
check("L02 R2 derivative per USD", f"{float(-Fr(120000) / Fr(1350) ** 2 * 100):.2f}", "-6.58")
check("L02 R2 exact change for +1 USD", f"{float(Fr(120000, 1450) - Fr(120000, 1350)):.2f}", "-6.13")
check("L02 M1 break-even", (Fr(45000, 30), Fr(45000) / Fr(30, 80)), (1500, 120000))
check("L02 M2 units", (Fr(10000, 7), -(-Fr(10000, 7).numerator // Fr(10000, 7).denominator)), (Fr(10000, 7), 1429))
check("L02 M2 OI at 1429 and 1428", (7 * 1429 - 10000, 7 * 1428 - 10000), (3, -4))
check("L02 R3 break-even above 1000", Fr(60000, 20), 3000)
check("L02 quiz q7 DOL", Fr(10000, 1) / Fr(27, 2), Fr(20000, 27))
check("L02 quiz q6 DOL", Fr(10 * 1000) / (10 * 1000 - 5000), 2)

bad = [l for l in out if "MISMATCH" in l]
print("\n".join(out))
print("MISMATCHES", len(bad))
sys.exit(1 if bad else 0)
