"""Witnesses for hypothesis-dropping key-result rows (verifier round 4)."""
import statistics
from collections import deque

# CS2 L10 key-results row: "front is the rolling minimum" without the no-NaN hypothesis of Theorem 2.2
s = [1.0, float("nan"), 0.0]
w = 3
d = deque()
fronts = []
for i, x in enumerate(s):
    while d and s[d[-1]] >= x:
        d.pop()
    d.append(i)
    while d[0] <= i - w:
        d.popleft()
    fronts.append(s[d[0]])
print("L10 NaN witness: deque front after position 2 is", fronts[2], "; the true minimum of the window (1, NaN, 0) is 0.0")

# CS2 L09 key-results row: "one step gives the mean of the first n values" without hypothesis (4) of Theorem 2.1
xs = [1.0, 2.0, 3.0]
M2, S2 = 0.0, 0.0  # wrong state after n-1 = 2 values (should be 1.5 and 0.5)
n = 3
d = xs[2] - M2
M3 = M2 + d / n
print("L09 witness: one step from a wrong state gives M3 =", M3, "but the mean of 1,2,3 is", statistics.mean(xs))
