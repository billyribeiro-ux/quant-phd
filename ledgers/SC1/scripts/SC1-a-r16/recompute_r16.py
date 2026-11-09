"""SC1-a round 16 independent recomputation of numbers printed or claimed in L01, L02, L03 and the hub.

Re-derives every number from first principles (own code, not the twins). Run: python3 -I <this file>.
"""

import math
import random
from fractions import Fraction

print("== L01 numbers")
print("placement 7/9 =", round(7 / 9 * 100, 1), " 8/9 =", round(8 / 9 * 100, 1))
print("sd of B_{1/4}-B_0 =", math.sqrt(0.25), "; 1/sqrt(1/100) =", 1 / math.sqrt(0.01))
print("sqrt(1/100)/(1/100) =", math.sqrt(0.01) / 0.01)
print("Var(3B1-B2) =", 9 * 1 + 2 - 6 * min(1, 2))
print("E[B3^2] =", 3)
t = Fraction(3, 4)
print("L01 E1: piece length 3/64, 16*(3/64) =", 16 * Fraction(3, 64))

print("== hub placement / rung 2 claim: walks of n=6 steps with max >= 2")
cnt = 0
for bits in range(2**6):
    s = 0
    m = 0
    for b in range(6):
        s += 1 if (bits >> b) & 1 else -1
        m = max(m, s)
    if m >= 2:
        cnt += 1
print("count n=6 a=2 max>=2:", cnt)
cnt2 = sum(1 for bits in range(4) if max(sum(1 if (bits >> b) & 1 else -1 for b in range(j + 1)) for j in range(2)) >= 1)
print("count n=2 a=1 max>=1:", cnt2)

print("== L02 lab numbers (SEED 20260101, LEVELS 8)")
SEED = 20260101
LEVELS = 8


def hat(m, j, t):
    c = (2 * j - 1) / 2.0**m
    return max(0.0, 1.0 - 2.0**m * abs(t - c))


def bound(m):
    return math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2)


def run_seed(seed, verbose=False):
    rng = random.Random(seed)
    xi0 = rng.gauss(0.0, 1.0)
    coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, LEVELS + 1)]

    def psum(levels, t):
        total = xi0 * t
        for m in range(1, levels + 1):
            sc = 2 ** (-(m + 1) / 2)
            for j in range(1, 2 ** (m - 1) + 1):
                total += coeffs[m - 1][j - 1] * sc * hat(m, j, t)
        return total

    def lsup(m):
        return max(abs(c) for c in coeffs[m - 1]) * 2 ** (-(m + 1) / 2)

    res = {}
    fixed_cases = fixed_equal = 0
    for n in range(5):
        for k in range(2**n + 1):
            t = k / 2**n
            base = psum(n, t)
            for levels in range(n, LEVELS + 1):
                fixed_cases += 1
                fixed_equal += psum(levels, t) == base
    res["fixed"] = (fixed_equal, fixed_cases)
    grid = [i / 2**10 for i in range(2**10 + 1)]
    agree = 0
    for m in range(1, LEVELS + 1):
        sc = 2 ** (-(m + 1) / 2)
        gs = max(abs(sum(coeffs[m - 1][j - 1] * hat(m, j, t) for j in range(1, 2 ** (m - 1) + 1)) * sc) for t in grid)
        agree += gs == lsup(m)
    res["grid_agree"] = agree
    within = sum(1 for m in range(1, LEVELS + 1) if lsup(m) <= bound(m))
    res["within"] = within
    tail_grid = max(abs(psum(LEVELS, t) - psum(4, t)) for t in grid)
    tail_bound = sum(bound(m) for m in range(5, LEVELS + 1))
    res["tail_grid"] = tail_grid
    res["tail_bound"] = tail_bound
    res["sups"] = [lsup(m) for m in range(1, LEVELS + 1)]
    res["xi11"] = coeffs[0][0]
    res["xi0"] = xi0
    return res


r = run_seed(SEED)
print("fixed:", r["fixed"], " grid_agree:", r["grid_agree"], "/", LEVELS, " within:", r["within"])
for m, s in enumerate(r["sups"], start=1):
    print(f"m = {m}: observed sup {s:.6f}, bound {bound(m):.6f}")
print(f"grid sup |Sigma_8-Sigma_4|: {r['tail_grid']:.6f}; sum bounds 5..8: {r['tail_bound']:.6f}")
x11 = abs(r["xi11"])
print("unrounded |xi_{1,1}| =", repr(x11), " level-1 sup =", repr(x11 * 2 ** -1))
print("twice the unrounded level-1 sup, 7 dp:", f"{2 * (x11 * 2 ** -1):.7f}", " rounded 6dp of 2*sup:", f"{2 * (x11 * 2 ** -1):.6f}")
print("printed level-1 sup 6dp of unrounded:", f"{x11 * 2 ** -1:.6f}")
print("lambda_1/2 =", f"{math.sqrt(4 * math.log(2)) / 2:.6f}", " sqrt(4 log 2) =", f"{math.sqrt(4 * math.log(2)):.6f}")

print("== L02 seed sweep: identities for seeds 0..49")
bad = []
for seed in range(50):
    rr = run_seed(seed)
    if rr["fixed"][0] != rr["fixed"][1] or rr["grid_agree"] != LEVELS:
        bad.append(seed)
print("seeds with a failed identity (dyadic fixed or grid sup):", bad)

print("== L03 numbers (SEED 20260503, PATHS 400)")
SEED3 = 20260503
PATHS = 400
rng = random.Random(SEED3)
rows = {}
for H in (1.0, 2.0):
    for k in range(8):
        N = 2**k
        sd = math.sqrt(H / N)
        vals = []
        for _ in range(PATHS):
            tot = 0.0
            for _ in range(N):
                inc = rng.gauss(0.0, sd)
                tot += inc * inc
            vals.append(tot)
        mean = sum(vals) / PATHS
        var = sum((v - mean) ** 2 for v in vals) / (PATHS - 1)
        se = math.sqrt(var / PATHS)
        z = (mean - H) / se
        theo = H * math.sqrt(2 / N) / 20
        rows[(H, N)] = (mean, se, z, theo)
        print(f"H={H:g} N={N:3d} mean={mean:.6f} se={se:.6f} z={z:.4f} theo_se={theo:.6f} gap={(se / theo - 1) * 100:+.4f}%")
maxz = max(rows.items(), key=lambda kv: abs(kv[1][2]))
print("largest |z| at", maxz[0], abs(maxz[1][2]))
zs = sorted((abs(v[2]) for v in rows.values()), reverse=True)
print("second largest |z|:", zs[1], " all |z| <= 3:", all(z <= 3 for z in zs))
gaps = {key: abs(v[1] / v[3] - 1) for key, v in rows.items()}
gk = max(gaps, key=gaps.get)
print("largest |gap| at", gk, f"{gaps[gk] * 100:.4f}%  (unrounded se)")
print("largest gap within 14 percent:", gaps[gk] * 100 < 14)
print("four-decimal printed se 0.1601 gap:", f"{(0.1601 / (2 * math.sqrt(2) / 20) - 1) * 100:.4f}%")
print("H=1 N=1 theo sqrt2/20:", f"{math.sqrt(2) / 20:.6f}")
print("H=2 N=128 theo:", f"{2 * math.sqrt(2 / 128) / 20:.6f}")
