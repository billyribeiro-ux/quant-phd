"""Brute-force check of every small worked example on L07 and L08 (independent of the pages' code)."""
from fractions import Fraction as F
from itertools import product


def plans(S, A, f, t, s, H):
    """All feasible action sequences from (t,s) and their state paths."""
    out = []
    def rec(k, st, acc, states):
        if k == H:
            out.append((tuple(acc), tuple(states)))
            return
        for a in A[st]:
            rec(k + 1, f[(st, a)], acc + [a], states + [f[(st, a)]])
    rec(t, s, [], [s])
    return out


def J(p, t, s, H, r, B, beta=F(1)):
    acts, states = p
    tot = F(0)
    for k in range(t, H):
        tot += beta ** (k - t) * r[(states[k - t], acts[k - t])]
    return tot + beta ** (H - t) * B[states[H - t]]


def V(S, A, f, t, s, H, r, B, beta=F(1)):
    return max(J(p, t, s, H, r, B, beta) for p in plans(S, A, f, t, s, H))


# ---- L07 M1-M3: states x,y; A(x)={u,v}, A(y)={w}; f(x,u)=y, f(x,v)=x, f(y,w)=y; r(x,u)=3, r(x,v)=5, r(y,w)=2; B(x)=0, B(y)=1; H=2
S = ['x', 'y']; A = {'x': ['u', 'v'], 'y': ['w']}
f = {('x', 'u'): 'y', ('x', 'v'): 'x', ('y', 'w'): 'y'}
r = {('x', 'u'): 3, ('x', 'v'): 5, ('y', 'w'): 2}
B = {'x': 0, 'y': 1}
print("L07 M1 V1(x),V1(y),V0(x):", V(S, A, f, 1, 'x', 2, r, B), V(S, A, f, 1, 'y', 2, r, B), V(S, A, f, 0, 'x', 2, r, B))
for p in plans(S, A, f, 0, 'x', 2):
    print("L07 M3 plan", p[0], "total", J(p, 0, 'x', 2, r, B))

# ---- L07 Remark 2.5: H=2, S={x,y}, A(x)={a,b}, A(y)={c}, f(x,a)=f(x,b)=y, f(y,c)=y, r(x,a)=0, r(x,b)=1, r(y,c)=0, B=0
S2 = ['x', 'y']; A2 = {'x': ['a', 'b'], 'y': ['c']}
f2 = {('x', 'a'): 'y', ('x', 'b'): 'y', ('y', 'c'): 'y'}
r2 = {('x', 'a'): 0, ('x', 'b'): 1, ('y', 'c'): 0}
B2 = {'x': 0, 'y': 0}
print("L07 Remark2.5 V1(y)=", V(S2, A2, f2, 1, 'y', 2, r2, B2), " V0(x)=", V(S2, A2, f2, 0, 'x', 2, r2, B2))
print("   J((a,c))=", J((('a', 'c'), ('x', 'y', 'y')), 0, 'x', 2, r2, B2), "  plans from (1,y):", plans(S2, A2, f2, 1, 'y', 2))

# ---- L07 Remark 1.3 (infinite action set): sup of totals with A(s)=(0,1); use a grid to show sup approaches 1
for n in (10, 100, 1000):
    grid = [F(i, n) for i in range(1, n)]
    print("L07 Remark1.3 finite grid n=%d max total" % n, max(grid))

# ---- L07 R2: objective J(p)=max_k r(s_k,a_k), B=0, H=2, S={s,x}, A(s)={a0}, A(x)={b,c}, f(s,a0)=x, f(x,*)=x, r(s,a0)=10, r(x,b)=5, r(x,c)=3
def Jmax(p, t, s, H, r):
    acts, states = p
    return max(r[(states[k - t], acts[k - t])] for k in range(t, H))
Sr = ['s', 'x']; Ar = {'s': ['a0'], 'x': ['b', 'c']}
fr = {('s', 'a0'): 'x', ('x', 'b'): 'x', ('x', 'c'): 'x'}
rr = {('s', 'a0'): 10, ('x', 'b'): 5, ('x', 'c'): 3}
for p in plans(Sr, Ar, fr, 0, 's', 2):
    print("L07 R2 plan", p[0], "objective", Jmax(p, 0, 's', 2, rr))
for p in plans(Sr, Ar, fr, 1, 'x', 2):
    print("L07 R2 from (1,x) plan", p[0], "objective", Jmax(p, 1, 'x', 2, rr))

# ---- L07 R2 of the L07 lab: greedy vs optimum already in lab script
# ---- L08 M2/M3: S={x,y}; A(x)={a,b}, A(y)={d}; f(x,a)=y; f(x,b)=x; f(y,d)=y; r(x,a)=2; r(x,b)=1; r(y,d)=3; B=0; H=2; beta=1/2
S3 = ['x', 'y']; A3 = {'x': ['a', 'b'], 'y': ['d']}
f3 = {('x', 'a'): 'y', ('x', 'b'): 'x', ('y', 'd'): 'y'}
r3 = {('x', 'a'): 2, ('x', 'b'): 1, ('y', 'd'): 3}
B3 = {'x': 0, 'y': 0}
b = F(1, 2)
print("L08 M2 V1(x),V1(y),V0(x),V0(y):", V(S3, A3, f3, 1, 'x', 2, r3, B3, b), V(S3, A3, f3, 1, 'y', 2, r3, B3, b),
      V(S3, A3, f3, 0, 'x', 2, r3, B3, b), V(S3, A3, f3, 0, 'y', 2, r3, B3, b))
print("L08 M3 J((a,d)) from (0,x)=", J((('a', 'd'), ('x', 'y', 'y')), 0, 'x', 2, r3, B3, b))
# ---- L08 negative discount example: H=2, one state, A={a,b}, f=s, r(a)=0, r(b)=1, B=0, beta=-1
S4 = ['s']; A4 = {'s': ['a', 'b']}; f4 = {('s', 'a'): 's', ('s', 'b'): 's'}; r4 = {('s', 'a'): 0, ('s', 'b'): 1}; B4 = {'s': 0}
tots = [J(p, 0, 's', 2, r4, B4, F(-1)) for p in plans(S4, A4, f4, 0, 's', 2)]
print("L08 neg-disc totals", tots, "V0", max(tots), "V1", V(S4, A4, f4, 1, 's', 1, r4, B4, F(-1)))
# Bellman with U2=0: U1 = max{0,1}; U0 = max{0 + (-1)U1, 1 + (-1)U1}
U1 = max(r4[('s', a)] + F(-1) * 0 for a in A4['s']); U0 = max(r4[('s', a)] + F(-1) * U1 for a in A4['s'])
print("L08 neg-disc U1", U1, "U0", U0)
# L08 Remark 1.5: H=1 one state A={a} r=1 f=s beta=1: check U0 = 1 + c, U1 = c solves t=0 eq
print("L08 Remark1.5 check c=5: U0=1+c=", 1 + 5, " rhs=", 1 + 1 * 5)
# L08 P1 H=1 uniqueness: trivial; P3 (beta=1, B=0) V0 = 1
# L08 misconception 1: one state one action r=1 f=s beta=1: U1 = 1 + U0
print("L08 misc1 U1 from U0=0:", 1 + 0, " from U0=5:", 1 + 5)
# L08 M1: V5 = max r (B=0); V4(0) = max{6+0.9*V5(1), -4+0.9*V5(0)}
print("L08 M1 V4(0) run:", F(6) + F(9, 10) * 4, " repair:", F(-4) + F(9, 10) * 6)
# L08 R3 counterexample u_n=1/n
for n in range(1, 6):
    u = lambda k: F(1, k)
    ch = abs(u(n + 1) - u(n)); dist = abs(u(n) - 0)
    print("L08 R3 n=%d change=%s dist=%s dist/change=%s" % (n, ch, dist, dist / ch))
print("L08 neg-disc corrected V1(s) with H=2, t=1:", V(S4, A4, f4, 1, 's', 2, r4, B4, F(-1)))
print("L08 neg-disc corrected: Theorem-1.3 check U0 = 0 != V0 = 1:", V(S4, A4, f4, 0, 's', 2, r4, B4, F(-1)))
