"""Independent recomputation of the L07 and L08 lab numbers and the hand-derived values on the pages (no lab code imported)."""
from fractions import Fraction as F
from itertools import product

# ---- L07 ----
H = 4
GRID = [0, 100, 200, 300, 400]
U = {0: 0, 100: 60, 200: 100, 300: 120, 400: 130}
def bq(w): return w // 100
# plans by full enumeration of consumptions from each state, feasibility by wealth
def total_plan(t, w, seq):
    tot = 0; wealth = w
    for c in seq:
        if c > wealth: return None
        tot += U[c]; wealth -= c
    return tot + bq(wealth)
def V(t, w):
    best = None; cnt = 0
    for seq in product(GRID, repeat=H - t):
        tot = total_plan(t, w, seq)
        if tot is None: continue
        cnt += 1
        best = tot if best is None or tot > best else best
    return best, cnt
print("L07 V_t(W) by enumeration:")
for t in range(H + 1):
    if t == H:
        print(t, [bq(w) for w in GRID]); continue
    print(t, [V(t, w)[0] for w in GRID])
print("L07 feasible sequences from (0,400):", V(0, 400)[1])
# greedy: largest period reward each step
g = []; w = 400
for _ in range(H):
    c = max(c for c in GRID if c <= w); g.append(c); w -= c
print("L07 greedy", g, "total", total_plan(0, 400, g), "optimum", V(0, 400)[0])
# every continuation of greedy from k=1..3 optimal?
path = [400]
for c in g: path.append(path[-1] - c)
for k in range(1, H):
    print("greedy tail from", k, "wealth", path[k], "tail total", total_plan(k, path[k], g[k:]), "V", V(k, path[k])[0])
# L07 page hand numbers
print("L07 W400 differences:", [240-220, 220-200, 200-130, 130-4])
print("L07 ratio 130/240 =", F(130, 240), float(F(130, 240)))
from math import comb
print("C(8,4)=", comb(8, 4))
print("V0(400)-V3(400)=", 240 - 130)

# ---- L08 ----
Hh = 6; beta = F(9, 10)
PROFIT = {0: 6, 1: 4, 2: 1}
def step(s, a):
    if a == 'run': return F(PROFIT[s]), min(s + 1, 2)
    return F(-4), 0
def bell(terminal):
    vals = [None] * (Hh + 1); vals[Hh] = dict(terminal)
    pol = {}
    for t in range(Hh - 1, -1, -1):
        vals[t] = {}; pol[t] = {}
        for s in range(3):
            cands = {}
            for a in ('run', 'repair'):
                r, ns = step(s, a)
                cands[a] = r + beta * vals[t + 1][ns]
            m = max(cands.values())
            winners = [a for a in ('run', 'repair') if cands[a] == m]
            vals[t][s] = m; pol[t][s] = (winners, len(winners) > 1)
    return vals, pol
vals, pol = bell({0: F(0), 1: F(0), 2: F(0)})
print("L08 Part A (exact fraction, float):")
for t in range(Hh + 1):
    print("t", t, [f"{float(vals[t][s]):.6f}" for s in range(3)], [str(vals[t][s]) for s in range(3)])
ties = 0
for t in range(Hh):
    row = {s: pol[t][s][0][0] for s in range(3)}
    ties += sum(1 for s in range(3) if pol[t][s][1])
    print("policy t", t, row)
print("ties t0..5:", ties)
# brute force
plans = 0; ok = True
for t in range(Hh):
    for s in range(3):
        best = None
        for seq in product(('run', 'repair'), repeat=Hh - t):
            st = s; tot = F(0); wgt = F(1); plans += 1
            for a in seq:
                r, ns = step(st, a); tot += wgt * r; wgt *= beta; st = ns
            best = tot if best is None or tot > best else best
        ok = ok and best == vals[t][s]
print("plans enumerated", plans, "brute matches", ok)
# value iteration
its = [{0: F(0), 1: F(0), 2: F(0)}]
for n in range(6):
    prev = its[-1]; new = {}
    for s in range(3):
        new[s] = max(step(s, a)[0] + beta * prev[step(s, a)[1]] for a in ('run', 'repair'))
    its.append(new)
chg = [max(abs(its[n + 1][s] - its[n][s]) for s in range(3)) for n in range(6)]
print("changes exact", [str(c) for c in chg])
print("changes", [f"{float(c):.10f}" for c in chg])
print("iterate == V_(H-n):", all(its[n][s] == vals[Hh - n][s] for n in range(7) for s in range(3)))
print("ratios", [str(chg[n] / chg[n - 1]) for n in range(1, 6)])
print("ratios float", [f"{float(chg[n] / chg[n - 1]):.6f}" for n in range(1, 6)])
print("V0(0)-V1(0) exact", vals[0][0] - vals[1][0], float(vals[0][0] - vals[1][0]))
print("V4(0)-V5(0) exact", vals[4][0] - vals[5][0])
def decimals(q):
    # smallest k with q * 10**k an integer (finite decimal expansion), else None
    k = 0
    while (q * 10 ** k).denominator != 1 and k < 60:
        k += 1
    return k if (q * 10 ** k).denominator == 1 else None
print("decimal places needed per V_t(s):", max(decimals(vals[t][s]) for t in range(7) for s in range(3)))
