"""Round 7 verifier: independent re-implementation of the L11 sketch (Definition 2.1) and checks of the page claims.
Stdlib only. Run with: .venv/bin/python -I ledgers/CS2/scripts/CS2-c-r7/l11_claims.py"""
import bisect
import math
import random
from fractions import Fraction


def cap(h, eps):
    return 2 * math.ceil(Fraction((h + 1) * (h + 2), 2) / eps)


class Sk:
    def __init__(self, eps):
        self.eps = eps
        self.levels = []
        self.n = 0
        self.comp = 0
        self.comp_by_level = {}

    def add(self, x):
        self.n += 1
        self.push(0, x)

    def push(self, h, x):
        while len(self.levels) <= h:
            self.levels.append([])
        buf = self.levels[h]
        buf.append(x)
        if len(buf) == cap(h, self.eps):
            buf.sort()
            kept = [buf[i] for i in range(len(buf)) if i % 2 == 1]  # 2nd, 4th, ... (1-based even)
            assert len(kept) == len(buf) // 2
            self.levels[h] = []
            self.comp += 1
            self.comp_by_level[h] = self.comp_by_level.get(h, 0) + 1
            for y in kept:
                self.push(h + 1, y)

    def stored(self):
        return sum(len(b) for b in self.levels)

    def weight(self):
        return sum(len(b) * 2 ** h for h, b in enumerate(self.levels))

    def query(self, q):
        pairs = sorted((v, 2 ** h) for h, b in enumerate(self.levels) for v in b)
        target = q * self.n
        cum = 0
        for v, w in pairs:
            cum += w
            if cum >= target:
                return v
        raise AssertionError("weight short")


def ranks(sorted_xs, v):
    return bisect.bisect_right(sorted_xs, v), bisect.bisect_left(sorted_xs, v)  # R(v), R^-(v)


# M3: 40 values, eps=1/10, k0=20
s = Sk(Fraction(1, 10))
for i in range(40):
    s.add(float(i))
print("M3 40 values: stored", s.stored(), "weight", s.weight(), "level sizes", [len(b) for b in s.levels], "comp", s.comp)
# E1: 39 values
s = Sk(Fraction(1, 10))
for i in range(39):
    s.add(float(i))
print("E1 39 values: stored", s.stored(), "weight", s.weight(), "level sizes", [len(b) for b in s.levels], "comp", s.comp, "E=sum C_h 2^h =", sum(c * 2 ** h for h, c in s.comp_by_level.items()))
# E2: compaction counts eps=1/20, n=5000 and per-level
rng = random.Random(2026)
xs = [rng.random() for _ in range(5000)]
s = Sk(Fraction(1, 20))
for x in xs:
    s.add(x)
print("eps1/20 n5000: stored", s.stored(), "comp", s.comp, "per level", dict(sorted(s.comp_by_level.items())), "weight", s.weight())
s2 = Sk(Fraction(1, 10))
for x in xs:
    s2.add(x)
print("eps1/10 n5000: stored", s2.stored(), "comp", s2.comp, "weight", s2.weight())
# stored count depends only on n and eps: try 5 seeds at eps=1/20
for seed in range(5):
    r = random.Random(seed)
    t = Sk(Fraction(1, 20))
    for _ in range(5000):
        t.add(r.random())
    print("seed", seed, "stored", t.stored(), "comp", t.comp)
# R3 / corollary closed forms
print("R3 sum k_h-1, eps=1/20, L=12:", sum(cap(h, Fraction(1, 20)) - 1 for h in range(13)))
print("closed form L=12:", Fraction(13 * 14 * 15, 3) / Fraction(1, 20) + 13, float(Fraction(13 * 14 * 15, 3) / Fraction(1, 20) + 13))
print("closed form L=29 (n=1e9):", Fraction(30 * 31 * 32, 3) / Fraction(1, 20) + 30, " floor(log2 1e9)=", int(math.log2(10**9)))
print("k_h eps=1/20 h=0..4:", [cap(h, Fraction(1, 20)) for h in range(5)], " eps=1/10 h=0..2:", [cap(h, Fraction(1, 10)) for h in range(3)])
# Section 3 example: values 1..1000, q=1/2, eps=1/20
ex = [float(i) for i in range(1, 1001)]
for v in (500, 501, 450, 1000):
    R, Rm = ranks(ex, v)
    print("1..1000 v", v, "R", R, "R^-", Rm, "eps=1/20 ineq:", Rm <= 500 + 50, R >= 500 - 50, " eps=0 ineq:", Rm <= 500, R >= 500)
# Misconception 2: 500 zeros, 500 thousands
two = [0.0] * 500 + [1000.0] * 500
allok = True
for v in [i * 0.5 for i in range(0, 2001)]:
    R, Rm = ranks(two, v)
    if not (Rm <= 500 and R >= 500):
        allok = False
        print("eps0 fails at", v)
        break
print("every v in [0,1000] satisfies eps=0 ineqs (grid step 0.5):", allok)
R, Rm = ranks(two, 1000.0)
print("R^-(1000)", Rm, "R(1000)", R, "allowed eps=1/20:", Rm <= 550 and R >= 450)
