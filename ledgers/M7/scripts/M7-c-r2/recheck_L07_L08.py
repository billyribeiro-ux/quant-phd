# Independent recomputation of the L07 and L08 numbers (written by the verifier; does not import the twins).
from fractions import Fraction as F
from itertools import product
import math

# ---- L07: wealth problem ----
H = 4
G = (0, 100, 200, 300, 400)
u = {0: 0, 100: 60, 200: 100, 300: 120, 400: 130}
bq = lambda w: w // 100
V = {H: {w: bq(w) for w in G}}
for t in range(H - 1, -1, -1):
    V[t] = {w: max(u[c] + V[t + 1][w - c] for c in G if c <= w) for w in G}
print("L07 W400 column t0..t4:", [V[t][400] for t in range(5)])
print("L07 full table:", {t: [V[t][w] for w in G] for t in range(5)})
# brute force all sequences of consumption of length H-t from w, counting feasible
def bf(t, w):
    best = None; cnt = 0
    for seq in product(G, repeat=H - t):
        ww = w; tot = 0; ok = True
        for c in seq:
            if c > ww: ok = False; break
            tot += u[c]; ww -= c
        if not ok: continue
        cnt += 1
        tot += bq(ww)
        best = tot if best is None or tot > best else best
    return best, cnt
print("L07 feasible seqs from (0,400):", bf(0, 400)[1], "C(8,4)=", math.comb(8, 4))
print("L07 brute==recursion all:", all(bf(t, w)[0] == V[t][w] for t in range(H) for w in G))
# greedy from 400
print("L07 greedy total: ", u[400] + 0)
opt_plan_total = 4 * 60
print("L07 optimal total 4*60 =", opt_plan_total, "; V0(400)=", V[0][400])
print("L07 E2 ratio 130/240 =", F(130, 240), float(F(130, 240)))
print("L07 E1 diffs:", [V[t][400] - V[t + 1][400] for t in range(4)])
print("L07 counterexample remark: V0(x)=", max(0 + 0, 1 + 0))

# ---- L08: maintenance problem, exact Fractions ----
Hh = 6; beta = F(9, 10)
S = (0, 1, 2)
prof = {0: 6, 1: 4, 2: 1}
def rew(s, a): return F(prof[s]) if a == "run" else F(-4)
def nxt(s, a): return min(s + 1, 2) if a == "run" else 0
A = ("run", "repair")
Vb = {Hh: {s: F(0) for s in S}}
policy = {}
ties_total = 0
for t in range(Hh - 1, -1, -1):
    Vb[t] = {}
    for s in S:
        cand = {a: rew(s, a) + beta * Vb[t + 1][nxt(s, a)] for a in A}
        Vb[t][s] = max(cand.values())
for t in range(Hh):
    for s in S:
        cand = {a: rew(s, a) + beta * Vb[t + 1][nxt(s, a)] for a in A}
        if cand["run"] == cand["repair"]: ties_total += 1
        policy[(t, s)] = max(A, key=lambda a: cand[a])
print("L08 V0(0)=", float(Vb[0][0]), "V4(0)=", float(Vb[4][0]), "V5(0)=", float(Vb[5][0]), "V0(0)-V1(0)=", Vb[0][0] - Vb[1][0])
for t in range(7):
    print("L08 t", t, [f"{float(Vb[t][s]):.6f}" for s in S])
print("L08 policy s2 by t:", [policy[(t, 2)] for t in range(6)], "s0:", [policy[(t,0)] for t in range(6)], "s1:", [policy[(t,1)] for t in range(6)])
print("L08 ties t0..5 (exact, counting cand equal):", ties_total)
# brute force
tot_checked = 0; all_ok = True
for t in range(Hh):
    for s in S:
        best = None
        for seq in product(A, repeat=Hh - t):
            st = s; total = F(0); wgt = F(1)
            for a in seq:
                total += wgt * rew(st, a); wgt *= beta; st = nxt(st, a)
            tot_checked += 1
            best = total if best is None or total > best else best
        all_ok = all_ok and best == Vb[t][s]
print("L08 plans enumerated:", tot_checked, "brute==recursion:", all_ok)
# value iteration
U = [{s: F(0) for s in S}]
for n in range(6):
    prev = U[-1]
    U.append({s: max(rew(s, a) + beta * prev[nxt(s, a)] for a in A) for s in S})
ch = [max(abs(U[n + 1][s] - U[n][s]) for s in S) for n in range(6)]
print("L08 changes exact:", [str(c) for c in ch])
print("L08 changes display:", [f"{float(c):.10f}" for c in ch])
print("L08 ratios of changes:", [float(ch[n]/ch[n-1]) for n in range(1,6)])
print("L08 U^n == V_(H-n):", all(U[n][s] == Vb[Hh - n][s] for n in range(7) for s in S))
print("L08 decimal places check: V0(0) exact =", Vb[0][0], "denominator", Vb[0][0].denominator)
print("L08 E1 V0(0)-V1(0) =", float(Vb[0][0]-Vb[1][0]), " V4(0)-V5(0)=", float(Vb[4][0]-Vb[5][0]))
print("L08 M1 check: V4(0) run=", 6 + F(9,10)*Vb[5][1], " repair=", -4 + F(9,10)*Vb[5][0])
# L08 M2/M3 problem (beta=1/2, two states)
b2 = F(1,2)
V1x = max(F(2), F(1)); V1y = F(3)
V0x = max(2 + b2*V1y, 1 + b2*V1x); V0y = 3 + b2*V1y
print("L08 M2:", V1x, V1y, V0x, V0y, " M3 plan (a,c):", 2 + b2*3 + b2*b2*0)
# L08 negative discount example
bb = F(-1)
plans = [(a0, a1) for a0 in "xy" for a1 in "xy"]
rr = {"x": 0, "y": 1}
totals = [rr[a0] + bb*rr[a1] for a0, a1 in plans]
print("L08 neg-discount totals:", totals, "V0=", max(totals))
V1 = max(rr[a] for a in "xy")
U1 = V1
U0 = max(0 + bb*U1, 1 + bb*U1)
print("L08 neg: V1=", V1, "U1=", U1, "U0=", U0, "V0=", max(totals))
# L08 R2-style: U2 as max over pairs of length 2 with B replaced by U0 (sanity: n=2 iterate)
# L08 M1 V5 and V4
print("L08 V5:", [float(Vb[5][s]) for s in S])
