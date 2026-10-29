"""Independent recomputation for L10 and L11 (verifier round 1, slice c)."""
import random
import math
from fractions import Fraction
from collections import deque

# ---------- L10: independent deque implementation + brute force, op counts
def roll_check(series, w):
    # independent: index-based deque, min and max, counts ops
    res = {}
    for kind in ("min", "max"):
        dq = deque()
        ops = 0
        largest_push_removals = 0
        largest_size = 0
        out = []
        for i, x in enumerate(series):
            rem = 0
            if kind == "min":
                while dq and series[dq[-1]] >= x:
                    dq.pop(); rem += 1
            else:
                while dq and series[dq[-1]] <= x:
                    dq.pop(); rem += 1
            dq.append(i)
            while dq[0] <= i - w:
                dq.popleft(); rem += 1
            ops += 1 + rem
            largest_push_removals = max(largest_push_removals, rem)
            largest_size = max(largest_size, len(dq))
            out.append(series[dq[0]])
        res[kind] = (out, ops, largest_push_removals, largest_size)
    return res

def brute(series, i, w, kind):
    seg = series[max(0, i - w + 1): i + 1]
    return min(seg) if kind == "min" else max(seg)

rng = random.Random(1010)
series = [rng.randint(0, 999) for _ in range(200)]
for w in (1, 2, 5, 13, 30):
    r = roll_check(series, w)
    for kind in ("min", "max"):
        out, ops, lpr, ls = r[kind]
        assert out == [brute(series, i, w, kind) for i in range(200)], (w, kind)
    print("L10 w=%d min ops %d max ops %d largest push removals %d largest size %d" % (
        w, r["min"][1], r["max"][1], max(r["min"][2], r["max"][2]), max(r["min"][3], r["max"][3])))

# hand-check M1/M2/M3 of L10
print("L10 M1 rolling min", [min([3,1,4,1,5][max(0,i-2):i+1]) for i in range(5)])

# E1: w=1 gives 2n-1 for any series (random tests)
for trial in range(50):
    s = [random.Random(trial).randint(0, 9) for _ in range(37)]
    r = roll_check(s, 1)
    assert r["min"][1] == 2 * 37 - 1 and r["max"][1] == 2 * 37 - 1, trial
print("L10 E1 2n-1 holds on 50 random series with n=37 (both kinds)")

# E2 witness
r = roll_check([1, 2, 3, 4, 5, 0], 5)
print("L10 E2 largest push removals", r["min"][2])
# E3 decreasing
r = roll_check([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], 4)
print("L10 E3 decreasing min ops", r["min"][1], "expected 2n-1 = 19")
# R3 expiry count: increasing series n=10 w=3 -> expiry removals n-w=7
def expiry_count(series, w):
    dq = deque(); exp = 0
    for i, x in enumerate(series):
        while dq and series[dq[-1]] >= x: dq.pop()
        dq.append(i)
        while dq[0] <= i - w:
            dq.popleft(); exp += 1
    return exp
print("L10 R3 expiry increasing n=10 w=3:", expiry_count(list(range(10)), 3), "expected 7")
# R3 ops with two windows
# Worst-case series: check Corollary (c) example for w=5..
# Misconception 1: largest push removal for w=5 on the lab series = 5 (from above)

# ---------- L11
def caps(eps):
    return lambda h: 2 * math.ceil(Fraction((h + 1) * (h + 2), 2) / eps)

class Sk:
    def __init__(self, eps):
        self.cap = caps(eps); self.levels = []; self.n = 0; self.comp = {}
    def add(self, x):
        self.n += 1; self.push(0, x)
    def push(self, h, x):
        while len(self.levels) <= h: self.levels.append([])
        b = self.levels[h]; b.append(x)
        if len(b) == self.cap(h):
            b.sort()
            kept = b[1::2]
            self.levels[h] = []
            self.comp[h] = self.comp.get(h, 0) + 1
            for y in kept: self.push(h + 1, y)
    def weight(self):
        return sum(len(b) * 2 ** h for h, b in enumerate(self.levels))
    def stored(self):
        return sum(len(b) for b in self.levels)
    def answer(self, q):
        pairs = sorted((v, 2 ** h) for h, b in enumerate(self.levels) for v in b)
        tgt = q * self.n; c = 0
        for v, w in pairs:
            c += w
            if c >= tgt: return v
        raise AssertionError

N = 5000
r = random.Random(2026)
xs = [r.random() for _ in range(N)]
srt = sorted(xs)
import bisect
for eps in (Fraction(1, 20), Fraction(1, 10)):
    sk = Sk(eps)
    for x in xs: sk.add(x)
    print("L11 eps", eps, "stored", sk.stored(), "weight", sk.weight(), "compactions per level", dict(sorted(sk.comp.items())),
          "total", sum(sk.comp.values()), "caps", [sk.cap(h) for h in range(3)])
    print("   per-level bound n/(k_h 2^h) floors:", [math.floor(N / (sk.cap(h) * 2 ** h)) for h in range(6)])
    worst_ex = Fraction(0); worst_def = Fraction(0); ok = True
    for q in [Fraction(0), Fraction(1,100), Fraction(1,10), Fraction(1,4), Fraction(1,2), Fraction(3,4), Fraction(9,10), Fraction(99,100), Fraction(1)]:
        v = sk.answer(q)
        below = bisect.bisect_left(srt, v); le = bisect.bisect_right(srt, v)
        ok &= below <= q * N + eps * N and le >= q * N - eps * N
        worst_ex = max(worst_ex, Fraction(below) - q * N)
        worst_def = max(worst_def, q * N - Fraction(le))
    print("   all pass", ok, "excess/N", float(worst_ex / N), "deficit/N", float(worst_def / N))

# R3 memory bound
k = lambda h: 20 * (h + 1) * (h + 2)
print("L11 R3 bound", sum(k(h) - 1 for h in range(0, 13)), "floor log2 5000", int(math.log2(5000)))
# E1 39 values eps 1/10
sk = Sk(Fraction(1, 10))
for x in xs[:39]: sk.add(x)
print("L11 E1 39 values: stored", sk.stored(), "weight", sk.weight(), "comp", sk.comp)
# M3 40 values
sk = Sk(Fraction(1, 10))
for x in xs[:40]: sk.add(x)
print("L11 M3 40 values: levels", [len(b) for b in sk.levels], "weight", sk.weight())
# canon: 1..1000 example, q=1/2 eps=1/20, median-like checks
for v in (500, 501, 450, 400):
    R_minus = v - 1; R = v
    print("canon v=%d R^-=%d R=%d  eps0-ok=%s eps1/20-ok=%s" % (v, R_minus, R, R_minus <= 500 and R >= 500, R_minus <= 550 and R >= 450))
# misconception 2
print("misc2: v=1000 R^-=500 <=550:", 500 <= 550, "R=1000>=450:", 1000 >= 450)
