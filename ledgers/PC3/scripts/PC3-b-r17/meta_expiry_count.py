"""Round 17: count the deque comparisons under the two readings of 'comparisons' in L05.

reading A (lesson, Prop 3.3): while-loop tests only, each a comparison of stored values.
reading B (literal): every '<=' or '>' comparison operator run, including the front-expiry test window[0] <= i - k.
Run: python3 -I ledgers/PC3/scripts/PC3-b-r17/meta_expiry_count.py
"""
import random
from collections import deque


def counts(xs, k):
    dq = deque()
    tests = 0
    expiry = 0
    for i, x in enumerate(xs):
        while dq:
            tests += 1
            if xs[dq[-1]] > x:
                break
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            expiry += 1
            dq.popleft()
        # the expiry test is run once per step, whether or not it fires
    return tests, expiry


best = (0.0, None)
rr = random.Random(1)
for trial in range(20000):
    n = rr.randint(2, 40)
    k = rr.randint(1, n)
    xs = [rr.randint(0, 99) for _ in range(n)]
    t, e = counts(xs, k)
    ratio_a = t / (2 * n)
    ratio_b = (t + n) / (2 * n)  # the expiry test is run once per step, n times in total
    if ratio_b > best[0]:
        best = (ratio_b, (n, k, t))
    assert t <= 2 * n
print(f"reading A (while tests) max tests/2n over 20000 random cases: <= 1 (assertion held)")
print(f"reading B (tests + one expiry test per step) max (tests+n)/2n = {best[0]:.3f} at (n, k, tests) = {best[1]}")
# explicit example: x = 1..n decreasing sequence in windows
xs = [5, 4, 3, 2, 1, 6, 7, 8, 9, 10]
t, _ = counts(xs, 3)
print(f"example xs={xs} k=3: while tests={t}, n={len(xs)}, tests+n={t+len(xs)} vs 2n={2*len(xs)}")
