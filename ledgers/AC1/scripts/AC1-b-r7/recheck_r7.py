"""Independent recomputation of every number in the AC1-b slice (L04, L05, L06) and the card scan."""
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1])

# ---- L04: regenerate the seeded set with an independent generator and recompute the printed figures
TERM, QUARTERS = 4, 8
rng = random.Random(2604)
q = []
for _ in range(QUARTERS):
    cs = rng.randint(50_000_00, 120_000_00)
    cr = rng.randint(20_000_00, 60_000_00)
    pp = rng.randint(40_000_00, 90_000_00) if rng.random() < 1 / 3 else 0
    ox = rng.randint(30_000_00, 70_000_00)
    it = rng.randint(2_000_00, 5_000_00)
    q.append((cs, cr, pp, ox, it))
print("L04 prepaid purchases by quarter:", [(i, x[2]) for i, x in enumerate(q) if x[2]])
exp_b = [0] * QUARTERS
for s, (cs, cr, pp, ox, it) in enumerate(q):
    base = pp // TERM
    sh = [base] * 3 + [pp - 3 * base]
    for o, v in enumerate(sh):
        if s + o < QUARTERS:
            exp_b[s + o] += v
rev = [cs + cr for cs, cr, *_ in q]
ni_a = [r - ox - it - pp for r, (cs, cr, pp, ox, it) in zip(rev, q)]
ni_b = [r - ox - it - e for r, (cs, cr, pp, ox, it), e in zip(rev, q, exp_b)]
pb = []
c1 = c2 = 0
for (cs, cr, pp, ox, it), e in zip(q, exp_b):
    c1 += pp
    c2 += e
    pb.append(c1 - c2)
print("L04 prepaid_balance_b:", pb)
print("L04 ni_a - ni_b per quarter:", [a - b for a, b in zip(ni_a, ni_b)])
print("L04 ni_a < ni_b quarters:", [i for i, (a, b) in enumerate(zip(ni_a, ni_b)) if a < b],
      "ni_a > ni_b:", [i for i, (a, b) in enumerate(zip(ni_a, ni_b)) if a > b])
dbal = [0] + [pb[t] - pb[t - 1] for t in range(1, QUARTERS)]
print("L04 (ni_a-ni_b) == -(change in balance) every quarter:",
      all(a - b == -d for a, b, d in zip(ni_a, ni_b, dbal)))
print("L04 cum NI rule A", sum(ni_a), "rule B", sum(ni_b), "diff", sum(ni_a) - sum(ni_b), "P7", pb[-1])
print("L04 P_7 purchase first share", 6632381 // 4, "unexpired", 6632381 - 6632381 // 4)
print("L04 3319293/27832482 =", 3319293 / 27832482, " 3319293/24513189 =", 3319293 / 24513189)
print("L04 interest total", sum(x[4] for x in q))
print("L04 rule B expense q7 share check: 6632381 shares", [6632381 // 4] * 3)

# ---- L05
W = 80_495_111
print("L05 shares", [round(x / W, 4) for x in (5434051, 9440568, 29888194, 35732298)],
      "sum of printed shares", round(0.0675 + 0.1173 + 0.3713 + 0.4439, 4))
print("L05 alloc sum", 5434051 + 9440568 + 29888194 + 35732298, "== price", 5434051 + 9440568 + 29888194 + 35732298 == W)
print("L05 50471362/80495111 =", 50471362 / W)
print("L05 32792272/80495111 =", 32792272 / W, " 23333398/80495111 =", 23333398 / W)
f1, f4 = 5434051 // 12, 35732298 // 12
print("L05 floors", f1, f4, "remainders m12", 5434051 - 11 * f1, 35732298 - 11 * f4)
print("L05 six months", 6 * f1, 6 * f4, "sum", 6 * f1 + 6 * f4)
print("L05 m12 totals check", 11 * f1 + (5434051 - 11 * f1) == 5434051, 11 * f4 + (35732298 - 11 * f4) == 35732298)
print("L05 P3 M2: 6*2000 + 60000", 60000 + 6 * 2000)

# ---- L06
rng6 = random.Random(2606)
term = rng6.randint(4, 7)
pay = rng6.randint(120_000_00, 300_000_00)
rate_bps = rng6.randint(400, 800)
r = rate_bps / 10_000
pv = round(sum(pay / (1 + r) ** t for t in range(1, term + 1)))
print("L06 term", term, "pay", pay, "rate", rate_bps, "L0", pv)
L = pv
A0 = pv
amort = [A0 // term] * (term - 1) + [A0 - (A0 // term) * (term - 1)]
I_list, F_list, Y_list, Lo = [], [], [], []
for t in range(term):
    I = (L * rate_bps + 5000) // 10000
    Y = pay if t < term - 1 else L + I
    Lo.append(L)
    I_list.append(I)
    Y_list.append(Y)
    F_list.append(I + amort[t])
    L = L + I - Y
print("L06 interest", I_list)
print("L06 amort", amort)
print("L06 F", F_list)
print("L06 final payment", Y_list[-1], "adj", Y_list[-1] - pay)
tot = sum(Y_list)
S = [tot // term] * (term - 1) + [tot - (tot // term) * (term - 1)]
print("L06 S", S, "total payments", tot, "sum F", sum(F_list))
print("L06 F-S", [f - s for f, s in zip(F_list, S)])
print("L06 interest falls", [I_list[t] - I_list[t + 1] for t in range(term - 1)])
print("L06 F falls", [F_list[t] - F_list[t + 1] for t in range(term - 1)])
print("L06 min interest fall", min(I_list[t] - I_list[t + 1] for t in range(term - 1)))
print("L06 F share year1", 14820224 / 91239905, "1/7", 1 / 7)
print("L06 rate*L0", 0.063 * 71992763)
print("L06 M1 PV", 10000 / 1.1 + 10000 / 1.1 ** 2 + 10000 / 1.1 ** 3)
print("L06 year-1 asset - liability", (71992763 - 10284680) - 63494035)
print("L06 Remark: year-7 F minus S", F_list[-1] - S[-1])

# ---- rate 0 claim: patterns coincide
def pattern_check(p, n, rate):
    lz = n * p
    a0 = lz
    am = [a0 // n] * (n - 1) + [a0 - (a0 // n) * (n - 1)]
    ints = []
    l = lz
    for t in range(n):
        i = (l * rate + 5000) // 10000
        y = p if t < n - 1 else l + i
        ints.append(i)
        l = l + i - y
    f = [i + a for i, a in zip(ints, am)]
    tot_y = p * (n - 1) + (p if False else 0)
    return f, ints
print("L06 rate 0 F values", pattern_check(120000, 5, 0)[0])

# ---- card scan
cards = json.load(open(root / "course/modules/AC/AC1/cards.json"))
fronts = [c["front"].strip().lower() for c in cards]
print("cards", len(cards), "duplicate fronts", len(fronts) - len(set(fronts)))
