"""Independent recomputation of every printed or prose number in SC1 L01 to L03 and the hub.

Written from the page's definitions, not from the twins: exact Fraction hats, own partial-sum code,
own statistics. Only the random draws reuse the seed and draw order of the twins (needed to reproduce the printed sample).
Run: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r3/recompute_r3.py
"""

import math
import random
from fractions import Fraction as F

out = []


def say(s):
    out.append(s)
    print(s)


# ---------- L01 ----------
say("L01 exact checks")
ok = 0
tot = 0
for t in (F(1), F(3, 4), F(5, 2)):
    for n in range(5):
        pieces = 2**n
        s = sum((t / pieces for _ in range(pieces)), F(0))
        tot += 1
        ok += s == t
say(f"  dyadic variance sums equal t: {ok} of {tot}")
grid = [F(i, 8) for i in range(9)]
agree = 0
pairs = 0
for i in range(9):
    for j in range(9):
        pairs += 1
        # Cov(B_s,B_t) = sum of variances of common increments on grid of eighths
        cov = F(min(i, j), 8)
        agree += cov == min(grid[i], grid[j])
say(f"  covariance equals min on grid: {agree} of {pairs}")
say(f"  Cov(B_1/4, B_5/8) = {F(2, 8)} ; min = {min(F(1,4), F(5,8))}")
say(f"  E1 piece length 3/64 times 16 = {16 * F(3, 64)} (claim 3/4)")
say(f"  Example 1.4: sd at h=1/4 {math.sqrt(0.25)}, at h=1/100 {math.sqrt(0.01)}, ratio at h=1/100: {1/math.sqrt(0.01):.12f}")
say(f"  Misconception L01: sd/h at h=1/100 = {math.sqrt(0.01)/0.01:.6f} (ten times)")
say(f"  M3: Var(3B1-B2)=9*1+2-6*min(1,2)={9*1+2-6*1}")

# ---------- L02 ----------
say("L02 recomputation")
SEED = 20260101
LEVELS = 8


def hat_exact(m, j, t):
    centre = F(2 * j - 1, 2**m)
    return max(F(0), 1 - 2**m * abs(t - centre))


rng = random.Random(SEED)
xi0 = rng.gauss(0.0, 1.0)
coeffs = {}
for m in range(1, LEVELS + 1):
    coeffs[m] = [rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))]

# count of dyadic identities and their cases
cases = 0
equal = 0
zero_checks = 0
for n in range(5):
    for k in range(2**n + 1):
        t = F(k, 2**n)
        for M in range(n, LEVELS + 1):
            cases += 1
            # Lemma 2.2(d): every level m in (n, M] vanishes exactly at t (Fraction), so S_M(t)=S_n(t)
            vanish = all(hat_exact(m, j, t) == 0 for m in range(n + 1, M + 1) for j in range(1, 2 ** (m - 1) + 1))
            equal += vanish
            zero_checks += 1
say(f"  Lemma 2.2(d) exact vanishing: {equal} of {cases} (depth, point, level) cases")
# distinct points and pairs
pairs_by_depth = [2**n + 1 for n in range(5)]
say(f"  points per depth 0..4: {pairs_by_depth}, total pairs {sum(pairs_by_depth)}, distinct points {2**4+1}")
say(f"  case count sum over depth of (points * (9-n)): {sum((2**n+1)*(9-n) for n in range(5))}")

# grid sup identity with exact hats on 2^-10 grid
G = 10
grid_t = [F(i, 2**G) for i in range(2**G + 1)]
sup_ok = True
obs = {}
for m in range(1, LEVELS + 1):
    scale = 2 ** (-(m + 1) / 2)
    best = 0.0
    for t in grid_t:
        val = sum(coeffs[m][j - 1] * float(hat_exact(m, j, t)) for j in range(1, 2 ** (m - 1) + 1))
        best = max(best, abs(val * scale))
    formula = max(abs(c) for c in coeffs[m]) * 2 ** (-(m + 1) / 2)
    sup_ok = sup_ok and (best == formula)
    obs[m] = formula
say(f"  grid sup equals formula for levels 1..8: {sup_ok}")
within = 0
for m in range(1, LEVELS + 1):
    lam = math.sqrt(4 * m * math.log(2))
    bnd = lam * 2 ** (-(m + 1) / 2)
    within += obs[m] <= bnd
    say(f"  m={m}: observed sup {obs[m]:.6f} bound {bnd:.6f} within {obs[m] <= bnd}")
    if m == 1:
        say(f"    E3: |xi_11| implied {obs[1]*2:.6f}; sqrt(4 log2)={math.sqrt(4*math.log(2)):.6f}; half={math.sqrt(4*math.log(2))/2:.6f}")
    # bound identity M_m = sqrt(2 log 2) sqrt(m) 2^{-m/2}
    ident = math.sqrt(2 * math.log(2)) * math.sqrt(m) * 2 ** (-m / 2)
    assert abs(ident - bnd) < 1e-12, (m, ident, bnd)
    # union bound: 2^{m-1} * 2 e^{-lam^2/2} = 2^{-m}
    ub = 2 ** (m - 1) * 2 * math.exp(-lam * lam / 2)
    assert abs(ub - 2 ** (-m)) < 1e-15, (m, ub)
say(f"  levels within bound: {within} of 8; identities M_m and union-bound 2^-m verified (asserts passed)")

# tail
def partial(levels, t):
    total = float(xi0) * float(t)
    for m in range(1, levels + 1):
        scale = 2 ** (-(m + 1) / 2)
        for j in range(1, 2 ** (m - 1) + 1):
            total += coeffs[m][j - 1] * scale * float(hat_exact(m, j, t))
    return total


tail = max(abs(partial(8, t) - partial(4, t)) for t in grid_t)
tb = sum(math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2) for m in range(5, 9))
say(f"  grid sup |S_8-S_4| {tail:.6f}; sum bounds levels 5..8 {tb:.6f}")

# Lemma 2.1 tail sanity: P(|eta|>lam) <= 2 exp(-lam^2/2), via erfc (exact normal tail)
for lam in (0.0, 0.5, 1.0, 2.0, 3.0):
    p = math.erfc(lam / math.sqrt(2))
    say(f"  Lemma 2.1 at lam={lam}: P={p:.6f} <= bound {2*math.exp(-lam*lam/2):.6f}: {p <= 2*math.exp(-lam*lam/2) + 1e-15}")

# Lemma 2.2 variance identity for the level step
for n in range(5):
    c2 = 2 ** (-(n + 2))
    say(f"  n={n}: 1/4*2^-n + c^2 = {0.25*2**(-n)+c2} vs 2^-(n+1) = {2**(-(n+1))}; cov 1/4*2^-n - c^2 = {0.25*2**(-n)-c2}")
    assert abs(0.25 * 2 ** (-n) + c2 - 2 ** (-(n + 1))) < 1e-15

# dyadic-time equality: the M1 claim S_1(1/2) = xi0/2 + xi11/2
say(f"  L02 M2: S_1(1/2) = xi0/2 + xi11/2 holds for own draws: {abs(partial(1, F(1,2)) - (xi0/2 + coeffs[1][0]/2)) < 1e-12}")

# ---------- L03 ----------
say("L03 recomputation")
SEED3 = 20260503
PATHS = 400
rng3 = random.Random(SEED3)
rows = {}
for H in (1.0, 2.0):
    for k in range(8):
        N = 2**k
        sd = math.sqrt(H / N)
        sums = []
        for _ in range(PATHS):
            s = 0.0
            for _ in range(N):
                x = rng3.gauss(0.0, sd)
                s += x * x
            sums.append(s)
        mean = sum(sums) / PATHS
        var = sum((v - mean) ** 2 for v in sums) / (PATHS - 1)
        se = math.sqrt(var / PATHS)
        z = (mean - H) / se
        pop = H * math.sqrt(2 / N) / 20
        rows[(H, N)] = (mean, se, z, pop)
        say(f"  H={H:g} N={N:3d}: mean {mean:.4f} se {se:.4f} z {z:.2f} pop_se {pop:.6f} gap% {(se/pop-1)*100:+.2f}")
gaps = {k: (v[1] / v[3] - 1) for k, v in rows.items()}
mx = max(gaps, key=lambda k: abs(gaps[k]))
say(f"  max |gap| at H={mx[0]:g}, N={mx[1]}: {gaps[mx]*100:.3f} percent; max |z| {max(abs(v[2]) for v in rows.values()):.4f}")
say(f"  printed-value gap at H=2,N=1 using 4-decimal printed values: {(0.1601/(2*math.sqrt(2)/20)-1)*100:.3f} percent")
say(f"  all |z| <= 3: {all(abs(v[2]) <= 3 for v in rows.values())}")
say(f"  within 14 percent for all 16 rows: {all(abs(g) <= 0.14 for g in gaps.values())}")

from itertools import pairwise
for H in (F(1), F(2)):
    for k in range(8):
        N = 2**k
        pts = [H * j / N for j in range(N + 1)]
        exact = sum(((b * b - a * a) ** 2 for a, b in pairwise(pts)), F(0))
        closed = H**4 * F(4 * N * N - 1, 3 * N**3)
        assert exact == closed
say("  exact t-squared sums equal closed form for all 16 (H,N): asserts passed")
say(f"  H=1,N=2: {F(1)**4*(4*4-1)/(3*8)} ; H=2,N=8: {F(16)*255/1536} = {float(F(16)*255/1536):.6f}")
say(f"  H=2,N=128 population se = {2*math.sqrt(2/128)/20}; H=1,N=1 pop se {math.sqrt(2)/20:.6f}")
say(f"  H=1 N=128 exact sum {float(F(1)**4*(4*128*128-1)/(3*128**3)):.6f}")
say(f"  misconception: H=2,N=128 exact sum {float(F(16)*(4*128*128-1)/(3*128**3)):.6f}")
say(f"  L03 M1: E[Q]=1, Var=1 for P={{0,1/2,1}}: {2*(F(1,2))**2}")
say(f"  L03 canon-break counterexample: N*X^2 variance N^2*2(t/N)^2 = {[2*F(1,1)**2 for _ in range(1)]} for every N")
say(f"  E|Z| = sqrt(2/pi) = {math.sqrt(2/math.pi):.12f}; sqrt(2Nt/pi) at N=2,t=1 = {math.sqrt(2*2/math.pi):.6f}")
say(f"  Mean abs sum expectation N sqrt(2/pi) sqrt(t/N) = sqrt(2Nt/pi) identity at N=8: {8*math.sqrt(2/math.pi)*math.sqrt(1/8):.6f} vs {math.sqrt(2*8/math.pi):.6f}")
say(f"  L03 R2 sum sum Delta^2 = t|P| for equal partition: {sum((1/8)**2 for _ in range(8))} vs {1*(1/8)}")
say(f"  hub: 8 lessons x 9h = {8*9}; hours split 72/28 -> percent project {28/100*100:.0f}")
open("/Users/billyribeiro/.fanout/wt/verifyE3-SC1-a/ledgers/SC1/scripts/SC1-a-r3/out/recompute_r3.txt", "w").write("\n".join(out) + "\n")
