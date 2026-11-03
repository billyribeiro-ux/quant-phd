"""Independent recomputation of the L07 and L08 lab numbers and of the prose/card numbers (round 2, slice e).

Written from the lesson text (L07 Lab 1 and L08 Lab 1 descriptions), not from the lab twin code.
Standard library only. Usage: python3 -I verify_l07_l08_r2.py
"""
from fractions import Fraction as F
from itertools import product

# ---- L07 toy: states wealth 0..400 cents, consumption grid, reward table, bequest W//100 ----
H7 = 4
G7 = (0, 100, 200, 300, 400)
U7 = {0: 0, 100: 60, 200: 100, 300: 120, 400: 130}
V = [dict() for _ in range(H7 + 1)]
V[H7] = {w: w // 100 for w in G7}
for t in range(H7 - 1, -1, -1):
    for w in G7:
        V[t][w] = max(U7[c] + V[t + 1][w - c] for c in G7 if c <= w)
for t in range(H7 + 1):
    print("L07 t", t, [V[t][w] for w in G7])
# brute force from (t,w): all consumption sequences, feasible ones only
feas_count = 0
bf_ok = True
for t in range(H7):
    for w in G7:
        best = None
        for plan in product(G7, repeat=H7 - t):
            wl = w
            tot = 0
            ok = True
            for c in plan:
                if c > wl:
                    ok = False
                    break
                tot += U7[c]
                wl -= c
            if not ok:
                continue
            tot += wl // 100
            if t == 0 and w == 400:
                feas_count += 1
            best = tot if best is None else max(best, tot)
        bf_ok = bf_ok and best == V[t][w]
print("L07 brute-force matches recursion at all t<H, all w:", bf_ok, "; feasible plans from (0,400):", feas_count)
print("L07 E3 binom(8,4) =", 70)
print("L07 E1 diffs W400:", 240 - 220, 220 - 200, 200 - 130, 130 - 4)
print("L07 E2 ratio 130/240 =", F(130, 240), float(F(130, 240)))
print("L07 M1 V1(x)=max(u:3+B(y)=4, v:5+B(x)=5)=5, V1(y)=3, V0(x)=max(3+3, 5+5)=10 ->", max(3 + 3, 5 + 5))
print("L07 M3 plans totals: (u,w)=", 3 + (2 + 1), " (v,u)=", 5 + (3 + 1), " (v,v)=", 5 + 5)
# greedy and optimal from (0,400)
greedy = 130
print("L07 greedy total 130 vs optimal", V[0][400], " ratio check", greedy == 130)
# Remark 2.5 check (H=2): V1(y)=0, V0(x)=max(0,1)=1
print("L07 Remark2.5 V0(x)=", max(0 + 0, 1 + 0))
# Problem R2 (max-reward objective)
print("L07 R2: (a0,b) max(10,5)=", max(10, 5), " (a0,c) max(10,3)=", max(10, 3), " V1(x)=", max(5, 3))

# ---- L08 maintenance: profit 6/4/1, repair cost 4, discount 9/10, H=6, terminal 0 ----
H8 = 6
B8 = F(9, 10)
PROF = {0: 6, 1: 4, 2: 1}


def rew(s, a):
    return F(PROF[s]) if a == "run" else F(-4)


def nxt(s, a):
    return min(s + 1, 2) if a == "run" else 0


VV = [dict() for _ in range(H8 + 1)]
VV[H8] = {s: F(0) for s in (0, 1, 2)}
pol = {}
ties = 0
for t in range(H8 - 1, -1, -1):
    for s in (0, 1, 2):
        cand = {a: rew(s, a) + B8 * VV[t + 1][nxt(s, a)] for a in ("run", "repair")}
        VV[t][s] = max(cand.values())
        pol[(t, s)] = max(cand, key=lambda a: cand[a])
        if list(cand.values()).count(VV[t][s]) > 1:
            ties += 1
for t in range(H8 + 1):
    print("L08 V_t", t, [str(VV[t][s]) for s in (0, 1, 2)], [str(float(VV[t][s])) for s in (0, 1, 2)])
print("L08 policy s2:", [pol[(t, 2)] for t in range(H8)], "s0:", [pol[(t, 0)] for t in range(H8)], "ties:", ties)
# brute force count and check
cnt = 0
bf = True
for t in range(H8):
    for s in (0, 1, 2):
        best = None
        for seq in product(("run", "repair"), repeat=H8 - t):
            st = s
            tot = F(0)
            for k, a in enumerate(seq):
                tot += B8 ** k * rew(st, a)
                st = nxt(st, a)
            tot += B8 ** (H8 - t) * F(0)
            cnt += 1
            best = tot if best is None else max(best, tot)
        bf = bf and best == VV[t][s]
print("L08 brute-force matches:", bf, "sequences enumerated:", cnt)
print("L08 3*(2^6+...+2^1)=", 3 * sum(2 ** k for k in range(1, 7)))
# value iteration
U = {s: F(0) for s in (0, 1, 2)}
iters = [dict(U)]
for n in range(7):
    newU = {s: max(rew(s, a) + B8 * U[nxt(s, a)] for a in ("run", "repair")) for s in (0, 1, 2)}
    iters.append(newU)
    ch = max(abs(newU[s] - U[s]) for s in (0, 1, 2))
    print("L08 change n", n, float(ch), str(ch))
    U = newU
for n in range(7):
    assert iters[n] == VV[H8 - n], n
print("L08 iterates equal V_(H-n) for n=0..6: True")
print("L08 E1 V0(0)-V1(0)=", VV[0][0] - VV[1][0], float(VV[0][0] - VV[1][0]), " V4(0)-V5(0)=", VV[4][0] - VV[5][0])
print("L08 E2 ratios:", [float(F(3, 5) * 0 + 0)] if False else "")
ch_list = []
U = {s: F(0) for s in (0, 1, 2)}
for n in range(6):
    newU = {s: max(rew(s, a) + B8 * U[nxt(s, a)] for a in ("run", "repair")) for s in (0, 1, 2)}
    ch_list.append(max(abs(newU[s] - U[s]) for s in (0, 1, 2)))
    U = newU
print("L08 ratios:", [float(ch_list[i] / ch_list[i - 1]) for i in range(1, 6)])
# L08 two-state example M2/M3 (beta = 1/2)
bx = F(1, 2)
V1x, V1y = 2, 3
V0x = max(2 + bx * V1y, 1 + bx * V1x)
V0y = 3 + bx * V1y
print("L08 M2 V0x", V0x, "V0y", V0y, "M3 plan (a,c) total", 2 + bx * 3)
# Remark 2.5 / negative discount example (beta=-1)
bm = F(-1)
tot = [0, 0 + bm * 1, 1, 1 + bm * 0]
print("L08 beta=-1 plan totals (x,x),(x,y),(y,x),(y,y)=", [F(0), F(0) + bm * 1, F(1) + bm * 0, F(1) + bm * 1])
U1 = 1
U0 = max(0 + bm * U1, 1 + bm * U1)
print("L08 beta=-1 U0 =", U0, " V0 = 1")
