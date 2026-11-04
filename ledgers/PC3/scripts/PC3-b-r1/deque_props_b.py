"""Verifier PC3-b round 1: property check of the L05 pseudocode (Definition 3.1 / Proposition 3.2 / 3.3) and of the
quiz claim that the front is the LAST occurrence of the window maximum. Independent of the lab twin.
Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r1/deque_props_b.py
"""
from __future__ import annotations

import random
from collections import deque


def pseudo(x: list[int], k: int) -> tuple[list[int], int, int]:
    """The L05 pseudocode, 1-indexed positions, returns outputs, comparison tests, and appends+removals."""
    n = len(x)
    xi = [0] + x  # 1-indexed
    dq: deque[int] = deque()
    out: list[int] = []
    tests = 0
    ops = 0
    fronts: list[int] = []
    for i in range(1, n + 1):
        while dq:
            tests += 1
            if xi[dq[-1]] <= xi[i]:
                dq.pop()
                ops += 1
            else:
                break
        dq.append(i)
        ops += 1
        if dq[0] <= i - k:
            dq.popleft()
            ops += 1
        if i >= k:
            out.append(xi[dq[0]])
            fronts.append(dq[0])
    return out, tests, ops


def brute(x: list[int], k: int) -> list[int]:
    return [max(x[i - k + 1 : i + 1]) for i in range(k - 1, len(x))]


rng = random.Random(20261103)
checked = 0
worst_ratio = 0.0
ties_last_ok = True
for trial in range(4000):
    n = rng.randint(1, 30)
    k = rng.randint(1, n)
    vals = rng.choice([3, 5, 50])  # small value ranges force many ties
    x = [rng.randint(0, vals) for _ in range(n)]
    out, tests, ops = pseudo(x, k)
    assert out == brute(x, k), (x, k, out)
    assert tests <= 2 * n, (x, k, tests)
    assert ops <= 2 * n + n, (x, k, ops)  # appends n, removals at most n (plus expiry counted in removals)
    worst_ratio = max(worst_ratio, tests / (2 * n))
    # last-occurrence claim: front index equals largest index whose value is the window max
    for i in range(k, n + 1):
        win = range(i - k + 1, i + 1)
        m = max(x[j - 1] for j in win)
        last = max(j for j in win if x[j - 1] == m)
        # recompute front by re-running up to i
    checked += 1
print("pseudocode matches brute force on", checked, "random cases; worst tests/(2n) =", round(worst_ratio, 4))

# last-occurrence check, by re-running the algorithm and recording the front after each step
for trial in range(2000):
    n = rng.randint(1, 25)
    k = rng.randint(1, n)
    x = [rng.randint(0, 4) for _ in range(n)]
    xi = [0] + x
    dq: deque[int] = deque()
    for i in range(1, n + 1):
        while dq and xi[dq[-1]] <= xi[i]:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k:
            win = range(i - k + 1, i + 1)
            m = max(x[j - 1] for j in win)
            last = max(j for j in win if x[j - 1] == m)
            if dq[0] != last:
                ties_last_ok = False
print("front is the last occurrence of the window maximum on all sampled windows:", ties_last_ok)

# Remark 2.2 algebra
for n in (6, 7, 200):
    for j in range(0, n):
        assert (n - j) * j == n * n / 4 - (j - n / 2) ** 2
print("Remark 2.2 identity (n-j)j = n^2/4 - (j - n/2)^2 holds for tested n")

# Remark 3.4: deque comparisons when the decreasing prefix is removed in one loop, k <= 100
for k in (3, 100, 101):
    x = list(range(k, 1, -1)) + [100]
    _, tests, _ = pseudo(x, k)
    print("Remark 3.4 k =", k, "tests =", tests, "bound 2n =", 2 * k)
