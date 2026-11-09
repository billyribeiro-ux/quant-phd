"""Independent re-derivation of the E1 project propositions, numbers and claims (round 5).

Exact Fractions everywhere. Brute-force grids check the closed forms against optimisation and equilibrium
definitions; the algebra in the propositions is checked on a parameter sweep.
"""

from fractions import Fraction as F
import math
import itertools

def half_up(x):
    return math.floor(x + F(1, 2))

def outputs(structure, a, b, c):
    d = F(a - b * c)
    if structure == "monopoly":
        Q, f = d / 2, F(a + b * c, 2 * b)
    elif structure == "cournot":
        Q, f = 2 * d / 3, F(a + 2 * b * c, 3 * b)
    else:
        Q, f = d, F(c)
    profit = (f - c) * Q
    cs = Q * Q / (2 * b)
    welfare = cs + profit
    dwl = (d - Q) ** 2 / (2 * b)
    return dict(Q=Q, f=f, profit=profit, cs=cs, welfare=welfare, dwl=dwl, d=d)

BRUTE = set()  # grid equilibrium checks moved to brute_r5.py (float, finer grid)
fails = []
checked = 0
# Parameter sweep: a > bc > 0, b in 1..3, c in 1..60, d in 1..400 (instance range) plus small/large.
cases = []
for b in range(1, 4):
    for c in range(1, 61, 1):
        for d in list(range(1, 60)) + list(range(60, 401, 7)):
            cases.append((b * c + d, b, c))
for a, b, c in cases:
    o = outputs("monopoly", a, b, c)
    checked += 1
    # Prop 1: monopoly profit pi(Q) = ((a-Q)/b - c) Q maximised at Q = d/2 (exact: pi(d/2 + t) = pi* - b t^2 ...)
    d = F(a - b * c)
    pi = lambda Q: ((a - Q) / F(b) - c) * Q
    if pi(o["Q"]) != o["d"] ** 2 / (4 * b):
        fails.append(("P1 max profit", a, b, c))
    for t in (F(1, 7), F(-1, 3), F(2, 5)):
        if not pi(d / 2 + t) < pi(d / 2):
            fails.append(("P1 strict max", a, b, c, t))
    # Prop 1 fee and profit identities
    if o["f"] != F(a + b * c, 2 * b) or o["profit"] != d * d / (4 * b):
        fails.append(("P1 fee/profit", a, b, c))
    # Prop 2: reaction and iteration error d/(3*2^k)
    q = F(0)
    for k in range(1, 9):
        q = (d - q) / 2
        if abs(q - d / 3) != d / (3 * 2 ** k) * (1 if k % 2 == 0 else 1):
            # error sign alternates; magnitude must equal d/(3 2^k)
            if abs(abs(q - d / 3) - d / (3 * 2 ** k)) != 0:
                fails.append(("P2 iteration magnitude", a, b, c, k))
    o2 = outputs("cournot", a, b, c)
    if o2["f"] != F(a + 2 * b * c, 3 * b) or o2["profit"] != 2 * d * d / (9 * b):
        fails.append(("P2 fee/profit", a, b, c))
    # Prop 2 uniqueness on a grid: best response of q_i to q_j and equilibrium only at d/3 (grid of step 1/6 on [0, d])
    step = F(1, 6)
    grid = [step * i for i in range(0, int(d * 6) + 1)] if (a, b, c) in BRUTE else None
    if grid is not None:
        cprofit = lambda qi, qj: ((F(a) - qi - qj) / b - c) * qi
        eq = []
        for qi in grid:
            for qj in grid:
                ok = True
                # best response over grid
                best_i = max(grid, key=lambda x: cprofit(x, qj))
                best_j = max(grid, key=lambda x: cprofit(x, qi))
                if cprofit(qi, qj) >= cprofit(best_i, qj) and cprofit(qj, qi) >= cprofit(best_j, qi):
                    eq.append((qi, qj))
        if eq != [(d / 3, d / 3)] and not (d / 3 in [x for x in grid] and set(eq) == {(d / 3, d / 3)}):
            # tolerate grid-discretisation only if the symmetric point is the unique grid equilibrium
            if set(eq) != {(d / 3, d / 3)}:
                fails.append(("P2 grid equilibria", a, b, c, eq[:3]))
    # Prop 3 Bertrand: on a fee grid, (c,c) is the only equilibrium
    fgrid = [] if (a, b, c) not in BRUTE else [F(c) + F(i, 4) for i in range(-4 * c, 4 * (a // b - c) + 1)] if a // b > c else []
    fgrid = [x for x in fgrid if 0 <= x <= F(a, b)]
    fgrid = sorted(set(fgrid + [F(c)]))
    def bprof(fi, fj):
        if fi < fj:
            dem = F(a) - b * fi
            return (fi - c) * dem
        if fi == fj:
            return (fi - c) * (F(a) - b * fi) / 2
        return F(0)
    beqs = []
    for f1, f2 in itertools.product(fgrid, repeat=2):
        p1, p2 = bprof(f1, f2), bprof(f2, f1)
        if all(bprof(g, f2) <= p1 for g in fgrid) and all(bprof(g, f1) <= p2 for g in fgrid):
            beqs.append((f1, f2))
    if (a, b, c) in BRUTE and beqs != [(F(c), F(c))]:
        fails.append(("P3 grid equilibria", a, b, c, beqs[:4]))
    # Prop 4: CS, DWL identities by independent numeric integration (Simpson, exact for cubics)
    def simpson(fn, lo, hi, n=8):
        h = (hi - lo) / n
        s = fn(lo) + fn(hi)
        for i in range(1, n):
            s += (4 if i % 2 else 2) * fn(lo + i * h)
        return s * h / 3
    Qm = o["Q"]
    cs_num = simpson(lambda t: (F(a) - t) / b - (F(a) - Qm) / b, F(0), Qm)
    if cs_num != o["cs"]:
        fails.append(("P4 CS numeric", a, b, c))
    W = lambda x: simpson(lambda t: (F(a) - t) / b, F(0), x) - c * x
    if W(d) - W(Qm) != o["dwl"]:
        fails.append(("P4 DWL numeric", a, b, c))
    if o["welfare"] != W(Qm):
        fails.append(("P4 welfare identity", a, b, c))
    # Prop 5 ordering of exact values (all cases)
    d_m, d_c = F(a - b * c), None
    V = [outputs(s, a, b, c) for s in ("monopoly", "cournot", "bertrand")]
    if not (V[0]["Q"] < V[1]["Q"] < V[2]["Q"]):
        fails.append(("P5 volume order", a, b, c))
    if not (V[0]["f"] > V[1]["f"] > V[2]["f"]):
        fails.append(("P5 fee order", a, b, c))
    if not (V[0]["dwl"] > V[1]["dwl"] > V[2]["dwl"]):
        fails.append(("P5 dwl order", a, b, c))
    if V[0]["profit"] - V[1]["profit"] != d * d / (36 * b):
        fails.append(("P5 profit diff", a, b, c))
    if not (W(d / 2) < W(2 * d / 3) < W(d)):
        fails.append(("P5 welfare order", a, b, c))
    # Prop 5 printed-integer ordering when d > 6b (whole a,b,c)
    if d > 6 * b:
        ints = {}
        for s in ("monopoly", "cournot", "bertrand"):
            r = outputs(s, a, b, c)
            ints[s] = {k: half_up(v) for k, v in r.items() if k in ("Q", "f", "profit", "cs", "welfare", "dwl")}
        for key, cmp in (("Q", lambda m, c_, b_: m < c_ < b_), ("f", lambda m, c_, b_: m > c_ > b_),
                         ("dwl", lambda m, c_, b_: m > c_ > b_), ("welfare", lambda m, c_, b_: m < c_ < b_)):
            if not cmp(ints["monopoly"][key], ints["cournot"][key], ints["bertrand"][key]):
                fails.append(("P5 printed order " + key, a, b, c))
        if not (ints["monopoly"]["profit"] > ints["cournot"]["profit"] > ints["bertrand"]["profit"]):
            fails.append(("P5 printed profit order", a, b, c))

print("sweep cases", checked)
print("failures", len(fails))
for x in fails[:20]:
    print("FAIL", x)

# Specific numeric claims in the page
a, b, c = 120, 1, 20
d = a - b * c
print("reference d", d, "d^2/(36b)", F(d * d, 36 * b), float(F(d * d, 36 * b)))
print("monopoly-Cournot profit diff", outputs("monopoly", a, b, c)["profit"] - outputs("cournot", a, b, c)["profit"])
print("W(2d/3)-W(d/2)", outputs("cournot", a, b, c)["welfare"] - outputs("monopoly", a, b, c)["welfare"], "=5d^2/(72b)=", F(5 * d * d, 72 * b))
print("fee diff monopoly-cournot", outputs("monopoly", a, b, c)["f"] - outputs("cournot", a, b, c)["f"], "= d/(6b)", F(d, 6 * b))
print("DWL cournot", outputs("cournot", a, b, c)["dwl"], float(outputs("cournot", a, b, c)["dwl"]), "half_up", half_up(outputs("cournot", a, b, c)["dwl"]))
print("a=121 monopoly fee", outputs("monopoly", 121, 1, 20)["f"], "vol", outputs("monopoly", 121, 1, 20)["Q"], "profit", outputs("monopoly", 121, 1, 20)["profit"])
# L07 R1 root: Q = d(1 +- sqrt2/4) gives dwl = monopoly/2; in [0,a] iff d <= 2 sqrt2 bc (check at random points)
import random
rng = random.Random(5)
bad = 0
for _ in range(20000):
    bb = rng.randint(1, 5); cc = rng.randint(1, 50); dd = rng.randint(1, 500); aa = bb * cc + dd
    r_minus = dd * (1 - math.sqrt(2) / 4)
    r_plus = dd * (1 + math.sqrt(2) / 4)
    mono_loss = (dd / 2) ** 2 / (2 * bb)
    for r in (r_minus, r_plus):
        if abs((dd - r) ** 2 / (2 * bb) - mono_loss / 2) > 1e-9:
            bad += 1
    inside = r_plus <= aa
    if inside != (dd <= 2 * math.sqrt(2) * bb * cc):
        bad += 1
print("L07 R1 root check mismatches", bad)
