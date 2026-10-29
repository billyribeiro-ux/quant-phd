"""Round 7 verifier: independent deque (Definition 2.1) checks of L10 claims (stdlib only)."""
import random
from collections import deque


def run(xs, w, mode="min", loose=False):
    dq = deque()
    ops = 0
    maxrem = 0
    fronts = []
    states = []
    for i, x in enumerate(xs):
        rem = 0
        while dq:
            bv = xs[dq[-1]]
            if mode == "min":
                dom = (bv > x) if loose else (bv >= x)
            else:
                dom = (bv < x) if loose else (bv <= x)
            if not dom:
                break
            dq.pop()
            rem += 1
        dq.append(i)
        while dq[0] <= i - w:
            dq.popleft()
            rem += 1
        ops += 1 + rem
        maxrem = max(maxrem, rem)
        fronts.append(xs[dq[0]])
        states.append(list(dq))
    return ops, maxrem, fronts, states


def brute_min(xs, i, w):
    return min(xs[max(0, i - w + 1): i + 1])


rng = random.Random(4242)
fails = 0
checked = 0
for trial in range(400):
    n = rng.randint(1, 60)
    w = rng.randint(1, 12)
    xs = [rng.randint(0, 9) for _ in range(n)]
    ops, maxrem, fronts, states = run(xs, w)
    checked += 1
    # Theorem 2.2 invariant and Thm 2.3 front and window bounds
    for i in range(n):
        S = [j for j in range(max(0, i - w + 1), i + 1) if all(xs[j] < xs[l] for l in range(j + 1, i + 1))]
        if sorted(states[i]) != S:
            fails += 1; print("invariant", trial, i); break
        if fronts[i] != brute_min(xs, i, w):
            fails += 1; print("front", trial, i); break
        if len(states[i]) > w:
            fails += 1; print("size", trial, i)
    if ops > 2 * n:
        fails += 1; print("ops > 2n", trial)
    # Cor 2.5(c) worst single push bound
    if maxrem > w:
        fails += 1; print("maxrem > w", trial)
    # Front index latest attaining min (Thm 2.3): check via last-attaining position
    # card c139: front is the new index i exactly when x_i <= every value still in window
    for i in range(n):
        lhs = (states[i][0] == i)
        rhs = all(xs[i] <= xs[j] for j in range(max(0, i - w + 1), i + 1))
        if lhs != rhs:
            fails += 1; print("c139", trial, i); break
print("random cases", checked, "fails", fails)

# Lab-like series (seed 1010) under the same deque: totals and maxrem
r = random.Random(1010)
series = [r.randint(0, 999) for _ in range(200)]
for w in (1, 2, 5, 13, 30):
    o1, m1, _, _ = run(series, w, "min")
    o2, m2, _, _ = run(series, w, "max")
    print("lab-series window", w, "ops min", o1, "max", o2, "maxrem", max(m1, m2))

# R1: looser rule still gives the right minimum (ties)
bad = 0
for trial in range(300):
    n = rng.randint(1, 40); w = rng.randint(1, 10)
    xs = [rng.randint(0, 4) for _ in range(n)]
    _, _, fr, _ = run(xs, w, "min", loose=True)
    for i in range(n):
        if fr[i] != brute_min(xs, i, w):
            bad += 1; break
print("R1 looser rule front failures:", bad)

# R3 bound and attaining series
n, w = 10, 3
xs = list(range(n))
_, _, _, st = run(xs, w)
removed = 0
prev = set()
# count step-3 removals by simulating: indices never in the deque at the end minus step-1 (none for increasing)
o, mr, _, _ = run(xs, w)
print("increasing series n=10 w=3 total ops", o, "expected 2n-w+n?")
# E1: w=1 total 2n-1 for random series
for trial in range(50):
    n = rng.randint(1, 80)
    xs = [rng.randint(0, 5) for _ in range(n)]
    o, _, _, _ = run(xs, 1)
    assert o == 2 * n - 1, (o, n)
print("E1 w=1 all series: ops = 2n-1 (50 random)")
# E3: strictly decreasing, any w
for w in (1, 2, 5):
    xs = [float(100 - i) for i in range(10)]
    o, _, _, _ = run(xs, w)
    print("E3 decreasing n=10 w", w, "ops", o)
# E2 example and R2 example
print("E2 series 1,2,3,4,5,0 w=5 maxrem", run([1, 2, 3, 4, 5, 0], 5)[1])
o, mr, fr, st = run([4, 1, 4], 2)
print("R2 series 4,1,4 w=2 states", st, "fronts", fr)
# M2 trace
o, mr, fr, st = run([3, 1, 4, 1, 5], 3)
print("M2 states", [[(j, [3, 1, 4, 1, 5][j]) for j in s] for s in st], "fronts", fr, "ops", o)
# Corollary 2.5(c) example w=4
w = 4
xs = list(range(w)) + [-1]
o, mr, fr, st = run(xs, w)
print("Cor2.5c example w=4: maxrem", mr)
