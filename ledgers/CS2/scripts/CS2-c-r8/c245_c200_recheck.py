"""CS2-c-r8 independent recheck of CS2-c245 numbers and CS2-c200 / Definition 2.1 algebra.

Standard library only. Independent of tests/labs/CS2/lab-CS2-L11-1.py: a different
loop structure, and exact counts by a linear scan instead of bisect.
"""

from __future__ import annotations

import random
from fractions import Fraction

N = 5000
SEED = 2026
EPSILONS = (Fraction(1, 20), Fraction(1, 10))
PROBES = [Fraction(0), Fraction(1, 100), Fraction(1, 10), Fraction(1, 4), Fraction(1, 2),
          Fraction(3, 4), Fraction(9, 10), Fraction(99, 100), Fraction(1)]


def capacity(h: int, eps: Fraction) -> int:
    # Definition 2.1: k_h = 2 * ceil((h+1)(h+2) / (2 eps))
    m = Fraction((h + 1) * (h + 2), 2) / eps
    c = -(-m.numerator // m.denominator)
    return 2 * c


def run(xs: list[float], eps: Fraction) -> tuple[list[list[float]], int]:
    # Definition 2.1 as written: a full level is sorted, its 2nd, 4th, ... items are pushed
    # into level h+1 in order, and each push may itself trigger a compaction before the next push.
    levels: list[list[float]] = []
    counter = [0]

    def push(h: int, y: float) -> None:
        while len(levels) <= h:
            levels.append([])
        buf = levels[h]
        buf.append(y)
        if len(buf) == capacity(h, eps):
            buf.sort()
            kept = buf[1::2]
            levels[h] = []
            counter[0] += 1
            for z in kept:
                push(h + 1, z)

    for x in xs:
        push(0, x)
    return levels, counter[0]


def quantile(levels: list[list[float]], q: Fraction, n: int) -> float:
    items = sorted((v, 2**h) for h, buf in enumerate(levels) for v in buf)
    total = 0
    target = q * n
    for v, w in items:
        total += w
        if total >= target:
            return v
    raise AssertionError("weight short")


def main() -> None:
    rng = random.Random(SEED)
    xs = [rng.random() for _ in range(N)]
    for eps in EPSILONS:
        levels, comp = run(xs, eps)
        total_w = sum(len(b) * 2**h for h, b in enumerate(levels))
        assert total_w == N, total_w
        worst_ex = Fraction(0)
        worst_de = Fraction(0)
        all_ok = True
        for q in PROBES:
            v = quantile(levels, q, N)
            below = sum(1 for x in xs if x < v)
            le = sum(1 for x in xs if x <= v)
            ok = below <= q * N + eps * N and le >= q * N - eps * N
            all_ok = all_ok and ok
            worst_ex = max(worst_ex, Fraction(below) - q * N)
            worst_de = max(worst_de, q * N - Fraction(le))
        print(f"eps {eps}: probes {len(PROBES)} all_pass={all_ok} compactions={comp} "
              f"excess/N={float(worst_ex / N):.4f} deficit/N={float(worst_de / N):.4f} "
              f"excess<eps*N:{worst_ex < eps * N} deficit<eps*N:{worst_de < eps * N}")
    # CS2-c200 algebra: k_h >= (h+1)(h+2)/eps, and sum_{h<=H} 1/((h+1)(h+2)) < 1
    for eps in EPSILONS:
        ok = all(Fraction(capacity(h, eps)) >= Fraction((h + 1) * (h + 2)) / eps for h in range(200))
        print(f"eps {eps}: k_h >= (h+1)(h+2)/eps for h in 0..199: {ok}")
    partial = Fraction(0)
    ok_lemma = True
    for H in range(200):
        partial += Fraction(1, (H + 1) * (H + 2))
        ok_lemma = ok_lemma and partial == 1 - Fraction(1, H + 2) and partial < 1
    print(f"Lemma 2.3 identity and bound for H in 0..199: {ok_lemma}")


main()
