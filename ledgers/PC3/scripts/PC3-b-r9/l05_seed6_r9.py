"""Verifier round 9 (PC3-b): independent recount of the L05 seed-6 numbers, written without the twin's code.

Counts: naive comparisons = window comparisons of the scan; deque comparisons = each test of the back index value
against the incoming value in the push loop; pops = removals from either end; pushes = appends.
"""

import random


def seq(seed: int, n: int) -> list[int]:
    r = random.Random(seed)
    return [r.randint(0, 999) for _ in range(n)]


def naive(xs: list[int], k: int) -> tuple[list[int], int]:
    out: list[int] = []
    cmp = 0
    for s in range(len(xs) - k + 1):
        m = xs[s]
        for v in xs[s + 1 : s + k]:
            cmp += 1
            m = max(m, v)
        out.append(m)
    return out, cmp


def dq(xs: list[int], k: int) -> tuple[list[int], int, int, int]:
    d: list[int] = []  # indices, values decreasing front to back
    out: list[int] = []
    cmp = pops = pushes = 0
    for i, v in enumerate(xs):
        while d:
            cmp += 1
            if xs[d[-1]] > v:
                break
            d.pop()
            pops += 1
        d.append(i)
        pushes += 1
        if d[0] == i - k:
            d.pop(0)
            pops += 1
        if i >= k - 1:
            out.append(xs[d[0]])
    return out, cmp, pops, pushes


for seed in (5, 6):
    xs = seq(seed, 200)
    a, ca = naive(xs, 8)
    b, cb, pp, pu = dq(xs, 8)
    print(f"seed {seed} k=8: equal {a == b}, naive {ca}, deque comparisons {cb}, pops {pp}, pushes {pu}")
