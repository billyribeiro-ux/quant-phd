"""Independent recomputation for CS2 L10: lab counts, invariant stress test (Theorem 2.2, 2.3, 2.4, Cor 2.5),
worked examples M1-M3, E1-E3, R1-R3, the looser-rule variant (R1) and the R2 example.

Run: python3 -I -W error ledgers/CS2/scripts/CS2-c-r4/l10_numbers_r4.py
"""
import random
from collections import deque


def push_min_or_max(dq, series_idx, i, x, w, is_min, stats):
    """Definition 2.1 written from its wording. dq holds indices; values read from series."""
    removed = 0
    # (1) remove back entries dominated by x (at least x for min, at most x for max)
    while dq:
        b = series[dq[-1]]
        if (b >= x) if is_min else (b <= x):
            dq.pop()
            removed += 1
        else:
            break
    # (2) append i
    dq.append(i)
    # (3) expire front entries with index <= i - w
    while dq and dq[0] <= i - w:
        dq.popleft()
        removed += 1
    stats["ops"] += 1 + removed
    stats["removed_max"] = max(stats["removed_max"], removed)
    stats["size_max"] = max(stats["size_max"], len(dq))


def run(series_, w, is_min):
    global series
    series = series_
    dq = deque()
    stats = {"ops": 0, "removed_max": 0, "size_max": 0}
    fronts = []
    for i, x in enumerate(series):
        push_min_or_max(dq, None, i, x, w, is_min, stats)
        fronts.append(series[dq[0]])
    return fronts, stats


def brute(series_, i, w, is_min):
    seg = series_[max(0, i - w + 1): i + 1]
    return min(seg) if is_min else max(seg)


# Lab 1 recomputation: seeded integer series N=200, seed 1010, windows 1,2,5,13,30
rng = random.Random(1010)
S = [rng.randint(0, 999) for _ in range(200)]
print("LAB window  ops_min ops_max largest_removals_min largest_removals_max largest_size_max brute_ok")
for w in (1, 2, 5, 13, 30):
    fmin, smin = run(S, w, True)
    fmax, smax = run(S, w, False)
    ok = all(fmin[i] == brute(S, i, w, True) and fmax[i] == brute(S, i, w, False) for i in range(200))
    print(f"LAB {w:>2} {smin['ops']:>8} {smax['ops']:>7} {smin['removed_max']:>27} {smax['removed_max']:>27} {max(smin['size_max'], smax['size_max']):>17} {ok}")

# Stress: Theorem 2.2 (invariant), 2.3 (front = rolling min, latest position), 2.4 (ops <= 2n, comparisons),
# Corollary 2.5(b) (|D_i| <= w) on many random series with ties
bad = 0
cases = 0
for seed in range(400):
    r = random.Random(seed)
    n = r.randint(1, 60)
    w = r.randint(1, 12)
    series = [r.randint(0, 5) for _ in range(n)]
    for is_min in (True, False):
        dq_fronts, st = run(series, w, is_min)
        cases += 1
        if st["ops"] > 2 * n or st["size_max"] > w:
            bad += 1
        for i in range(n):
            if dq_fronts[i] != brute(series, i, w, is_min):
                bad += 1
# Theorem 2.3 latest-position check
for seed in range(200):
    r = random.Random(1000 + seed)
    n = r.randint(1, 40)
    w = r.randint(1, 10)
    series = [r.randint(0, 3) for _ in range(n)]
    dq = deque()
    stats = {"ops": 0, "removed_max": 0, "size_max": 0}
    global_series = series
    for i in range(n):
        push_min_or_max(dq, None, i, series[i], w, True, stats)
        lo = max(0, i - w + 1)
        m = min(series[lo:i + 1])
        latest = max(j for j in range(lo, i + 1) if series[j] == m)
        if dq[0] != latest:
            bad += 1
print("STRESS cases", cases, "failures", bad)

# E1: window 1, n=200 random series: total ops is exactly 2n-1
for seed in range(20):
    r = random.Random(seed)
    s = [r.randint(0, 9) for _ in range(200)]
    for is_min in (True, False):
        _, st = run(s, 1, is_min)
        assert st["ops"] == 2 * 200 - 1, (seed, st)
print("E1 window1 2n-1 holds on 40 random series; n=200 gives", 2 * 200 - 1)

# E3: strictly decreasing, any window: ops = 2n-1 and size 1
for w in (1, 2, 3, 7, 50):
    s = list(range(10, 0, -1))
    _, st = run(s, w, True)
    print("E3 decreasing n=10 w=", w, "ops", st["ops"], "size_max", st["size_max"])

# E2: 1,2,3,4,5,0 with w=5, minimum deque: insertion 5 removes 5
series = [1, 2, 3, 4, 5, 0]
dq = deque()
stats = {"ops": 0, "removed_max": 0, "size_max": 0}
per = []
for i, x in enumerate(series):
    before = stats["removed_max"]
    push_min_or_max(dq, None, i, x, 5, True, stats)
    per.append(list(dq))
print("E2 deque after each insertion (min, w=5):", per, "removed_max", stats["removed_max"])

# R2: 4,1,4 with w=2 minimum version
series = [4, 1, 4]
dq = deque()
stats = {"ops": 0, "removed_max": 0, "size_max": 0}
per = []
for i, x in enumerate(series):
    push_min_or_max(dq, None, i, x, 2, True, stats)
    per.append(list(dq))
print("R2 deque (index) after each insertion:", per)

# R3: increasing series 0..n-1 with window w: step-3 removals = n-w
for n, w in ((10, 3), (200, 5), (7, 7), (7, 9)):
    series = list(range(n))
    _, st = run(series, w, True)
    print("R3 n", n, "w", w, "expected max expiry", max(0, n - w))

# M2 trace (3,1,4,1,5; w=3)
series = [3, 1, 4, 1, 5]
dq = deque()
stats = {"ops": 0, "removed_max": 0, "size_max": 0}
trace = []
for i, x in enumerate(series):
    push_min_or_max(dq, None, i, x, 3, True, stats)
    trace.append([(j, series[j]) for j in dq])
print("M2 trace", trace)
print("M3 total ops", stats["ops"], "bound", 2 * len(series))
fronts = [series[dq_idx[0][0]] for dq_idx in [t for t in trace]]
print("M1 fronts", [t[0][1] for t in trace])

# R1: looser rule (remove only strictly greater back). Check the min equals brute force and deque nondecreasing.
def run_loose(series_, w):
    dq = deque()
    fronts = []
    bad_order = 0
    for i, x in enumerate(series_):
        while dq and series_[dq[-1]] > x:
            dq.pop()
        dq.append(i)
        while dq and dq[0] <= i - w:
            dq.popleft()
        vals = [series_[j] for j in dq]
        if any(vals[k] > vals[k + 1] for k in range(len(vals) - 1)):
            bad_order += 1
        fronts.append(series_[dq[0]])
    return fronts, bad_order

rbad = 0
for seed in range(300):
    r = random.Random(5000 + seed)
    n = r.randint(1, 50)
    w = r.randint(1, 10)
    s = [r.randint(0, 4) for _ in range(n)]
    fr, bo = run_loose(s, w)
    if bo:
        rbad += 1
    for i in range(n):
        if fr[i] != brute(s, i, w, True):
            rbad += 1
print("R1 looser-rule failures", rbad)
