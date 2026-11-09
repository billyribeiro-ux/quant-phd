"""Independent recomputation of the seed-0 numbers and prose figures (round 18), by routes different from the page's.
Usage: python3 -I indep_numbers_r18.py"""
import math
import random
from statistics import NormalDist

N01 = NormalDist()
SEED = 0
# instance, drawn in the page's fixed order
r = random.Random(1_000_003 * SEED + 54_321)
H = round(r.uniform(0.25, 4.0), 3)
a = round(r.uniform(0.25, 2.5), 3)
n_steps = r.randint(4, 256)
N = r.randint(400, min(800, 200_000 // n_steps))
print("instance", H, a, n_steps, N)

tail_erfc = math.erfc(a / math.sqrt(2 * H))
tail_norm = 2 * (1 - N01.cdf(a / math.sqrt(H)))  # route 2: normal cdf
print(f"tail erfc {tail_erfc:.9f}  tail via NormalDist {tail_norm:.9f}  diff {abs(tail_erfc - tail_norm):.2e}")
tail = tail_erfc

def paths(n):
    g = random.Random(SEED)
    out = []
    sd = math.sqrt(H / n)
    for _ in range(N):
        steps = [g.gauss(0.0, sd) for _ in range(n)]
        pos, run, mx = 0.0, [], -math.inf
        for s in steps:
            pos += s
            mx = max(mx, pos)
            run.append(pos)
        out.append(run)
    return out

def est(hits, n):
    p = hits / n
    var = sum((1.0 if x else 0.0 - p) ** 2 for x in [])  # placeholder, replaced below
    var = (hits * (1 - p) ** 2 + (n - hits) * p ** 2) / (n - 1)
    return p, math.sqrt(var) / math.sqrt(n)

rows = {}
for n in (1, 4, 16, 64, 256):
    ps = paths(n)
    hits = sum(1 for run in ps if max(run) >= a)
    p, se = est(hits, N)
    rows[n] = (hits, p, se)
    print(f"n={n:3d} hits={hits:3d} est={p:.6f} se={se:.6f} tail-est={tail - p:+.6f}")

# nested on the 256-step paths
ps = paths(256)
fine = sum(1 for run in ps if max(run) >= a)
for coarse_n in (64, 16, 4, 1):
    stride = 256 // coarse_n
    c = sum(1 for run in ps if max(run[stride - 1::stride]) >= a)
    print(f"nested coarse {coarse_n}: {c} <= fine {fine}: {c <= fine}")

# one-step band and prose figures
target = tail / 2
tse = math.sqrt(target * (1 - target) / N)
band = 5 * tse + 1 / N
print(f"target {target:.6f} target_se {tse:.6f} band {band:.6f}")
d = rows[1][1] - target
print(f"one-step diff {d:+.6f}  in SE units: sample {abs(d)/rows[1][2]:.3f} target {abs(d)/tse:.3f}  inside band {abs(d) <= band}")
print(f"64-step excess over tail {rows[64][1] - tail:.6f} = {(rows[64][1]-tail)/rows[64][2]:.3f} SE")
print(f"minimum/maximum grid se {min(v[2] for v in rows.values()):.6f} {max(v[2] for v in rows.values()):.6f}")
print("within 5 se of tail for each grid:", {n: abs(tail - v[1]) <= 5 * v[2] for n, v in rows.items()})

# walk counts, exact, by a different route (binomial sums)
def walks_max_end(n, lev):
    end = sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= lev)
    end1 = sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= lev + 1)
    return end + end1, end
print("walk n=12 a=3 (max, end):", walks_max_end(12, 3), " 4096 =", 2 ** 12)
print("walk n=6 a=2 (max, end, end+1):", walks_max_end(6, 2), sum(math.comb(6, j) for j in range(7) if 2 * j - 6 >= 3))

# test comment claim: seed 32, instance level, grids 16, 32, 64 give estimate 0.0 (at the instance's own level)
def inst_of(seed):
    rr = random.Random(1_000_003 * seed + 54_321)
    h = round(rr.uniform(0.25, 4.0), 3)
    lv = round(rr.uniform(0.25, 2.5), 3)
    ns = rr.randint(4, 256)
    npth = rr.randint(400, min(800, 200_000 // ns))
    return h, lv, npth
h32, lv32, n32 = inst_of(32)
print("seed 32 instance H, a, N:", h32, lv32, n32)
for g in (16, 32, 64):
    sd = math.sqrt(h32 / g)
    gg = random.Random(32)
    hits = 0
    for _ in range(n32):
        pos, mx = 0.0, -math.inf
        for _ in range(g):
            pos += gg.gauss(0.0, sd)
            mx = max(mx, pos)
        hits += mx >= lv32
    print(f"seed 32 grid {g}: hits {hits}")
