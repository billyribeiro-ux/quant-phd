"""Independent brute-force checks of L05 Propositions 2.1, 3.2, 3.3, P3, Remark 3.4 and Example 3.5/Problem M2 traces.

The deque here is written independently of the lab twin (own code from the page's pseudocode), and it counts
while-loop value comparisons as Proposition 3.3 defines them.
"""

from __future__ import annotations

import itertools
import random
from collections import deque


def deque_run(x: list[float], k: int) -> tuple[list[float], int, int, list[int]]:
    dq: deque[int] = deque()
    out: list[float] = []
    comps = 0
    back_removals_at_step: list[int] = []
    for i in range(1, len(x) + 1):
        removed = 0
        while dq:
            comps += 1
            if x[dq[-1] - 1] <= x[i - 1]:
                dq.pop()
                removed += 1
            else:
                break
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k:
            out.append(x[dq[0] - 1])
        back_removals_at_step.append(removed)
    return out, comps, len(x), back_removals_at_step


def brute(x: list[float], k: int) -> list[float]:
    return [max(x[i - k : i]) for i in range(k, len(x) + 1)]


rng = random.Random(12345)
checked = 0
worst_ratio = 0.0
for trial in range(4000):
    n = rng.randint(1, 12)
    vals = [rng.randint(0, 4) for _ in range(n)]  # many ties on purpose
    for k in range(1, n + 1):
        out, comps, nn, _ = deque_run(vals, k)
        assert out == brute(vals, k), (vals, k)
        assert comps <= 2 * n, (vals, k, comps)
        worst_ratio = max(worst_ratio, comps / (2 * n))
        checked += 1
print(f"Prop 3.2 outputs equal brute force and Prop 3.3 bound 2n holds on {checked} (sequence, k) pairs; max comps/(2n) = {worst_ratio:.3f}")

# Prop 2.1: naive count (n-k+1)(k-1), with the naive scan written from H3
for n in range(1, 30):
    for k in range(1, n + 1):
        count = 0
        for i in range(k, n + 1):
            count += k - 1
        assert count == (n - k + 1) * (k - 1)
print("Prop 2.1 count identity checked for 1 <= n < 30")

# P3: strictly increasing sequence: exactly n-1 while-loop comparisons for every k
for n in range(1, 40):
    for k in range(1, n + 1):
        x = list(range(1, n + 1))
        _, comps, _, _ = deque_run(x, k)
        assert comps == n - 1, (n, k, comps)
print("P3 n-1 comparisons on strictly increasing sequences checked for 1 <= n < 40, all k")

# Remark 3.4: x = (k, k-1, ..., 2, k+1), n = k: step k removes k-1 entries
for k in range(2, 12):
    x = list(range(k, 1, -1)) + [k + 1]
    assert len(x) == k
    _, _, _, removals = deque_run(x, k)
    assert removals[-1] == k - 1, (k, removals)
print("Remark 3.4: step k removes k-1 entries for k = 2..11")

# Example 3.5 trace and Problem M2 trace outputs
print("Example 3.5 outputs (expect (4,4,5)):", deque_run([3, 1, 4, 1, 5], 3)[0])
print("Problem M2 outputs (expect (5,5,1,3)):", deque_run([2, 5, 1, 0, 3], 2)[0])
print("Problem M3 k=1 outputs equal the input:", deque_run([2, 5, 1, 0, 3], 1)[0] == [2, 5, 1, 0, 3])
print("Problem M3 k=n gives one output:", deque_run([2, 5, 1, 0, 3], 5)[0] == [5])
print("P1: max of (n-r) r over integer r for n=200 equals 10000 at r=100:", max((200 - r) * r for r in range(0, 201)), (200 - 100) * 100)
