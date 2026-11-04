import random
from fractions import Fraction as F
SUP = (1000, 2000, 3000, 4000, 5000)
def mean(p): return sum(q * x for q, x in zip(p, SUP))
def icdf(p, t): return sum(q * max(t - x, 0) for q, x in zip(p, SUP))
def draw(rng):
    c = [0] * 5
    for _ in range(12): c[rng.randrange(5)] += 1
    return tuple(F(k, 12) for k in c)
def shift_up(p, rng):
    st = F(1, 12); el = [i for i in range(4) if p[i] >= st]
    if not el: return None
    i = rng.choice(el); j = rng.randrange(i + 1, 5); q = list(p); q[i] -= st; q[j] += st
    return tuple(q)
def match_mean(p, target):
    mv = (target - mean(p)) / 4000; q = list(p)
    if mv >= 0:
        if q[0] < mv: return None
        q[0] -= mv; q[-1] += mv
    else:
        m = -mv
        if q[-1] < m: return None
        q[-1] -= m; q[0] += m
    return tuple(q)
rng = random.Random(20261028); kinds = ("shift", "equal-mean", "random"); pairs = []
while len(pairs) < 24:
    k = kinds[len(pairs) % 3]; px = draw(rng)
    if k == "shift": py = shift_up(px, rng)
    elif k == "equal-mean": py = match_mean(draw(rng), mean(px))
    else: py = draw(rng)
    if py is not None: pairs.append((k, px, py))
for n, (k, px, py) in enumerate(pairs):
    if mean(px) == mean(py):
        ix = [icdf(px, t) for t in SUP]; iy = [icdf(py, t) for t in SUP]
        a = all(u <= v for u, v in zip(ix, iy)); b = all(v <= u for u, v in zip(ix, iy))
        v = "identical" if a and b else "X dominates Y" if a else "Y dominates X" if b else "no ranking"
        print(n, k, v)
