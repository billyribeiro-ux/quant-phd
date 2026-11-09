"""Independent re-derivation of L08 Lab 1 and the L08 problem-set numbers (Fraction arithmetic, no lab import)."""
from fractions import Fraction as F
from itertools import product
from math import comb

H = 6
beta = F(9, 10)
St = (0, 1, 2)
Ac = ('run', 'repair')
prof = {0: 6, 1: 4, 2: 1}

def rew(s, a):
    return F(prof[s]) if a == 'run' else F(-4)

def nxt(s, a):
    return min(s + 1, 2) if a == 'run' else 0

def bstep(u):
    new, pol, ties = {}, {}, 0
    for s in St:
        cand = {a: rew(s, a) + beta * u[nxt(s, a)] for a in Ac}
        top = max(cand.values())
        wins = [a for a in Ac if cand[a] == top]
        ties += len(wins) > 1
        new[s] = top
        pol[s] = wins
    return new, pol, ties

V = {H: {s: F(0) for s in St}}
for t in range(H - 1, -1, -1):
    V[t], _, _ = bstep(V[t + 1])
print("V_t(s) exact:")
for t in range(H + 1):
    print(" ", t, [str(V[t][s]) for s in St], [float(V[t][s]) for s in St])
print("V0(0) exact =", V[0][0], "denominator", V[0][0].denominator)
print("V0(0)-V1(0) =", V[0][0] - V[1][0], float(V[0][0] - V[1][0]))
print("V4(0)-V5(0) =", V[4][0] - V[5][0])
print("V4(0) =", V[4][0], "V5 =", [V[5][s] for s in St])
ties_all = 0
for t in range(H):
    new, pol, ties = bstep(V[t + 1])
    ties_all += ties
    print("policy t", t, {s: pol[s] for s in St}, "ties", ties)
print("tied pairs t0..5:", ties_all)

# brute force
def brute(t, s):
    best = None
    cnt = 0
    for plan in product(Ac, repeat=H - t):
        cnt += 1
        st = s
        tot = F(0)
        w = F(1)
        for a in plan:
            tot += w * rew(st, a)
            w *= beta
            st = nxt(st, a)
        tot += w * F(0)
        best = tot if best is None or tot > best else best
    return best, cnt

ok = True
plans = 0
for t in range(H):
    for s in St:
        b, c = brute(t, s)
        ok = ok and b == V[t][s]
        plans += c
print("brute == recursion (18 pairs):", ok, "plans enumerated:", plans)
print("3*(2^6+...+2^1) =", 3 * sum(2 ** k for k in range(1, 7)), " 3*C? ", 3 * sum(2 ** (6 - t) for t in range(6)))

# value iteration
U = [{s: F(0) for s in St}]
for n in range(6):
    new, _, _ = bstep(U[-1])
    U.append(new)
for n in range(6):
    ch = max(abs(U[n + 1][s] - U[n][s]) for s in St)
    print("n", n, "change exact", ch, "float", float(ch), "%.10f" % float(ch))
print("U^n == V_(H-n) for n=0..6:", all(U[n][s] == V[H - n][s] for n in range(7) for s in St))
print("ratios of changes:")
chs = [max(abs(U[n + 1][s] - U[n][s]) for s in St) for n in range(6)]
for n in range(1, 6):
    rr = chs[n] / chs[n - 1]
    print("  n", n, "ratio", rr, float(rr), "%.4f" % float(rr))
print("sum 2^k 1..6 =", sum(2 ** k for k in range(1, 7)))

# M1: V5, V4(0)
print("M1 V5:", [V[5][s] for s in St], "V4(0) run:", 6 + F(9, 10) * V[5][1], "repair:", -4 + F(9, 10) * V[5][0])

# two-state example (problem set): H=2, beta=1/2
b2 = F(1, 2)
V1x = max(F(2), F(1))
V1y = F(3)
V0x = max(2 + b2 * V1y, 1 + b2 * V1x)
V0y = 3 + b2 * V1y
print("problem set: V1x", V1x, "V1y", V1y, "V0x", V0x, "V0y", V0y, "plan (a,d) total", 2 + b2 * 3 + b2 ** 2 * 0)

# Remark 2.5-like negative beta example (beta=-1)
bb = F(-1)
Hh = 2
# plans from (0,s): actions a (r=0), b (r=1), self loop, B=0
tots = []
for p in product(['a', 'b'], repeat=2):
    tot = F(0)
    for k, a in enumerate(p):
        tot += bb ** k * (F(0) if a == 'a' else F(1))
    tots.append(tot)
print("beta=-1 plan totals:", tots, "V0", max(tots))
V1 = max(F(0), F(1))
U1 = max(F(0) + bb * F(0), F(1) + bb * F(0))  # U2=0
U1 = max(F(0), F(1))
U0 = max(F(0) + bb * U1, F(1) + bb * U1)
print("beta=-1: V1", V1, "U1", U1, "U0", U0)

# Remark 1.5
print("Remark 1.5: (U0,U1)=(1+c,c) solves t=0 equation for all c: check c=0.5 ->", (1 + F(1, 2)) == 1 + F(1, 2))
