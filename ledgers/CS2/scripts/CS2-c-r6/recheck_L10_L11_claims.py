import random, bisect, math
from fractions import Fraction
from collections import deque

# --- L10 deque: independent re-implementation with explicit window check and op counting
def run_deque(series, w, is_min):
    dq = deque(); ops = 0; maxrem = 0; maxsize = 0; out = []
    for i, x in enumerate(series):
        rem = 0
        while dq and ((dq[-1][1] >= x) if is_min else (dq[-1][1] <= x)):
            dq.pop(); rem += 1
        dq.append((i, x))
        while dq[0][0] <= i - w:
            dq.popleft(); rem += 1
        ops += 1 + rem; maxrem = max(maxrem, rem); maxsize = max(maxsize, len(dq))
        out.append(dq[0][1])
    return out, ops, maxrem, maxsize

def brute(series, w, is_min):
    res = []
    for i in range(len(series)):
        seg = series[max(0, i - w + 1): i + 1]
        res.append(min(seg) if is_min else max(seg))
    return res

# alternative random streams: check the claimed op bound and invariants
bad = 0
worst_ops = 0
for seed in range(300):
    r = random.Random(seed)
    n = r.randint(1, 60)
    s = [r.randint(-5, 5) for _ in range(n)]
    for w in (1, 2, 3, 7, 60):
        for is_min in (True, False):
            out, ops, _, size = run_deque(s, w, is_min)
            if out != brute(s, w, is_min) or ops > 2 * n or size > w:
                bad += 1
            worst_ops = max(worst_ops, ops - 2 * n)
print("L10 random-stream mismatches:", bad, "max(ops-2n):", worst_ops)

# E2 example: 1,2,3,4,5,0 w=5 min deque, single push removals at i=5
_, ops, maxrem, _ = run_deque([1, 2, 3, 4, 5, 0], 5, True)
print("L10 E2 example ops", ops, "maxrem", maxrem)
# M3 trace: 3,1,4,1,5 w=3 min
_, ops, _, _ = run_deque([3, 1, 4, 1, 5], 3, True)
print("L10 M3 ops", ops)
# R2: 4,1,4 w=2
out, ops, _, _ = run_deque([4, 1, 4], 2, True)
print("L10 R2 fronts", out, "ops", ops)
# R3: increasing series, count step (3) removals for n=10 w=3
s = list(range(10))
dq = deque(); exp_removed = 0
for i, x in enumerate(s):
    while dq and dq[-1][1] >= x: dq.pop()
    dq.append((i, x))
    while dq[0][0] <= i - 3:
        dq.popleft(); exp_removed += 1
print("L10 R3 step(3) removals n=10 w=3:", exp_removed, "expected n-w =", 10 - 3)
# E1: window 1, n=200 random
r = random.Random(1010)
ser = [r.randint(0, 999) for _ in range(200)]
print("L10 w=1 ops on lab series:", run_deque(ser, 1, True)[1], run_deque(ser, 1, False)[1])
# lab series check of claims: 396..399 totals
for w in (1, 2, 5, 13, 30):
    print("lab series w", w, run_deque(ser, w, True)[1], run_deque(ser, w, False)[1], run_deque(ser, w, True)[2], run_deque(ser, w, False)[2], run_deque(ser, w, True)[3])

# --- L11 sketch: independent check that stored count is stream independent and E/guarantee hold
def sketch_run(xs, eps):
    levels = []; compactions = 0
    def cap(h): return 2 * math.ceil(Fraction((h + 1) * (h + 2), 2) / eps)
    def push(h, x):
        nonlocal compactions
        while len(levels) <= h: levels.append([])
        levels[h].append(x)
        if len(levels[h]) == cap(h):
            buf = sorted(levels[h]); levels[h] = []
            compactions += 1
            for y in buf[1::2]: push(h + 1, y)
    for x in xs: push(0, x)
    return levels, compactions

for eps in (Fraction(1, 20), Fraction(1, 10)):
    stored = set()
    for seed in (2026, 1, 7, 99, 12345):
        r = random.Random(seed)
        xs = [r.random() for _ in range(5000)]
        levels, comp = sketch_run(xs, eps)
        stored.add((sum(len(l) for l in levels), comp))
    print("L11 eps", eps, "(stored, compactions) over 5 seeds:", stored)
# worst-case rank error over random orders for claimed bound
for eps in (Fraction(1, 20),):
    worst = 0
    for seed in range(5):
        r = random.Random(seed * 17 + 3)
        xs = [r.random() for _ in range(5000)]
        levels, comp = sketch_run(xs, eps)
        pairs = sorted((v, 2 ** h) for h, l in enumerate(levels) for v in l)
        ordered = sorted(xs)
        for k in range(0, 101):
            q = Fraction(k, 100)
            tgt = q * 5000
            cum = 0
            for v, w in pairs:
                cum += w
                if cum >= tgt: break
            below = bisect.bisect_left(ordered, v); atle = bisect.bisect_right(ordered, v)
            assert below <= tgt + eps * 5000 and atle >= tgt - eps * 5000, (seed, q)
            worst = max(worst, below - float(tgt))
    print("L11 worst excess over 101 quantiles, 5 seeds (fraction of N):", worst / 5000, "bound", float(eps))
