"""Round 3: small two-period and one-period examples in L07 and L08, recomputed by plan enumeration (exact)."""
from fractions import Fraction as F
from itertools import product

def plans(S, A, f, H, s0, t0=0):
    """All feasible action sequences from (t0, s0) of length H - t0."""
    res = []
    def rec(t, s, acc):
        if t == H:
            res.append(tuple(acc))
            return
        for a in A(s):
            rec(t + 1, f(s, a), acc + [(s, a)])
    rec(t0, s0, [])
    return res

# L07 M1-M3: states x,y; A(x)={u,v}, A(y)={w}; f(x,u)=y, f(x,v)=x, f(y,w)=y; r(x,u)=3, r(x,v)=5, r(y,w)=2; B(x)=0,B(y)=1; H=2
A7 = lambda s: {'x': ['u', 'v'], 'y': ['w']}[s]
f7 = lambda s, a: {('x', 'u'): 'y', ('x', 'v'): 'x', ('y', 'w'): 'y'}[(s, a)]
r7 = lambda s, a: {('x', 'u'): 3, ('x', 'v'): 5, ('y', 'w'): 2}[(s, a)]
B7 = {'x': 0, 'y': 1}
def total7(seq, s0):
    tot = 0; s = s0
    for (st, a) in seq:
        tot += r7(st, a); s = f7(st, a)
    return tot + B7[s]
allp = plans(None, A7, f7, 2, 'x')
print("L07 M3 plans from (0,x):", [(seq, total7(seq, 'x')) for seq in allp])
print("L07 M3 plans enumerated", len(allp), "max", max(total7(q, 'x') for q in allp))
# M1 values: V1(x)=max(3+B(y), 5+B(x)); V1(y)=2+B(y); V0(x)=max(3+V1(y),5+V1(x))
V1x = max(r7('x', a) + B7[f7('x', a)] for a in A7('x')); V1y = r7('y', 'w') + B7[f7('y', 'w')]
V0x = max(r7('x', a) + V1x*0 + (V1y if f7('x', a) == 'y' else V1x) for a in A7('x'))
print("L07 M1 V1(x)", V1x, "V1(y)", V1y, "V0(x)", V0x)
# L07 Remark 2.5: H=2, S={x,y}, A(x)={a,b}, A(y)={c}, f(x,a)=f(x,b)=y, f(y,c)=y, r(x,a)=0, r(x,b)=1, r(y,c)=0, B=0
A5 = lambda s: {'x': ['a', 'b'], 'y': ['c']}[s]
f5 = lambda s, a: 'y' if s == 'x' else 'y'
r5 = lambda s, a: {('x', 'a'): 0, ('x', 'b'): 1, ('y', 'c'): 0}[(s, a)]
p5 = plans(None, A5, f5, 2, 'x')
tot5 = lambda seq: sum(r5(st, a) for st, a in seq)
print("L07 Remark2.5 plans from (0,x):", [(seq, tot5(seq)) for seq in p5], "V0(x)", max(tot5(q) for q in p5))
# L07 R2: objective max_k r(s_k,a_k), H=2, S={s,x}, A(s)={a0}, A(x)={b,c}, f(s,a0)=x, f(x,b)=f(x,c)=x, r(s,a0)=10, r(x,b)=5, r(x,c)=3
A2 = lambda s: {'s': ['a0'], 'x': ['b', 'c']}[s]
f2 = lambda s, a: 'x'
r2 = lambda s, a: {('s', 'a0'): 10, ('x', 'b'): 5, ('x', 'c'): 3}[(s, a)]
p2 = plans(None, A2, f2, 2, 's')
print("L07 R2 plans from (0,s):", [(seq, max(r2(st, a) for st, a in seq)) for seq in p2])
print("L07 R2 from (1,x): one-period values", [(a, r2('x', a)) for a in ['b', 'c']])
# L07 lesson: V_1(400)=220 witness: 200,100,100 ; 240 witness 100 x4 (lab checked); binomial
from math import comb
print("C(8,4)", comb(8, 4))
# L07 E1 differences
print("E1 diffs", 240-220, 220-200, 200-130, 130-4)
print("E2 ratio 130/240", F(130, 240))
# L08 M1-M3 and negative-discount example (exact)
# M2/M3: states x,y; A(x)={a,b}, A(y)={c}; f(x,a)=y, f(x,b)=x, f(y,c)=y; r(x,a)=2, r(x,b)=1, r(y,c)=3; B=0; H=2; beta=1/2
beta = F(1, 2)
V1 = {'x': max(2, 1), 'y': 3}
V0 = {'x': max(2 + beta*V1['y'], 1 + beta*V1['x']), 'y': 3 + beta*V1['y']}
print("L08 M2 V1", V1, "V0", V0)
print("L08 M3 discounted total of (a,c) from x", F(2) + beta*3 + beta**2*0)
# negative discount example: H=2, one state, A={x,y}, r(x)=0, r(y)=1, B=0, beta=-1
bm = F(-1)
allp = [(a1, a2) for a1 in 'xy' for a2 in 'xy']
tots = {p: (0 if p[0]=='x' else 1) + bm*(0 if p[1]=='x' else 1) for p in allp}
print("negative-discount totals", tots, "V0", max(tots.values()))
V1n = max(0, 1); U0n = max(0 + bm*V1n, 1 + bm*V1n)
print("negative-discount U1", V1n, "U0 from Bellman", U0n)
# Remark 1.5 H=1: (U0,U1)=(1+c,c)
