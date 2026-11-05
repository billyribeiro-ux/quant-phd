"""Re-derive every number that a PC3 card states, from first principles (exact fractions where possible)."""
import math
from fractions import Fraction as F
from itertools import product

out = []


def line(label, value):
    out.append(f"{label}: {value}")


# L01 (cards c007, c009, c013, c014, c016, c129-c133, c156)
line("c007 product bounds", (20 * 2 * 300, 60 * 10 * 390))
ln195 = math.log(19.5)
line("c156 ln 19.5 to ten places", f"{ln195:.10f}")
line("c129 factor widths ln3 ln5 ln1.3 sum", f"{math.log(3):.10f} {math.log(5):.10f} {math.log(1.3):.10f} sum={math.log(3)+math.log(5)+math.log(1.3):.10f}")
base = ln195
red_q = math.log(10 / 2) - math.log(10 / 2)  # placeholder to keep structure explicit
totalq = math.log(19.5) - math.log(19.5)
narrow_sym = math.log(60 / 20) - math.log(40 / 20)  # reduction from narrowing symbols [20,60]->[20,40]
narrow_q = math.log(10 / 2) - math.log(8 / 4)  # quote updates [2,10]->[4,8]
narrow_m = math.log(390 / 300) - math.log(360 / 330)  # minutes [300,390]->[330,360]
line("c009 reductions (symbols, quotes, minutes)", f"{narrow_sym:.10f} {narrow_q:.10f} {narrow_m:.10f}")
line("c009 share of baseline quotes percent", f"{100*narrow_q/base:.4f}")
line("c009 share of baseline minutes percent", f"{100*narrow_m/base:.4f}")
line("c009 baseline", f"{base:.10f}")
line("c016 ln1.5", f"{math.log(1.5):.4f}")
line("c016 ln(2.5/1.01)", f"{math.log(2.5/1.01):.4f}")
line("c016 ln2.5 ln3", f"{math.log(2.5):.4f} {math.log(3):.4f}")
rem = F(1, 1) * 0
x = F(1, 100)
n = 10
exact = (1 + x) ** n
rem = exact - 1 - n * x
bound = F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x
line("c130 remainder n=10 x=1/100", f"{float(rem):.10f}")
line("c131 bound n=10 x=1/100", f"{float(bound):.10f}")
line("c013 (1.01)^10 exact prefix", f"{float(exact):.12f} exact={exact} ~ {float(exact):.10f}")
x20 = F(1, 20)
line("c014 (1.05)^10 to 4 places, miss vs 1.5", f"{float((1+x20)**10):.6f} miss={float((1+x20)**10 - (1+10*x20)):.6f}")
line("c133 bound n=10 x=1/20", f"{float(F(10*9,2)*(1+x20)**8*x20*x20):.10f}")
line("c132 rem<bound n=10 x=1/100", float(rem) < float(bound))

# L02 (c023-c035)
coins = list(product("HT", repeat=2))
ev_any = [c for c in coins if "H" in c]
p_any = F(len(ev_any), 4)
p_both = F(1, 4)
line("c023 P(at least one head), P(both)", f"{p_any} {p_both} cond={p_both/p_any}")
ev_first = [c for c in coins if c[0] == "H"]
line("c023 P(first heads), cond both|first", f"{F(len(ev_first),4)} {p_both/F(len(ev_first),4)}")
line("c025 P(at least one | both)", F(1, 4) / F(1, 4))
balls = ["r1", "r2", "r3", "b1", "b2"]
pairs = [(a, b) for a in balls for b in balls if a != b]
red = {"r1", "r2", "r3"}
line("c026-c028 counts", (len(pairs), sum(a in red for a, _ in pairs), sum(b in red for _, b in pairs), sum(a in red and b in red for a, b in pairs)))
line("c029 P(second red | first blue)", F(sum(b in red for a, b in pairs if a.startswith("b")), sum(1 for a, _ in pairs if a.startswith("b"))))
# Monty Hall rule A and rule B by enumeration
def monty(rule):
    stay = sw = tot = F(0)
    for car, pick in product(range(3), range(3)):
        others = [d for d in range(3) if d != pick]
        for opened in others:
            if rule == "A":
                goats = [d for d in others if d != car]
                if opened not in goats:
                    continue
                po = F(1, len(goats))
            else:
                if opened == car:
                    continue
                po = F(1, 2)
            w = F(1, 9) * po
            tot += w
            sd = [d for d in others if d != opened][0]
            stay += w if pick == car else 0
            sw += w if sd == car else 0
    return stay / tot, sw / tot
line("c030 Monty rule A stay, switch", monty("A"))
line("c031 Monty rule B stay, switch", monty("B"))
line("c033 bag: P(red)=1/2*3/4+1/2*1/4, P(bag1|red)", (F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4), (F(1, 2) * F(3, 4)) / (F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4))))
pA, pBA, pBnA = F(3, 10), F(1, 2), F(1, 5)
pB = pBA * pA + pBnA * (1 - pA)
line("c035 P(B), P(A|B)", (pB, pBA * pA / pB))

# L03 (c045-c059, c135, c136)
def fair_stop_expectation(outcomes, rule, horizon=6):
    def value(hist):
        if len(hist) == horizon or rule(hist):
            return F(sum(hist))
        return sum((p * value(hist + (x,)) for x, p in outcomes), F(0))
    return value(())
RULES = [
    ("play all", lambda h: False),
    ("stop after first win", lambda h: bool(h) and h[-1] > 0),
    ("stop after first loss", lambda h: bool(h) and h[-1] < 0),
    ("stop total reaches 100", lambda h: sum(h) >= 100),
    ("stop at +-200", lambda h: sum(h) >= 200 or sum(h) <= -200),
]
FAIR = ((100, F(1, 2)), (-100, F(1, 2)))
BIAS = ((150, F(1, 2)), (-100, F(1, 2)))
for name, r in RULES:
    line(f"c052-c053/c135-c136 fair {name}", fair_stop_expectation(FAIR, r))
for name, r in RULES:
    line(f"c051/c052/c135/c136 biased {name}", fair_stop_expectation(BIAS, r))
reroll = F(sum(100 * g for g in range(1, 7)), 6) - 100
line("c045 continuation", reroll)
val = sum((max(F(100 * f), reroll) for f in range(1, 7)), F(0)) / 6
line("c046 reroll value", (val, float(val)))
line("c058 gain over stop-at-once", val - F(350))
line("c056 faces rerolling", [f for f in range(1, 7) if 100 * f < reroll])
# R1 two-turn look-ahead expectation
paths = [((100, 100)), ((100, -100)), ((-100, 100)), ((-100, -100))]
tot = []
for p in product((100, -100), repeat=2):
    w1 = p[0]
    w2 = p[0] + p[1]
    tot.append(max(w1, w2))
line("c055 look-ahead expectation", F(sum(tot), 4))
line("c040 face 7/2 and 350", (F(21, 6), 100 * F(21, 6)))

# L04 (c067, c069-c083)
line("c067 mid vs settlement P&L (mid 9990, settle 9980, cash -9950, inv 1)", (-9950 + 9990, -9950 + 9980))
line("c070 example 3.2 values", [5 - F(1, 2) * (max(v - 10010, 0) + max(9990 - v, 0)) for v in (10000, 10020, 9985)])
line("c082 d=(1-p)h/p at p=3/5 h=10", F(2, 5) * 10 / F(3, 5))
line("c083 variance 25 I^2 at |I|=1,2", [25 * i * i for i in (1, 2)])
line("c074 sd at 3 and 10 units", [5 * 3, 5 * 10])
line("c080 variance at 10 units", 25 * 100)
line("c079 P&L", 10010 - 10000)

# L06 (c110-c127, c147-c151, c179)
def annuity(r):
    return sum((1 / (1 + r) ** t for t in range(1, 4)), F(0)) if False else sum((F(1) / (1 + r) ** t for t in range(1, 4)), F(0))
r10 = F(1, 10)
A10 = annuity(r10)
line("c115 A(10%) exact", A10)
for rate in (F(8, 100), F(10, 100), F(12, 100)):
    A = annuity(rate)
    be = F(15000000, 5000) / A
    line(f"c116/c121/c148 break-even at {rate}", (float(be), f"{float(be):.4f}"))
line("c147 u* 10% exact", F(15000000, 5000) / A10)
line("c126 M3 u*", F(100000, 400) / A10)
line("c125 M2 NPV", F(-100) + F(60) / F(11, 10) + F(60) / F(121, 100))
def npv(u, r):
    return -15000000 + sum(u * 5000 / (1 + r) ** t for t in range(1, 4))
line("c117 NPV at 200 units, 10% exact", npv(F(200), r10))
line("c117 displayed", round(float(npv(F(200), r10)), 6))
line("c150 NPV at 1600 units, 10% exact", npv(F(1600), r10))
line("c179 NPV at 1200 units exact and float", (npv(F(1200), r10), float(npv(F(1200), r10))))
line("c124 NPV at 1200, 8%", float(npv(F(1200), F(8, 100))))
line("c149 signs at 200 and 1600, 8/10/12%", [(float(npv(F(200), r)) < 0, float(npv(F(1600), r)) > 0) for r in (F(8, 100), F(10, 100), F(12, 100))])
m_star = F(15000000) / (F(1600) * A10)
line("c127 margin for break-even 1600 at 10%", (float(m_star), float(m_star / 5000), float(1 - m_star / 5000) * 100))
line("c114 units bounds", (2000 * 1 * F(1, 10), 4000 * 2 * F(1, 5)))
line("c151 E3 slope per point", (float(F(1249046900000, 10**10)) - 1164.1005) / 4)
line("c121 rounded breakevens 8/10/12", [round(float(F(15000000,5000)/annuity(r)),2) for r in (F(8,100),F(10,100),F(12,100))])

with open(__file__.replace(".py", ".out"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
print("\n".join(out))
