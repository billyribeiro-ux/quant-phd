"""Round-14 independent check of Theorems 1.5 and 2.3 and Lemma 2.2 (E3 L04), on exact random pairs.

Independent of the lab: random pairs are drawn with a different generator (Python random with seed 14),
FOSD/SOSD verdicts are computed from CDFs and integrated CDFs, and the expected-utility side uses a
random sample of nondecreasing (and nondecreasing concave) utilities on S, drawn from random nonnegative
increments and decreasing chord slopes, not the lab's witness set. Any disagreement is printed.
"""
import random
from fractions import Fraction

S = [1000, 2000, 3000, 4000, 5000]
rng = random.Random(14)

def rand_pmf(k_balls=6):
    c = [0] * len(S)
    for _ in range(k_balls):
        c[rng.randrange(len(S))] += 1
    return [Fraction(x, k_balls) for x in c]

def mean(p):
    return sum(pi * x for pi, x in zip(p, S))

def F(p, t):
    return sum(pi for pi, x in zip(p, S) if x <= t)

def I(p, t):
    return sum(pi * max(t - x, 0) for pi, x in zip(p, S))

def eu(p, u):
    return sum(pi * ui for pi, ui in zip(p, u))

def rand_nondecreasing(concave):
    if concave:
        slopes = sorted([rng.random() for _ in range(len(S) - 1)], reverse=True)
    else:
        slopes = [rng.random() for _ in range(len(S) - 1)]
    u = [rng.uniform(-3, 3)]
    for j, sl in enumerate(slopes):
        u.append(u[-1] + sl * (S[j + 1] - S[j]))
    return [Fraction(round(v * 1000), 1000) for v in u]  # exact rational values

def verdict_eu(p, q, utils):
    diffs = [eu(p, u) - eu(q, u) for u in utils]
    return (all(d >= 0 for d in diffs), all(d <= 0 for d in diffs))

fosd_mismatch = sosd_mismatch = integ_mismatch = 0
n_fosd = n_sosd = 0
checked = 0
for trial in range(400):
    p = rand_pmf()
    q = rand_pmf()
    # first-order
    x_dom = all(F(p, t) <= F(q, t) for t in S)
    y_dom = all(F(q, t) <= F(p, t) for t in S)
    utils = [rand_nondecreasing(False) for _ in range(400)]
    ex, ey = verdict_eu(p, q, utils)
    n_fosd += 1
    if x_dom != ex or (y_dom != ey):
        # EU side is a sample: it can only be weaker, so flag only when the sample refutes a proven dominance
        if x_dom and not ex:
            fosd_mismatch += 1
        if y_dom and not ey:
            fosd_mismatch += 1
    # second-order, equal means only
    if mean(p) == mean(q):
        n_sosd += 1
        ix = all(I(p, t) <= I(q, t) for t in S)
        iy = all(I(q, t) <= I(p, t) for t in S)
        cutils = [rand_nondecreasing(True) for _ in range(400)]
        cx, cy = verdict_eu(p, q, cutils)
        if ix and not cx:
            sosd_mismatch += 1
        if iy and not cy:
            sosd_mismatch += 1
        # Lemma 2.2 at all real t: check I(t) piecewise on a fine grid of t in [1000, 5000] step 50 cents
        grid = [Fraction(t) for t in range(900, 5101, 50)]
        ix_all = all(I(p, t) <= I(q, t) for t in grid)
        if ix_all != ix:
            integ_mismatch += 1
    checked += 1

print(f"pairs checked {checked}; FOSD pairs {n_fosd}; equal-mean pairs {n_sosd}")
print(f"proven FOSD dominance refuted by sampled nondecreasing utilities: {fosd_mismatch}")
print(f"proven SOSD dominance refuted by sampled nondecreasing concave utilities: {sosd_mismatch}")
print(f"support-point SOSD verdict differs from grid-of-t verdict (Lemma 2.2): {integ_mismatch}")

# Converse direction sample: when the EU side ranks, the CDF side must rank too (Theorem 1.5 'if')
conv_bad = 0
for trial in range(300):
    p = rand_pmf()
    q = rand_pmf()
    utils = [rand_nondecreasing(False) for _ in range(60)]
    ex, ey = verdict_eu(p, q, utils)
    if ex and not all(F(p, t) <= F(q, t) for t in S):
        conv_bad += 1
print(f"sampled nondecreasing utilities rank X above Y where F_X <= F_Y fails: {conv_bad}")

# Resolve the converse-sample cases with the exact witnesses 1{s > t} (Theorem 1.5 'if' direction):
resolved = 0
unresolved = 0
rng2 = random.Random(14)
rng = rng2
for trial in range(300):
    p = rand_pmf()
    q = rand_pmf()
    utils = [rand_nondecreasing(False) for _ in range(60)]
    ex, ey = verdict_eu(p, q, utils)
    if ex and not all(F(p, t) <= F(q, t) for t in S):
        witnesses = [[Fraction(1 if x > t else 0) for x in S] for t in S]
        wx, wy = verdict_eu(p, q, witnesses)
        if not wx:
            resolved += 1
        else:
            unresolved += 1
print(f"converse-sample cases resolved by exact indicator witnesses: {resolved}; unresolved: {unresolved}")
