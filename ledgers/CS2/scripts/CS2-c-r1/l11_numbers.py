"""Recompute L11 prose numbers, the sketch guarantee, per-level compaction counts and the Corollary 2.6 sums (CS2 slice c r1)."""
import bisect
import math
import random
from fractions import Fraction

N = 5000
SEED = 2026
EPS = (Fraction(1, 20), Fraction(1, 10))
PROBES = (Fraction(0), Fraction(1, 100), Fraction(1, 10), Fraction(1, 4), Fraction(1, 2),
          Fraction(3, 4), Fraction(9, 10), Fraction(99, 100), Fraction(1))


def cap(h, eps):
    return 2 * math.ceil(Fraction((h + 1) * (h + 2), 2) / eps)


class Sk:
    def __init__(self, eps):
        self.eps = eps
        self.levels = []
        self.n = 0
        self.per_level = {}

    def add(self, x):
        self.n += 1
        self.push(0, x)

    def push(self, h, x):
        while len(self.levels) <= h:
            self.levels.append([])
        b = self.levels[h]
        b.append(x)
        if len(b) == cap(h, self.eps):
            b.sort()
            kept = b[1::2]
            self.levels[h] = []
            self.per_level[h] = self.per_level.get(h, 0) + 1
            for y in kept:
                self.push(h + 1, y)

    def stored(self):
        return sum(len(b) for b in self.levels)

    def weight(self):
        return sum(len(b) * 2 ** h for h, b in enumerate(self.levels))

    def query(self, q):
        pairs = sorted((v, 2 ** h) for h, b in enumerate(self.levels) for v in b)
        t = q * self.n
        cum = 0
        for v, w in pairs:
            cum += w
            if cum >= t:
                return v
        raise AssertionError


def run(xs, eps):
    sk = Sk(eps)
    for x in xs:
        sk.add(x)
    ordered = sorted(xs)
    ex = Fraction(0)
    de = Fraction(0)
    ok = True
    for q in PROBES:
        v = sk.query(q)
        below = bisect.bisect_left(ordered, v)
        le = bisect.bisect_right(ordered, v)
        ok &= below <= q * N + eps * N and le >= q * N - eps * N
        ex = max(ex, Fraction(below) - q * N)
        de = max(de, q * N - Fraction(le))
    return sk, ok, float(ex / N), float(de / N)


rng = random.Random(SEED)
xs = [rng.random() for _ in range(N)]
for eps in EPS:
    sk, ok, ex, de = run(xs, eps)
    total = sum(sk.per_level.values())
    print(f"eps {eps}: pass={ok} stored={sk.stored()} weight={sk.weight()} compactions={total} per_level={dict(sorted(sk.per_level.items()))}")
    print(f"   largest excess/N={ex!r} (print .4f -> {ex:.4f}); deficit/N={de!r}; eps={float(eps)}")
    print(f"   capacities k0..k4 = {[cap(h, eps) for h in range(5)]}")
    bound_counts = [math.floor(Fraction(N, cap(h, eps) * 2 ** h)) for h in range(40)]
    print(f"   floor bounds per level = {bound_counts[:8]} sum={sum(bound_counts)}")
    # Corollary 2.6 sum
    L = int(math.floor(math.log2(N)))
    cor = sum(cap(h, eps) - 1 for h in range(L + 1))
    print(f"   Corollary 2.6 sum for n={N}, L={L}: {cor}")
    closed = Fraction((L + 1) * (L + 2) * (L + 3), 3) / eps + (L + 1)
    print(f"   closed form bound (L+1)(L+2)(L+3)/(3eps)+(L+1) = {closed}")

# Independence of stored count and compactions from the values (claimed on page: depends only on n and eps)
for label, ys in (("sorted", sorted(xs)), ("reversed", sorted(xs, reverse=True)), ("seed7", [random.Random(7).random() for _ in range(N)])):
    sk, ok, ex, de = run(ys, Fraction(1, 20))
    print(f"stream {label}: pass={ok} stored={sk.stored()} compactions={sum(sk.per_level.values())} excess={ex:.4f} deficit={de:.4f}")

# Closed form at n = 10^9
L9 = int(math.floor(math.log2(10**9)))
print("L for 1e9 =", L9, "closed form =", Fraction((L9 + 1) * (L9 + 2) * (L9 + 3), 3) / Fraction(1, 20) + (L9 + 1))
# Problem R3: sum_{h=0}^{12} (20(h+1)(h+2)-1)
print("R3 sum =", sum(20 * (h + 1) * (h + 2) - 1 for h in range(13)), " 20*910-13 =", 20 * 910 - 13)
