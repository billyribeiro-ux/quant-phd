"""Independent re-derivation of the L11 numbers (CS2-c r3): sketch written from Definition 2.1 wording, not the twin's code."""
import math, random, bisect
from fractions import Fraction as F

def cap(h, eps):
    return 2 * math.ceil(F((h + 1) * (h + 2)) / (2 * eps))

class Sk:
    def __init__(self, eps):
        self.eps = eps; self.lv = []; self.C = {}; self.n = 0
    def _push(self, h, y):
        while len(self.lv) <= h: self.lv.append([])
        self.lv[h].append(y)
        k = cap(h, self.eps)
        if len(self.lv[h]) == k:
            srt = sorted(self.lv[h]); kept = [srt[i] for i in range(1, k, 2)]  # 2nd,4th,...,k-th (1-based)
            self.lv[h] = []; self.C[h] = self.C.get(h, 0) + 1
            for z in kept: self._push(h + 1, z)
    def add(self, x):
        self.n += 1; self._push(0, x)
    def stored(self): return sum(len(b) for b in self.lv)
    def weight(self): return sum(len(b) * 2 ** h for h, b in enumerate(self.lv))
    def items(self): return [(v, 2 ** h) for h, b in enumerate(self.lv) for v in b]
    def query(self, q):
        it = sorted(self.items()); tot = 0
        for v, w in it:
            tot += w
            if tot >= q * self.n: return v
        raise RuntimeError

print("capacities eps=1/20:", [cap(h, F(1,20)) for h in range(3)], " eps=1/10:", [cap(h, F(1,10)) for h in range(3)])
print("k0..k4 for eps=1/20:", [cap(h, F(1,20)) for h in range(5)])
for eps in (F(1, 20), F(1, 10)):
    rng = random.Random(2026)
    xs = [rng.random() for _ in range(5000)]
    sk = Sk(eps)
    for x in xs: sk.add(x)
    ordered = sorted(xs)
    print("eps", eps, "stored", sk.stored(), "compactions", sum(sk.C.values()), "per-level", dict(sorted(sk.C.items())), "weight==n", sk.weight() == 5000)
    probes = [F(0), F(1,100), F(1,10), F(1,4), F(1,2), F(3,4), F(9,10), F(99,100), F(1)]
    exc = F(0); dfc = F(0); ok = True
    for q in probes:
        v = sk.query(q)
        below = bisect.bisect_left(ordered, v); le = bisect.bisect_right(ordered, v)
        ok &= (below <= q*5000 + eps*5000) and (le >= q*5000 - eps*5000)
        exc = max(exc, F(below) - q*5000); dfc = max(dfc, q*5000 - F(le))
    print("   all probes pass", ok, "excess/N", round(float(exc/5000), 4), "deficit/N", round(float(dfc/5000), 4))
    # per-level bounds C_h <= n/(k_h 2^h)
    print("   per-level bounds floor(5000/(k_h 2^h)):", [5000 // (cap(h, eps) * 2 ** h) for h in range(6)])

# closed forms
print("R3 exact sum:", sum(cap(h, F(1,20)) - 1 for h in range(13)), " closed form+13:", (13*14*15)/(3*(1/20)) + 13, " L=29 closed:", (30*31*32)/(3*(1/20)) + 30)
print("n=5000 log2 floor:", math.floor(math.log2(5000)), " n=1e9 floor log2:", math.floor(math.log2(10**9)))
# M2 query check
print("M2 weights total", 1+2+4, "qn", F(7,2))
# M3: 40 values eps=1/10
s = Sk(F(1,10))
for i in range(40): s.add(float(i))
print("M3 level sizes", [len(b) for b in s.lv], "weight", s.weight(), "C", s.C)
# E1: 39 values eps=1/10
s = Sk(F(1,10))
for i in range(39): s.add(float(i))
print("E1 level sizes", [len(b) for b in s.lv], "stored", s.stored(), "weight", s.weight(), "E", sum(c*2**h for h,c in s.C.items()), "eps n", F(1,10)*39, float(F(1,10)*39))
# E2 claim: sum of level bounds = 151
print("E2 level-bound sum", sum(5000 // (cap(h, F(1,20))*2**h) for h in range(20)))
# Section 3 example
print("S3 v=450:", 449 <= 550 and 450 >= 450, " v=501 eps0:", 500 <= 500 and 501 >= 500)
# misconception 2: 500 zeros 500 thousands
print("M-2: R^-(1000)=500<=550", 500<=550, "R(1000)=1000>=450", 1000>=450)
# R1: E/n bound check example not needed
