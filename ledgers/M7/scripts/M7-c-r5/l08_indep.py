# Independent recomputation of L08 Lab 1 numbers, and examples in L08 sections 1, 3 and problems.
from fractions import Fraction as F
import itertools
b = F(9, 10)
P = {0: 6, 1: 4, 2: 1}
def rew(s, a): return F(P[s]) if a == 'run' else F(-4)
def nxt(s, a): return min(s + 1, 2) if a == 'run' else 0
H = 6
V = {H: {s: F(0) for s in range(3)}}
for t in range(H - 1, -1, -1):
    V[t] = {}
    for s in range(3):
        V[t][s] = max(rew(s, a) + b * V[t + 1][nxt(s, a)] for a in ('run', 'repair'))
for t in range(H + 1):
    print('t', t, [f"{float(V[t][s]):.6f}" for s in range(3)], [str(V[t][s]) for s in range(3)])
# ties
ties = 0
for t in range(H):
    for s in range(3):
        c = [rew(s, a) + b * V[t + 1][nxt(s, a)] for a in ('run', 'repair')]
        if c[0] == c[1]: ties += 1
print('ties', ties)
# plans enumerated and brute force
cnt = 0; ok = True
for t in range(H):
    for s in range(3):
        best = None
        for plan in itertools.product(('run', 'repair'), repeat=H - t):
            cnt += 1
            st = s; tot = F(0); w = F(1)
            for a in plan:
                tot += w * rew(st, a); w *= b; st = nxt(st, a)
            best = tot if best is None or tot > best else best
        ok = ok and best == V[t][s]
print('plans', cnt, 'brute ok', ok)
# value iteration changes
U = {s: F(0) for s in range(3)}
for n in range(6):
    NU = {s: max(rew(s, a) + b * U[nxt(s, a)] for a in ('run', 'repair')) for s in range(3)}
    print('n', n, 'change', float(max(abs(NU[s] - U[s]) for s in range(3))), str(max(abs(NU[s] - U[s]) for s in range(3))))
    U = NU
# policy at each t for state 2
for t in range(H):
    print('pol', t, [max(('run', 'repair'), key=lambda a: rew(s, a) + b * V[t + 1][nxt(s, a)]) for s in range(3)])
# Section 3 example beta=-1, H=2
bb = F(-1)
tots = []
for p in itertools.product(('a', 'b'), repeat=2):
    r = {'a': F(0), 'b': F(1)}
    tots.append(r[p[0]] + bb * r[p[1]])
print('beta=-1 totals', [str(x) for x in tots], 'max', max(tots))
# M2 example
bh = F(1, 2)
V1x = max(F(2), F(1)); V1y = F(3)
V0x = max(F(2) + bh * V1y, F(1) + bh * V1x); V0y = F(3) + bh * V1y
print('M2', V1x, V1y, V0x, V0y, 'M3', F(2) + bh * F(3) + bh**2 * 0)
# Remark 1.5 check: (1+c, c) satisfies U0 = 1 + U1
print('R1 check beta=-1 example V1', max(F(0), F(1)))
