"""Brute-force check of CS2-c139: the front of the minimum deque after position i is i exactly when
x_i is at most every value still in the window (and 'not in general' holds for some series)."""
import random
from collections import deque

def run(xs, w):
    dq = deque()
    fronts = []
    for i, x in enumerate(xs):
        while dq and xs[dq[-1]] >= x:          # step (1), minimum version
            dq.pop()
        dq.append(i)                            # step (2)
        while dq and dq[0] <= i - w:            # step (3)
            dq.popleft()
        fronts.append(dq[0])
    return fronts

rng = random.Random(7)
checked = 0
not_i = 0
for trial in range(3000):
    n = rng.randint(1, 30)
    w = rng.randint(1, 8)
    xs = [rng.randint(0, 5) for _ in range(n)]   # small range: ties included
    fr = run(xs, w)
    for i in range(n):
        window = range(max(0, i - w + 1), i)     # earlier indices still in W_i
        cond = all(xs[i] <= xs[j] for j in window)
        assert (fr[i] == i) == cond, (xs, w, i)
        checked += 1
        if fr[i] != i:
            not_i += 1
print("checked positions:", checked, "front != i positions:", not_i)
print("c139 equivalence holds on all checked positions; 'not in general' witness: xs=[1,2], w=2 gives fronts", run([1, 2], 2))
