"""Independent re-derivation of every number on M7 L07 and L08 (verifier, round 1).

Written from the page prose, not from the lab code. Exact Fraction arithmetic throughout.
Run: python3 -I -W error ledgers/M7/scripts/M7-c-r1/indep_L07_L08.py
"""
from fractions import Fraction as F
from itertools import product
from math import comb

# ---------- L07 toy problem: W grid 0..400 by 100, consumption c in grid, c<=W, u(c), bequest W//100, H=4
U = {0: 0, 100: 60, 200: 100, 300: 120, 400: 130}
G = [0, 100, 200, 300, 400]
H = 4


def bequest(w):
    return w // 100


# value by recursion (independent code: memo recursion, not backward table)
from functools import lru_cache


@lru_cache(None)
def V(t, w):
    if t == H:
        return bequest(w)
    return max(U[c] + V(t + 1, w - c) for c in G if c <= w)


print("L07 V_t(W) table:")
for t in range(H + 1):
    print(" ", t, [V(t, w) for w in G])
print("L07 V0(400)=", V(0, 400), " V1(400)=", V(1, 400), " V3(400)=", V(3, 400), " V0-V3=", V(0, 400) - V(3, 400))
print("L07 E1 diffs W400:", [V(t, 400) - V(t + 1, 400) for t in range(4)])
# brute force: all sequences of length 4 over G, feasibility stepwise
cnt = 0
best = None
for seq in product(G, repeat=H):
    w = 400
    tot = 0
    ok = True
    for c in seq:
        if c > w:
            ok = False
            break
        tot += U[c]
        w -= c
    if not ok:
        continue
    cnt += 1
    tot += bequest(w)
    best = tot if best is None or tot > best else best
print("L07 feasible sequences from (0,400):", cnt, " C(8,4)=", comb(8, 4), " brute best=", best)
# greedy: largest U at each step
w = 400
gt = 0
seq = []
for _ in range(H):
    c = max((c for c in G if c <= w), key=lambda x: U[x])
    seq.append(c)
    gt += U[c]
    w -= c
gt += bequest(w)
print("L07 greedy", seq, "total", gt, "ratio", F(gt, V(0, 400)), float(F(gt, V(0, 400))))
print("L07 greedy tails optimal:", [ (k, gt_k == V(k, w_k)) for k, gt_k, w_k in []])
# greedy tail check
w = 400
path = [400]
for c in seq:
    w -= c
    path.append(w)
for k in range(1, H):
    tot = sum(U[c] for c in seq[k:]) + bequest(path[H])
    print("L07 greedy tail from t", k, "wealth", path[k], "total", tot, "V", V(k, path[k]), tot == V(k, path[k]))
# action sets for optimal plan from (0,400)
opt = []
w = 400
for t in range(H):
    c = max((c for c in G if c <= w), key=lambda x: U[x] + V(t + 1, w - x))
    opt.append(c)
    w -= c
print("L07 optimal plan", opt)
# V1(400) witness 200,100,100
print("L07 witness 200,100,100 from 400 total:", U[200] + U[100] + U[100] + bequest(0))

# Two-period remark 2.5 check: H=2, S={x,y}, A(x)={a,b}, A(y)={c}, f(x,a)=f(x,b)=y, f(y,c)=y, r(x,a)=0, r(x,b)=1, r(y,c)=0, B=0
# plans from (0,x): (a,c) total 0 ; (b,c) total 1 -> V0(x)=1 attained only by b; V1(y)=0 ; continuation (c) optimal
print("R2.5 plans from (0,x): (a,c)=", 0 + 0, " (b,c)=", 1 + 0, " V0(x)=", max(0, 1))

# ---------- L07 problem set two-period example (M1-M3, P2-P3 are checks)
# states x,y ; A(x)={u,v}, A(y)={w}; f(x,u)=y, f(x,v)=x, f(y,w)=y; r(x,u)=3, r(x,v)=5, r(y,w)=2; B(x)=0 B(y)=1; H=2
r = {("x", "u"): 3, ("x", "v"): 5, ("y", "w"): 2}
fn = {("x", "u"): "y", ("x", "v"): "x", ("y", "w"): "y"}
Bq = {"x": 0, "y": 1}
A = {"x": ["u", "v"], "y": ["w"]}
V1 = {s: max(r[(s, a)] + Bq[fn[(s, a)]] for a in A[s]) for s in "xy"}
V0x = max(r[("x", a)] + V1[fn[("x", a)]] for a in A["x"])
print("M1: V1", V1, "V0(x)", V0x)
plans = []
for a0 in A["x"]:
    for a1 in A[fn[("x", a0)]]:
        s1 = fn[("x", a0)]
        s2 = fn[(s1, a1)]
        plans.append(((a0, a1), r[("x", a0)] + r[(s1, a1)] + Bq[s2]))
print("M3 plans", plans)

# ---------- L08 maintenance problem
DISC = F(9, 10)
PROFIT = {0: 6, 1: 4, 2: 1}
RC = 4


def rew(s, a):
    return F(PROFIT[s]) if a == "run" else F(-RC)


def nxt(s, a):
    return min(s + 1, 2) if a == "run" else 0


@lru_cache(None)
def W(t, s):
    if t == 6:
        return F(0)
    return max(rew(s, a) + DISC * W(t + 1, nxt(s, a)) for a in ("run", "repair"))


print("L08 V table:")
for t in range(7):
    print(" ", t, [float(W(t, s)) for s in range(3)], [W(t, s) for s in range(3)] if t in (0, 1) else "")
# optimal action and ties
for t in range(6):
    row = []
    ties = 0
    for s in range(3):
        cands = {a: rew(s, a) + DISC * W(t + 1, nxt(s, a)) for a in ("run", "repair")}
        top = max(cands.values())
        win = [a for a in cands if cands[a] == top]
        if len(win) > 1:
            ties += 1
        row.append((s, win[0], len(win)))
    print("L08 policy t", t, row, "ties", ties)
# brute force enumeration, independent
plans_n = 0
allok = True
for t in range(6):
    for s in range(3):
        best = None
        for seq in product(("run", "repair"), repeat=6 - t):
            plans_n += 1
            st = s
            tot = F(0)
            wt = F(1)
            for a in seq:
                tot += wt * rew(st, a)
                wt *= DISC
                st = nxt(st, a)
            best = tot if best is None or tot > best else best
        allok = allok and best == W(t, s)
print("L08 plans enumerated", plans_n, "3*(2^6+..+2^1)=", 3 * (2**6 + 2**5 + 2**4 + 2**3 + 2**2 + 2**1), "brute==recursion", allok)
# value iteration
it = [{s: F(0) for s in range(3)}]
for n in range(6):
    prev = it[-1]
    new = {s: max(rew(s, a) + DISC * prev[nxt(s, a)] for a in ("run", "repair")) for s in range(3)}
    it.append(new)
for n in range(6):
    ch = max(abs(it[n + 1][s] - it[n][s]) for s in range(3))
    print("L08 change n", n, float(ch), ch)
print("L08 iterate n equals V_(6-n):", all(it[n][s] == W(6 - n, s) for n in range(7) for s in range(3)))
# ratios
chg = [max(abs(it[n + 1][s] - it[n][s]) for s in range(3)) for n in range(6)]
print("L08 ratios chg[n]/chg[n-1]:", [float(chg[n] / chg[n - 1]) for n in range(1, 6)])
print("L08 V0(0)-V1(0)=", float(W(0, 0) - W(1, 0)), W(0, 0) - W(1, 0))
print("L08 V4(0)-V5(0)=", float(W(4, 0) - W(5, 0)))
print("L08 V4(0) run value", float(rew(0, "run") + DISC * W(5, 1)), "repair", float(rew(0, "repair") + DISC * W(5, 0)))
print("L08 V_0 exact decimal digits check: W(0,0) denominator", W(0, 0).denominator)
print("L08 V0(0)*10^5 integer?", (W(0, 0) * 100000).denominator)

# ---------- L08 negative discount example: H=2, one state, A={x,y}, r(x)=0, r(y)=1, B=0, beta=-1
beta = -1
plans_neg = {}
for a0, a1 in product("xy", repeat=2):
    rr = {"x": 0, "y": 1}
    plans_neg[(a0, a1)] = rr[a0] + beta * rr[a1]
print("L08 neg-beta plan totals", plans_neg, "V0", max(plans_neg.values()))
U1 = max(0 + beta * 0, 1 + beta * 0)
U0 = max(0 + beta * U1, 1 + beta * U1)
print("L08 neg-beta U1", U1, "U0", U0)

# ---------- L08 M2/M3 two-state example, beta=1/2
b2 = F(1, 2)
rr2 = {("x", "a"): F(2), ("x", "b"): F(1), ("y", "c"): F(3)}
nx2 = {("x", "a"): "y", ("x", "b"): "x", ("y", "c"): "y"}
A2 = {"x": ["a", "b"], "y": ["c"]}
V1b = {s: max(rr2[(s, a)] for a in A2[s]) for s in "xy"}
V0b = {s: max(rr2[(s, a)] + b2 * V1b[nx2[(s, a)]] for a in A2[s]) for s in "xy"}
print("L08 M2 V1", V1b, "V0", V0b)
print("L08 M3 plan (a,c) total", rr2[("x", "a")] + b2 * rr2[("y", "c")])
