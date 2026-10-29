"""Round-7: recompute the L09 Lab 1 numbers quoted by cards c123-c126 (independent of the twin's main())."""

import random
from fractions import Fraction

N, SEED = 2000, 90
for offset in (0.0, 1e6, 1e9):
    rng = random.Random(SEED)
    xs = [offset + rng.random() for _ in range(N)]
    fr = [Fraction(x) for x in xs]
    mean = sum(fr, Fraction(0)) / N
    exact = sum(((x - mean) ** 2 for x in fr), Fraction(0)) / (N - 1)
    count, m, s = 0, 0.0, 0.0
    for x in xs:
        count += 1
        d = x - m
        m += d / count
        s += d * (x - m)
    welford = s / (count - 1)
    print(f"offset {offset:g}: exact {float(exact):.10f} exact_full {float(exact):.12e}")
    print(f"   welford {welford:.12e} rel {float(abs(Fraction(welford) - exact) / exact):.4e}")
