# Independent recomputation of L07 lab numbers and the L07 worked examples touched by the delta.
import itertools
H = 4
G = (0, 100, 200, 300, 400)
R = {0: 0, 100: 60, 200: 100, 300: 120, 400: 130}
V = {H: {w: w // 100 for w in G}}
for t in range(H - 1, -1, -1):
    V[t] = {w: max(R[c] + V[t + 1][w - c] for c in G if c <= w) for w in G}
for t in range(H + 1):
    print('t', t, [V[t][w] for w in G])
cnt = 0; ok = True
for t in range(H):
    for w in G:
        best = None
        for seq in itertools.product(G, repeat=H - t):
            ww = w; tot = 0; feas = True
            for c in seq:
                if c > ww: feas = False; break
                tot += R[c]; ww -= c
            if not feas: continue
            cnt += 1
            tot += ww // 100
            best = tot if best is None or tot > best else best
        ok = ok and best == V[t][w]
best400 = None; n400 = 0
for seq in itertools.product(G, repeat=H):
    ww = 400; tot = 0; feas = True
    for c in seq:
        if c > ww: feas = False; break
        tot += R[c]; ww -= c
    if feas:
        n400 += 1
print('brute ok', ok, 'feasible sequences from (0,400) =', n400)
# greedy plan 400,0,0,0 from (0,400)
g = [400, 0, 0, 0]; w = 400; tot = 0
for c in g:
    tot += R[c]; w -= c
tot += w // 100
print('greedy total', tot)
# tails of greedy from t=1,2,3 optimal from the state reached
path = [400]
for c in g: path.append(path[-1] - c)
for k in range(1, H):
    wk = path[k]
    tail = sum(R[c] for c in g[k:]) + path[H] // 100
    print('greedy tail from', k, 'wealth', wk, 'tail total', tail, 'V', V[k][wk], 'optimal', tail == V[k][wk])
# optimal plan from (0,400)
print('V0(400)', V[0][400], 'W400 column', [V[t][400] for t in range(H + 1)])
print('E1 diffs', [V[t][400] - V[t + 1][400] for t in range(4)])
print('E2 ratio', round(130 / 240, 4), 130 / 240)
from math import comb
print('C(8,4)', comb(8, 4))
