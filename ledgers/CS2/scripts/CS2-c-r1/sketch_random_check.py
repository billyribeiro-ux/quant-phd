"""Random check of L11 Theorems 2.2, 2.4, 2.5 and the R2 odd-position variant; plus the E bound (verifier round 1)."""
import random, math, bisect
from fractions import Fraction as F

def cap(h, eps):
    return 2 * math.ceil(F((h + 1) * (h + 2), 2) / eps)

class Sk:
    def __init__(self, eps, keep_odd=False):
        self.eps = eps; self.levels = []; self.n = 0; self.E = 0; self.keep_odd = keep_odd
    def add(self, x):
        self.n += 1; self.push(0, x)
    def push(self, h, x):
        while len(self.levels) <= h: self.levels.append([])
        b = self.levels[h]; b.append(x)
        if len(b) == cap(h, self.eps):
            b.sort()
            kept = b[0::2] if self.keep_odd else b[1::2]
            self.levels[h] = []
            self.E += 2 ** h
            for y in kept: self.push(h + 1, y)
    def weight(self):
        return sum(len(b) * 2 ** h for h, b in enumerate(self.levels))
    def answer(self, q):
        pairs = sorted((v, 2 ** h) for h, b in enumerate(self.levels) for v in b)
        tgt = q * self.n; c = 0
        for v, w in pairs:
            c += w
            if c >= tgt: return v

fails = dict(weight=0, E=0, guarantee_even=0, guarantee_odd=0)
for t in range(200):
    r = random.Random(t)
    eps = F(r.randint(1, 9), 20)
    n = r.randint(1, 1500)
    xs = [r.randint(0, 50) for _ in range(n)]  # ties on purpose
    for keep_odd in (False, True):
        sk = Sk(eps, keep_odd)
        for x in xs: sk.add(x)
        if sk.weight() != n: fails["weight"] += 1
        if sk.E > eps * n: fails["E"] += 1
        srt = sorted(xs)
        for q in [F(0), F(1, 3), F(1, 2), F(4, 5), F(1)]:
            v = sk.answer(q)
            below = bisect.bisect_left(srt, v); le = bisect.bisect_right(srt, v)
            ok = below <= q * n + eps * n and le >= q * n - eps * n
            if not ok:
                fails["guarantee_odd" if keep_odd else "guarantee_even"] += 1
print("failures over 200 random streams with ties:", fails)
