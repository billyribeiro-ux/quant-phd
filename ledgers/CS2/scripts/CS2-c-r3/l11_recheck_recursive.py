"""Same as l11_recheck.py but pushes kept items recursively in order, as Definition 2.1(2) states."""
import random
import sys
from fractions import Fraction
from math import ceil

N, SEED = 5000, 2026
rng = random.Random(SEED)
xs = [rng.random() for _ in range(N)]
srt = sorted(xs)
levels = []
comp = [0]

def cap(h, eps):
    return 2 * ceil(Fraction((h + 1) * (h + 2)) / (2 * eps))

def push(h, y, eps):
    while len(levels) <= h:
        levels.append([])
    levels[h].append(y)
    if len(levels[h]) == cap(h, eps):
        buf = sorted(levels[h]); levels[h] = []
        comp[0] += 1
        for z in buf[1::2]:
            push(h + 1, z, eps)

def query(pairs, q):
    tgt = q * N; tot = 0
    for v, w in pairs:
        tot += w
        if tot >= tgt:
            return v

probes = [Fraction(0), Fraction(1, 100), Fraction(1, 10), Fraction(1, 4), Fraction(1, 2),
          Fraction(3, 4), Fraction(9, 10), Fraction(99, 100), Fraction(1)]
for eps in (Fraction(1, 20), Fraction(1, 10)):
    levels.clear(); comp[0] = 0
    for x in xs:
        push(0, x, eps)
    weight = sum(len(b) * 2 ** h for h, b in enumerate(levels))
    stored = sum(len(b) for b in levels)
    pairs = sorted((v, 2 ** h) for h, b in enumerate(levels) for v in b)
    excess = Fraction(0); deficit = Fraction(0)
    for q in probes:
        v = query(pairs, q)
        below = sum(1 for x in srt if x < v); atle = sum(1 for x in srt if x <= v)
        excess = max(excess, below - q * N); deficit = max(deficit, q * N - atle)
    print(f"eps {eps}: weight {weight} stored {stored} compactions {comp[0]} "
          f"max excess/N {float(excess / N):.6f} max deficit/N {float(deficit / N):.6f}")
