"""Independent L11 recheck: own sketch (integer capacities), own exact rank counts, unrounded excess/deficit."""
import random
from fractions import Fraction
from math import ceil, floor, log2

N, SEED = 5000, 2026
rng = random.Random(SEED)
xs = [rng.random() for _ in range(N)]
srt = sorted(xs)

def cap(h, eps):  # k_h = 2*ceil((h+1)(h+2)/(2 eps)) computed exactly with Fraction
    return 2 * ceil(Fraction((h + 1) * (h + 2)) / (2 * eps))

def run(eps):
    levels = []
    compactions = 0
    Ccount = {}
    for x in xs:
        cur = x; h = 0
        levels_items = levels
        # push x into level 0
        stack = [(0, x)]
        while stack:
            h, val = stack.pop()
            while len(levels) <= h:
                levels.append([])
            levels[h].append(val)
            k = cap(h, eps)
            if len(levels[h]) == k:
                buf = sorted(levels[h]); levels[h] = []
                compactions += 1; Ccount[h] = Ccount.get(h, 0) + 1
                for y in buf[1::2]:
                    stack.append((h + 1, y))
    weight = sum(len(b) * 2 ** h for h, b in enumerate(levels))
    stored = sum(len(b) for b in levels)
    pairs = sorted((v, 2 ** h) for h, b in enumerate(levels) for v in b)
    return levels, compactions, Ccount, weight, stored, pairs

def query(pairs, q):
    tgt = q * N; tot = 0
    for v, w in pairs:
        tot += w
        if tot >= tgt:
            return v

probes = [Fraction(0), Fraction(1, 100), Fraction(1, 10), Fraction(1, 4), Fraction(1, 2),
          Fraction(3, 4), Fraction(9, 10), Fraction(99, 100), Fraction(1)]
for eps in (Fraction(1, 20), Fraction(1, 10)):
    levels, comp, Cc, weight, stored, pairs = run(eps)
    caps = [cap(h, eps) for h in range(3)]
    excess = Fraction(0); deficit = Fraction(0); ok = True
    for q in probes:
        v = query(pairs, q)
        below = sum(1 for x in srt if x < v); atle = sum(1 for x in srt if x <= v)
        ok &= (below <= q * N + eps * N) and (atle >= q * N - eps * N)
        excess = max(excess, below - q * N); deficit = max(deficit, q * N - atle)
    print(f"eps {eps}: caps {caps} weight {weight} stored {stored} compactions {comp} per-level {Cc} "
          f"probes ok {ok} max excess/N {float(excess / N):.6f} max deficit/N {float(deficit / N)}")
    print("   bound per level 5000/(k_h 2^h):", [floor(Fraction(N, cap(h, eps) * 2 ** h)) for h in range(6)])
# Corollary sums
print("Cor 2.6 sum eps=1/20, L=12:", sum(cap(h, Fraction(1, 20)) - 1 for h in range(0, 13)))
print("Cor 2.6 sum eps=1/20, L=29 (n=1e9):", sum(cap(h, Fraction(1, 20)) - 1 for h in range(0, 30)))
print("formula L=29:", Fraction(30 * 31 * 32, 3) / Fraction(1, 20) + 30)
print("formula L=12:", Fraction(13 * 14 * 15, 3) / Fraction(1, 20) + 13)
print("floor log2 1e9 =", floor(log2(10**9)), " floor log2 5000 =", floor(log2(5000)))
