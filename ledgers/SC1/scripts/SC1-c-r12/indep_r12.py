"""Independent recomputation of the printed numbers in SC1 L07 and L08 (round 12).

Uses dynamic programming on the walk position distribution (not the binomial identity), explicit loops, and
math.erfc for the closed forms. Shares no code with the lab twins. Usage: python -I indep_r12.py
"""
import math
import random
from fractions import Fraction

# ---- L08 Part B/D: exact truncated mean via absorbing DP on the walk (independent of the binomial identity)
def first_passage_survival(level: int, steps: int) -> list[Fraction]:
    """Return P(nu_level > k) for k = 0..steps, by DP on positions below the level (absorb at >= level)."""
    dist: dict[int, Fraction] = {0: Fraction(1)}
    out = [Fraction(1)]  # k = 0
    for _ in range(steps):
        nxt: dict[int, Fraction] = {}
        for pos, p in dist.items():
            for step in (1, -1):
                q = pos + step
                if q >= level:
                    continue  # absorbed: passage has happened
                nxt[q] = nxt.get(q, Fraction(0)) + p / 2
        dist = nxt
        out.append(sum(dist.values(), Fraction(0)))
    return out

surv = first_passage_survival(1, 256)
for n in (16, 64, 256):
    tm = sum(surv[:n], Fraction(0))  # sum_{k=0}^{n-1} P(nu_1 > k)
    print(f"L08 B indep: N={n} E[min(nu_1,N)] = {float(tm):.6f}  (exact {tm})")
print("L08 B exact N=16 check 179587/32768:", sum(surv[:16], Fraction(0)) == Fraction(179587, 32768))

# L08 Part A: P(nu_3 <= 12) and P(S_12 >= 3) by DP
def hit_counts(level: int, n: int) -> tuple[int, int]:
    surv_k = first_passage_survival(level, n)
    hit = (1 - surv_k[n]) * 2**n
    # endpoint >= level by DP over positions (no absorption)
    dist = {0: Fraction(1)}
    for _ in range(n):
        nxt: dict[int, Fraction] = {}
        for pos, p in dist.items():
            for s in (1, -1):
                nxt[pos + s] = nxt.get(pos + s, Fraction(0)) + p / 2
        dist = nxt
    end = sum((p for pos, p in dist.items() if pos >= level), Fraction(0)) * 2**n
    return int(hit), int(end)

h, e = hit_counts(3, 12)
print(f"L08 A indep: count nu_3<=12 = {h}/4096 = {h/4096:.6f}; count S_12>=3 = {e}/4096 = {e/4096:.6f}")

# ---- L07 Part A: tail probabilities by DP on walk endpoints and running max (independent)
def max_tail_dp(n: int, m: int) -> int:
    # states (position, running max capped at m) -> count
    st: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, mx), c in st.items():
            for s in (1, -1):
                q = pos + s
                key = (q, max(mx, q) if max(mx, q) < m else m)
                nxt[key] = nxt.get(key, 0) + c
        st = nxt
    return sum(c for (pos, mx), c in st.items() if mx >= m)

for n in (4, 16):
    m = math.isqrt(n)
    print(f"L07 A indep: N={n} m={m} P(M_N>=m) = {max_tail_dp(n, m)}/{2**n} = {max_tail_dp(n, m)/2**n:.6f}")
# identity check on the enumerated range by DP
ok = 0; tot = 0
for n in range(1, 13):
    for m in range(1, n + 1):
        end_ge = 0; end_gt = 0
        st = {0: 1}
        for _ in range(n):
            nxt = {}
            for pos, c in st.items():
                for s in (1, -1):
                    nxt[pos + s] = nxt.get(pos + s, 0) + c
            st = nxt
        end_ge = sum(c for pos, c in st.items() if pos >= m)
        end_gt = sum(c for pos, c in st.items() if pos > m)
        tot += 1
        ok += max_tail_dp(n, m) == end_ge + end_gt
print(f"L07 A indep: identity by DP holds for {ok} of {tot} pairs")

# ---- L07 Part B/C: same seeded paths, explicit loops, independent of lab helper functions
FINE, PATHS, SEED = 256, 400, 20260507
rng = random.Random(SEED)
scale = math.sqrt(1.0 / FINE)
grids = (4, 16, 64, 256)
maxes = {g: [] for g in grids}
for _ in range(PATHS):
    x = 0.0
    walk = [0.0]
    for _ in range(FINE):
        x += rng.gauss(0.0, scale)
        walk.append(x)
    for g in grids:
        stride = FINE // g
        best = -1e300
        for j in range(0, FINE + 1, stride):
            if walk[j] > best:
                best = walk[j]
        maxes[g].append(best)

def phi(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2))

closed = 2 * (1 - phi(1.0))
viol = sum(1 for a, b in ((4, 16), (16, 64), (64, 256)) for u, v in zip(maxes[a], maxes[b]) if u > v)
print("L07 B indep: violations", viol)
for g in grids:
    ind = [1.0 if v >= 1.0 else 0.0 for v in maxes[g]]
    p = sum(ind) / PATHS
    var = sum((v - p) ** 2 for v in ind) / (PATHS - 1)
    se = math.sqrt(var / PATHS)
    print(f"L07 B indep: N={g} count={int(sum(ind))} p={p:.4f} se={se:.4f} diff={p-closed:+.4f}")
target = math.sqrt(2 / math.pi)
for g in grids:
    mu = sum(maxes[g]) / PATHS
    var = sum((v - mu) ** 2 for v in maxes[g]) / (PATHS - 1)
    se = math.sqrt(var / PATHS)
    print(f"L07 C indep: N={g} mean={mu:.4f} se={se:.4f} diff={mu-target:+.4f} (unrounded diff {mu-target:+.6f})")
print("L07 C indep: 256-step gap in SE units:", round((target - sum(maxes[256]) / PATHS) / math.sqrt(sum((v - sum(maxes[256]) / PATHS) ** 2 for v in maxes[256]) / (PATHS - 1) / PATHS), 4))
print("L07 closed form 2(1-Phi(1)) unrounded:", f"{closed:.10f}", " target sqrt(2/pi):", f"{target:.10f}")

# ---- L08 Part C: independent seeded walks (SEED 20260508), explicit loop, capped at 256
rng2 = random.Random(20260508)
capped = []
for _ in range(1000):
    pos = 0; first = 256
    for k in range(1, 257):
        pos += 1 if rng2.random() < 0.5 else -1
        if pos >= 1:
            first = k
            break
    capped.append(first)
for n, exact in ((16, 5.480560302734375), (64, 11.815731), (256, 24.557203)):
    vals = [min(c, n) for c in capped]
    mu = sum(vals) / 1000
    var = sum((v - mu) ** 2 for v in vals) / 999
    se = math.sqrt(var / 1000)
    print(f"L08 C indep: N={n} mean={mu:.4f} se={se:.4f} z={(mu-exact)/se:+.4f}")

# ---- L08 Part D and interpretation numbers
for H in (1.0, 2.0):
    cdf = math.erfc(1.0 / math.sqrt(2 * H))
    dens = 1.0 / (math.sqrt(2 * math.pi) * H ** 1.5) * math.exp(-1.0 / (2 * H))
    print(f"L08 D indep: H={H} cdf={cdf:.10f} dens={dens:.10f}")
print("L08 E3 density H=2 unrounded:", f"{1/(math.sqrt(2*math.pi)*2**1.5)*math.exp(-0.25):.10f}")
print("L08 E1 odd counts sum:", 512 + 384 + 288 + 224 + 180)
print("L08 pairs: sum 2^n n=1..12 =", sum(2**n for n in range(1, 13)), " sum n2^n =", sum(n * 2**n for n in range(1, 13)))
print("L07 E2 binomials:", sum(math.comb(16, u) for u in range(10, 17)), sum(math.comb(16, u) for u in range(11, 17)))
print("L07 E3: 33759/63840000 sqrt =", f"{math.sqrt(33759/63840000):.6f}")
