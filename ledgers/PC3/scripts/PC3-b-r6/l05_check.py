"""Independent check of L05 numbers (PC3-b round 6). Own implementation of the page's pseudocode and counting rules.

Counting rule from the page (Prop 3.3): comparisons = one per while-loop test on a non-empty deque; pops = back and
front removals; pushes = appends. Input: random.Random(seed).randint(0, 999) x 200, as in the lab docstring.
"""
import random
from collections import deque

def seq(seed, n=200):
    r = random.Random(seed)
    return [r.randint(0, 999) for _ in range(n)]

def naive(xs, k):
    out, cmp_ = [], 0
    for s in range(len(xs) - k + 1):
        w = xs[s:s + k]
        best = w[0]
        for x in w[1:]:
            cmp_ += 1
            best = max(best, x)
        out.append(best)
    return out, cmp_

def dq(xs, k):
    d = deque()
    out = []
    comps = pops = pushes = 0
    for i, x in enumerate(xs):
        while d:
            comps += 1
            if xs[d[-1]] > x:
                break
            d.pop()
            pops += 1
        d.append(i)
        pushes += 1
        if d[0] <= i - k:
            d.popleft()
            pops += 1
        if i >= k - 1:
            out.append(xs[d[0]])
    return out, dict(comps=comps, pops=pops, pushes=pushes)

def brute(xs, k):
    return [max(xs[i - k + 1:i + 1]) for i in range(k - 1, len(xs))]

x5 = seq(5)
print("seed5 first5", x5[:5], "max", max(x5))
n5, nc5 = naive(x5, 8)
d5, o5 = dq(x5, 8)
print("seed5 k8: naive", nc5, "deque", o5, "equal", n5 == d5, "brute", brute(x5, 8) == n5)
print("seed5 ratio k32 naive/deque:", 5239 / 382, "check", naive(x5, 32)[1], dq(x5, 32)[1]["comps"])
print("seed5 k=1 deque", dq(x5, 1)[1], "k200", dq(x5, 200)[1], naive(x5, 200)[1])
for k in (1, 2, 8, 32, 200):
    _, o = dq(x5, k)
    print("row", k, "windows", 200 - k + 1, "naive", naive(x5, k)[1], "formula", (200 - k + 1) * (k - 1), "deque", o)
print("seed5 k1..20 agree", all(naive(x5, k)[0] == dq(x5, k)[0] == brute(x5, k) for k in range(1, 21)))
x6 = seq(6)
n6, nc6 = naive(x6, 8)
d6, o6 = dq(x6, 8)
print("seed6 k8 outputs equal", n6 == d6, "naive", nc6, "deque", o6, "ratio", o6["comps"] <= 400)
print("seed6 first five", x6[:5])
# edge checks from the page
print("k=1 output equals input:", dq(x5, 1)[0] == x5)
print("k=n one entry", dq(x5, 200)[0] == [max(x5)])
print("E3 split bound: 194 + 200 =", 194 + 200, "387 <= 394:", 387 <= 394)
print("R2 k maximizing naive:", max(range(1, 201), key=lambda k: (200 - k + 1) * (k - 1)), (200 - 101 + 1) * 100)
print("Remark 3.6 heap bound 3*200*7 =", 3 * 200 * 7)
# P3 increasing sequence: deque comparisons equal n-1 for all k
inc = list(range(1, 201))
print("increasing n-1 for all k:", all(dq(inc, k)[1]["comps"] == 199 for k in range(1, 201)))
# Remark 3.4 example check for k=5: x = (k, k-1, ..., 2, k+1)
kk = 5
ex = list(range(kk, 1, -1)) + [kk + 1]
print("Remark 3.4 example k=5 xs", ex, "removals at step k:", dq(ex, kk)[1])
# Example 3.5 trace
print("Example 3.5 outputs", dq([3, 1, 4, 1, 5], 3)[0])
print("M2 trace outputs", dq([2, 5, 1, 0, 3], 2)[0])
print("Prop 3.3 check all k in 1..200 for seed 5: comps<=2n and pops<=n, pushes==n:",
      all(dq(x5, k)[1]["comps"] <= 400 and dq(x5, k)[1]["pops"] <= 200 and dq(x5, k)[1]["pushes"] == 200 for k in range(1, 201)))
print("Prop 3.3 checks seed 6 all k:", all(dq(x6, k)[1]["comps"] <= 400 for k in range(1, 201)))
