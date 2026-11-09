"""Independent re-derivation of the L10 lab numbers and the L10 worked examples (CS2-c r3).
Uses only the page's Definition 2.1 wording, not the twin's code. Brute force over every window."""
import random
from collections import deque

def run(series, w, sign):
    # sign=+1: minimum deque (remove back while back >= x); sign=-1: maximum deque (remove back while back <= x)
    d = deque()
    ops = 0
    max_removed = 0
    max_size = 0
    front_vals = []
    for i, x in enumerate(series):
        removed = 0
        while d and (sign * (series[d[-1]] - x) >= 0):   # min: back >= x ; max: back <= x
            d.pop(); removed += 1
        d.append(i); ops += 1
        while d[0] <= i - w:
            d.popleft(); removed += 1
        ops += removed
        max_removed = max(max_removed, removed)
        max_size = max(max_size, len(d))
        front_vals.append(series[d[0]])
    return ops, max_removed, max_size, front_vals

def brute(series, w, want_min):
    out = []
    for i in range(len(series)):
        seg = series[max(0, i - w + 1): i + 1]
        out.append(min(seg) if want_min else max(seg))
    return out

rng = random.Random(1010)
series = [rng.randint(0, 999) for _ in range(200)]
for w in (1, 2, 5, 13, 30):
    omin, rmin, smin, fmin = run(series, w, +1)
    omax, rmax, smax, fmax = run(series, w, -1)
    assert fmin == brute(series, w, True), w
    assert fmax == brute(series, w, False), w
    print(f"window {w:2d}: all 200 positions match brute force; operations min {omin}, max {omax}, bound 2N = 400; largest single-push removals {max(rmin, rmax)}; largest deque size {max(smin, smax)}")

# Worked examples on the page
ex_m1 = run([3, 1, 4, 1, 5], 3, +1)
print("M1 fronts", ex_m1[3], "ops", ex_m1[0], "M3 expects 8 ops")
print("E1 window 1 ops n=200:", run(series, 1, +1)[0], "formula 2n-1 =", 2*200-1)
print("E2 series 1..5,0 w=5 max removals:", run([1,2,3,4,5,0], 5, +1)[1])
print("E3 decreasing n=10 ops (w=3):", run(list(range(10,0,-1)), 3, +1)[0], "2n-1=", 19)
print("R2 4,1,4 w=2 min deque final:", end=" ")
d = run([4,1,4], 2, +1); print("fronts", d[3], "ops", d[0])
print("R3 increasing n=12 w=3 expiry removals:", end=" ")
ops, rem, size, fr = run(list(range(12)), 3, +1); print("max_removed per push", rem, "total ops", ops, "n-w+... total expired expected", 12-3)
print("Quiz q3 2n-1 n=10:", 2*10-1, "| Q9 n-w n=10 w=3:", 10-3)
