"""Independent recomputation of the project page numbers (round 15, SC1-d). Written from the page's definitions, not
by importing the labs or the grader. Usage: recompute_r15.py  (run with -I from the checkout root)."""
import math
import random
from fractions import Fraction

def inst(seed):
    rng = random.Random(1_000_003 * seed + 54_321)
    H = round(rng.uniform(0.25, 4.0), 3)
    a = round(rng.uniform(0.25, 2.5), 3)
    n = rng.randint(4, 256)
    N = rng.randint(400, min(800, 200_000 // n))
    return H, a, n, N

H, a, n0, N = inst(0)
print("instance seed0 H,a,n_steps,N =", H, a, n0, N)
tail = math.erfc(a / math.sqrt(2 * H))
print(f"tail {tail:.6f}")
# Simpson on the normal density, own implementation
def simpson(a, H, m=4000):
    top = a + 12 * math.sqrt(H); h = (top - a) / m
    f = lambda x: math.exp(-x * x / (2 * H)) / math.sqrt(2 * math.pi * H)
    s = f(a) + f(top) + sum((4 if k % 2 else 2) * f(a + k * h) for k in range(1, m))
    return 2 * s * h / 3
print(f"simpson diff {abs(simpson(a,H)-tail):.2e}")
# one-step estimate (draws in the page's order, gauss(0, sqrt(H)))
rng = random.Random(0)
ind = [1.0 if rng.gauss(0.0, math.sqrt(H)) >= a else 0.0 for _ in range(N)]
p = sum(ind) / N
se = math.sqrt(sum((x - p) ** 2 for x in ind) / (N - 1)) / math.sqrt(N)
target = tail / 2
tse = math.sqrt(target * (1 - target) / N)
print(f"one step est {p:.6f} se {se:.6f} target {target:.6f} target_se {tse:.6f} band {5*tse+1/N:.6f} diff {abs(p-target):.6f}")
print(f"gap_tail_minus_est {tail-p:.6f}; est-target over sample se {abs(p-target)/se:.2f}; over target se {abs(p-target)/tse:.2f}")
# grids, own implementation: path k-th partial sums, gauss(0, sqrt(H/n))
def grid_max_hits(n, a, H, N, seed=0, stride_list=(1,)):
    rng = random.Random(seed)
    sd = math.sqrt(H / n)
    hits = {s: 0 for s in stride_list}
    for _ in range(N):
        pos = 0.0; mx = {s: -1e300 for s in stride_list}
        for k in range(1, n + 1):
            pos += rng.gauss(0.0, sd)
            for s in stride_list:
                if k % s == 0 and pos > mx[s]:
                    mx[s] = pos
        for s in stride_list:
            if mx[s] >= a:
                hits[s] += 1
    return hits
for g in (1, 4, 16, 64, 256):
    h = grid_max_hits(g, a, H, N)[1]
    est = h / N
    sem = math.sqrt(est * (1 - est) / (N - 1)) / 1.0 * math.sqrt(1)  # sqrt(p(1-p)/(N-1)) form
    se_g = math.sqrt(est * (1 - est) / (N - 1))
    print(f"grid {g}: hits {h} est {est:.6f} se {se_g:.6f} tail-est {tail-est:.6f} within5se {abs(est-tail) <= 5*se_g}")
nest = grid_max_hits(256, a, H, N, stride_list=(1, 4, 16, 64, 256))
print("nested fine", nest[1], "coarse 64", nest[4], "coarse 16", nest[16], "coarse 4", nest[64], "coarse 1", nest[256])
# walk counts by DP over (position, reached) -- independent of enumeration
def walk_counts_dp(n, a):
    dist = {(0, False): 1}
    for _ in range(n):
        new = {}
        for (pos, reached), c in dist.items():
            for step in (1, -1):
                q = pos + step
                key = (q, reached or q >= a)
                new[key] = new.get(key, 0) + c
        dist = new
    maxhits = sum(c for (pos, reached), c in dist.items() if reached)
    endhits = sum(c for (pos, reached), c in dist.items() if pos >= a)
    return maxhits, endhits
print("walk n=12 a=3 (max, end):", walk_counts_dp(12, 3), "identity end+end(a+1):", walk_counts_dp(12, 3)[1] + walk_counts_dp(12,4)[1])
print("walk n=6 a=2:", walk_counts_dp(6, 2), "end(a+1)", walk_counts_dp(6, 3)[1])
# seed-32 claim: instance of seed 32, grids 16, 32, 64 at its own level: estimate zero?
H32, a32, n32, N32 = inst(32)
print("seed 32 instance:", H32, a32, n32, N32)
for g in (4, 8, 16, 32, 64):
    print("  seed32 own level grid", g, "hits", grid_max_hits(g, a32, H32, N32, seed=32)[1])
