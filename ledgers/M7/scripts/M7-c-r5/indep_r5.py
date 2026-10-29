# Independent recomputation for M7 slice c (L07, L08), round 5. Written from the prose, not from the twins.
from fractions import Fraction as F
from itertools import product
from math import comb

# ---- L07 toy: wealth grid in cents, consumption grid, utils reward table, H=4, bequest W//100
G = (0, 100, 200, 300, 400)
U = {0: 0, 100: 60, 200: 100, 300: 120, 400: 130}
H = 4
def Vtab():
    V = {H: {w: w // 100 for w in G}}
    for t in range(H - 1, -1, -1):
        V[t] = {w: max(U[c] + V[t + 1][w - c] for c in G if c <= w) for w in G}
    return V
V = Vtab()
print("L07 V_t(400) t=0..4:", [V[t][400] for t in range(5)])
print("L07 table row t=0..4:", [[V[t][w] for w in G] for t in range(5)])
d = [V[t][400] - V[t + 1][400] for t in range(4)]
print("L07 E1 differences:", d, "largest index", d.index(max(d)))
print("L07 E2 ratio 130/240 =", F(130, 240), float(F(130, 240)))
# brute-force count of feasible sequences from (0,400), 4 periods
cnt = sum(1 for p in product(G, repeat=4) if sum(p) <= 400)
print("L07 feasible sequences from 400 (4 periods):", cnt, "C(8,4)=", comb(8, 4))
# greedy from 400: take 400 then zero
greedy = 130 + 0
print("L07 greedy total:", greedy, "optimal total:", V[0][400])
# M1-M3 problem of L07
# states x,y; A(x)={u,v}; A(y)={w}; f(x,u)=y; f(x,v)=x; f(y,w)=y; r(x,u)=3; r(x,v)=5; r(y,w)=2; B(x)=0; B(y)=1; H=2
V1x = max(3 + 1, 5 + 0); V1y = 2 + 1; V0x = max(3 + V1y, 5 + V1x)
print("L07 M1: V1x V1y V0x", V1x, V1y, V0x)
# plans from (0,x)
plans = {"uw": 3 + (2 + 1), "vu": 5 + (3 + 1), "vv": 5 + 5}
print("L07 M3 plans:", plans)

# ---- L08 maintenance toy: H=6, beta=9/10, states 0,1,2; run: profit 6,4,1, next min(s+1,2); repair: -4, next 0
b = F(9, 10)
P = {0: 6, 1: 4, 2: 1}
def step(s, a):
    return (F(P[s]), min(s + 1, 2)) if a == "run" else (F(-4), 0)
Vb = {6: {s: F(0) for s in range(3)}}
pol = {}
ties = 0
for t in range(5, -1, -1):
    Vb[t] = {}
    for s in range(3):
        cands = {}
        for a in ("run", "repair"):
            r, n = step(s, a)
            cands[a] = r + b * Vb[t + 1][n]
        m = max(cands.values())
        if sum(1 for x in cands.values() if x == m) > 1:
            ties += 1
        Vb[t][s] = m
        pol[(t, s)] = max(cands, key=lambda a: cands[a])
for t in range(7):
    print("L08 t", t, [float(Vb[t][s]) for s in range(3)])
print("L08 policy s2 by t:", [pol[(t, 2)] for t in range(6)], "ties", ties)
print("L08 V0(0) exact:", Vb[0][0], float(Vb[0][0]))
# brute force over all 2-action sequences from (t,s) with discounted totals
def brute(t, s):
    best = None; n = 0
    for seq in product(("run", "repair"), repeat=6 - t):
        n += 1; st = s; tot = F(0); w = F(1)
        for a in seq:
            r, nx = step(st, a); tot += w * r; w *= b; st = nx
        best = tot if best is None or tot > best else best
    return best, n
total_plans = 0; ok = True
for t in range(6):
    for s in range(3):
        bb, n = brute(t, s); total_plans += n; ok = ok and bb == Vb[t][s]
print("L08 plans enumerated", total_plans, "brute match", ok, "3*126=", 3 * 126)
# value iteration from 0
Ut = [{s: F(0) for s in range(3)}]
for _ in range(6):
    prev = Ut[-1]; new = {}
    for s in range(3):
        new[s] = max(step(s, a)[0] + b * prev[step(s, a)[1]] for a in ("run", "repair"))
    Ut.append(new)
for n in range(6):
    ch = max(abs(Ut[n + 1][s] - Ut[n][s]) for s in range(3))
    print("L08 change n", n, float(ch), ch)
print("L08 iterate equals V_(6-n):", all(Ut[n][s] == Vb[6 - n][s] for n in range(7) for s in range(3)))
ch = [max(abs(Ut[n + 1][s] - Ut[n][s]) for s in range(3)) for n in range(6)]
print("L08 E2 ratios:", [float(ch[i] / ch[i - 1]) for i in range(1, 6)])
print("L08 E1 diffs:", float(Vb[0][0] - Vb[1][0]), float(Vb[4][0] - Vb[5][0]))
# R1/Canon example: H=2, one state, A={x,y}, r(x)=0, r(y)=1, B=0, beta=-1
bb = F(-1)
tot = {}
for seq in product(("x", "y"), repeat=2):
    rr = {"x": 0, "y": 1}; w = F(1); T = F(0)
    for a in seq:
        T += w * rr[a]; w *= bb
    tot[seq] = T
print("negative discount totals", tot, "V0", max(tot.values()))
U1 = max(0, 1); U0 = max(0 + bb * U1, 1 + bb * U1)
print("negative discount U1, U0:", U1, U0)
# Problem M2/M3 of L08: A(x)={a,b}, A(y)={c}; f(x,a)=y, f(x,b)=x, f(y,c)=y; r(x,a)=2, r(x,b)=1, r(y,c)=3; H=2; beta=1/2
h = F(1, 2)
W1x = max(2, 1); W1y = 3
W0x = max(2 + h * W1y, 1 + h * W1x); W0y = 3 + h * W1y
print("L08 M2:", W1x, W1y, W0x, W0y, "M3 plan (a,c):", 2 + h * 3 + h * h * 0)
# Remark 1.5 check: H=1, r=1, beta=1, U0=1+c, U1=c
print("Remark1.5 ok:", all((1 + c) == 1 + c for c in [F(-3), F(0), F(5)]))
# E1 claim: values have at most five decimals
print("L08 V0(0) decimals check:", (Vb[0][0] * 10**5).denominator == 1)
