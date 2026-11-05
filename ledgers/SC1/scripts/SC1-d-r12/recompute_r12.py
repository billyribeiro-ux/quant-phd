"""Independent recomputation of the project page's printed numbers (Labs 1-3, the interpretation arithmetic, the proof's constants)."""
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "course/modules/SC/SC1/grader"))
from instance import make_instance  # the grader's own instance generator, for cross-check

inst = make_instance(0)
H, a, N = inst["H"], inst["a"], inst["n_paths"]
print("instance seed 0 (grader):", {k: inst[k] for k in ("H", "a", "n_steps", "n_paths")})

# Lab 1: closed form, Simpson, one-step estimate and band, with exact-ish quadrature (Fraction-free float, 20000 intervals)
tail = math.erfc(a / math.sqrt(2 * H))
def simpson(lo, hi, n):
    h = (hi - lo) / n
    f = lambda x: math.exp(-x * x / (2 * H)) / math.sqrt(2 * math.pi * H)
    s = f(lo) + f(hi) + sum((4 if k % 2 else 2) * f(lo + k * h) for k in range(1, n))
    return 2 * s * h / 3
quad = simpson(a, a + 12 * math.sqrt(H), 20000)
print(f"Lab1 tail {tail:.6f} quad {quad:.6f} |diff| {abs(quad - tail):.3e}")
rng = random.Random(0)
rng = random.Random(inst["seed"])
draws = [rng.gauss(0.0, math.sqrt(H)) for _ in range(N)]
ind = [1.0 if x >= a else 0.0 for x in draws]
p1 = sum(ind) / N
sd1 = math.sqrt(sum((x - p1) ** 2 for x in ind) / (N - 1)) / math.sqrt(N)
target = tail / 2
tse = math.sqrt(target * (1 - target) / N)
band = 5 * tse + 1 / N
print(f"Lab1 estimate {p1:.6f} sample se {sd1:.6f} target {target:.6f} target se {tse:.6f} band {band:.6f} diff {abs(p1 - target):.6f} inside {abs(p1-target) <= band}")
print(f"  diff / sample se = {abs(p1-target)/sd1:.4f}; diff / target se = {abs(p1-target)/tse:.4f}; diff / ... (page: 1.52, 1.77)")
print(f"  diff in target se units using page's diff 0.016300: {0.016300/0.010735:.4f} and {0.016300/0.009218:.4f}")

# Lab 3: grid estimates on the one-generator reading: path by path, step by step, sd sqrt(H/n)
def grid_max_hits(n_steps, n_paths, stride_list):
    rng = random.Random(inst["seed"])
    sd = math.sqrt(H / n_steps)
    out = {s: 0 for s in stride_list}
    maxima = {s: [] for s in stride_list}
    for _ in range(n_paths):
        pos = 0.0
        best = {s: -math.inf for s in stride_list}
        for k in range(1, n_steps + 1):
            pos += rng.gauss(0.0, sd)
            for s in stride_list:
                if k % s == 0:
                    best[s] = max(best[s], pos)
        for s in stride_list:
            maxima[s].append(best[s])
    return maxima

printed = {1: (29, 0.059548, 0.010735, 0.026948), 4: (24, 0.049281, 0.009819, 0.037215),
           16: (32, 0.065708, 0.011239, 0.020788), 64: (43, 0.088296, 0.012870, -0.001799), 256: (40, 0.082136, 0.012455, 0.004361)}
for n in (1, 4, 16, 64, 256):
    m = grid_max_hits(n, N, [1])[1]
    hits = sum(1 for x in m if x >= a)
    p = hits / N
    se = math.sqrt(hits * (N - hits) / N / (N - 1)) / math.sqrt(N) * 0 + math.sqrt(p * (1 - p) / (N - 1))
    ok = hits == printed[n][0] and round(p, 6) == printed[n][1] and round(se, 6) == printed[n][2] and round(tail - p, 6) == printed[n][3]
    print(f"grid {n}: hits {hits} p {p:.6f} se {se:.6f} tail-p {tail - p:.6f} matches printed: {ok}; within 5 se of tail: {abs(tail - p) <= 5 * se}")
nest = grid_max_hits(256, N, [1, 4, 16, 64, 256])
fine = sum(1 for x in nest[1] if x >= a)
for coarse_n, s in ((64, 4), (16, 16), (4, 64), (1, 256)):
    c = sum(1 for x in nest[s] if x >= a)
    print(f"nested coarse {coarse_n}: {c} <= fine {fine}: {c <= fine}")
print(f"64-step estimate above tail by {-printed[64][3]:.6f} = {(-printed[64][3]) / printed[64][2]:.4f} se (page: 0.14)")
print(f"one-step bias target {tail/2:.6f}; printed 0.026948 - target = {0.026948 - tail/2:.6f} (page -0.016300)")
print(f"page 0.016300/0.010735 = {0.016300/0.010735:.4f}; 0.016300/0.009218 = {0.016300/0.009218:.4f}")

# Walk counts, independent of the page: DP over (position, max) and the reflection identity
def walk_counts(n, lvl):
    dist = {(0, 0): 1}
    for _ in range(n):
        nxt = {}
        for (pos, mx), c in dist.items():
            for st in (1, -1):
                q = pos + st
                key = (q, max(mx, q))
                nxt[key] = nxt.get(key, 0) + c
        dist = nxt
    maxhit = sum(c for (pos, mx), c in dist.items() if mx >= lvl)
    endhit = sum(c for (pos, mx), c in dist.items() if pos >= lvl)
    return maxhit, endhit
print("walk n=12 a=3:", walk_counts(12, 3), "(page 1588, 794)")
print("walk n=6 a=2:", walk_counts(6, 2), "end>=3:", walk_counts(6, 3)[1], "(page 29, 22, 7)")
print("identity n=12 a=3:", walk_counts(12, 3)[0] == walk_counts(12, 3)[1] + walk_counts(12, 4)[1])
print("2^12 =", 2**12)
