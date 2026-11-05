"""Independent recomputation of every printed figure in the L07 and L08 lab twins (verifier round 13).

Shares no code with the twins: walk counts come from a dynamic programme over (position, running maximum)
with absorbing barriers, Brownian and walk samples are rebuilt with explicit loops using the same
random.Random draw order (the seed and the draw order are the only shared facts), and the normal tail is
checked by a separate Simpson rule. Run as: python -I indep_r13.py
"""

import math
import random
from fractions import Fraction

# ---------- L07 Part A: exact tails by absorbing DP (count paths that stay strictly below m) ----------
def count_max_below(n, m):
    """Number of n-step +-1 walks from 0 whose running maximum over S_0..S_n is < m (m >= 1)."""
    # dp maps position -> count, positions restricted to < m
    dp = {0: 1}
    for _ in range(n):
        new = {}
        for p, c in dp.items():
            for q in (p + 1, p - 1):
                if q < m:
                    new[q] = new.get(q, 0) + c
        dp = new
    return sum(dp.values())


def tail_exact(n, m):
    return Fraction(2**n - count_max_below(n, m), 2**n)


# enumeration check for N <= 12 (brute force over all sequences), level a = 1..N
def brute_pairs(n):
    out = []
    for bits in range(2**n):
        pos = 0
        top = 0
        for i in range(n):
            pos += 1 if (bits >> i) & 1 else -1
            top = max(top, pos)
        out.append((top, pos))
    return out


print("== L07 Part A ==")
ident_ok = 0
checked = 0
for n in range(1, 13):
    pairs = brute_pairs(n)
    for a in range(1, n + 1):
        reached = sum(1 for t, _ in pairs if t >= a)
        ge = sum(1 for _, e in pairs if e >= a)
        gt = sum(1 for _, e in pairs if e > a)
        checked += 1
        ident_ok += reached == ge + gt
        # DP agreement
        assert reached == 2**n - count_max_below(n, a), (n, a)
print(f"identity holds {ident_ok} of {checked}")
for n in (4, 16, 64, 256, 1024):
    m = math.isqrt(n)
    t = tail_exact(n, m)
    print(f"N={n} m={m} P={float(t):.6f} exact_num={t.numerator} den={t.denominator}")

# ---------- L07 Part B and C: seeded Brownian paths, same draw order ----------
FINE = 256
PATHS = 400
rng = random.Random(20260507)
grids = (4, 16, 64, 256)
maxes = {g: [] for g in grids}
scale = math.sqrt(1.0 / FINE)
for _ in range(PATHS):
    path = [0.0]
    for _j in range(FINE):
        path.append(path[-1] + rng.gauss(0.0, scale))
    for g in grids:
        step = FINE // g
        best = path[0]
        for j in range(0, FINE + 1, step):
            if path[j] > best:
                best = path[j]
        maxes[g].append(best)

viol = 0
for coarse, fine in ((4, 16), (16, 64), (64, 256)):
    for c, f in zip(maxes[coarse], maxes[fine]):
        if c > f:
            viol += 1
print("== L07 Part B ==")
print("violations", viol)
closed_tail = 2 * (1 - 0.5 * (1 + math.erf(1 / math.sqrt(2))))
print("closed 2(1-Phi(1)) =", f"{closed_tail:.6f}", repr(closed_tail))
for g in grids:
    ind = [1.0 if m >= 1.0 else 0.0 for m in maxes[g]]
    p = sum(ind) / PATHS
    var = sum((x - p) ** 2 for x in ind) / (PATHS - 1)
    se = math.sqrt(var / PATHS)
    print(f"N={g} count={int(sum(ind))} p={p:.4f} se={se:.4f} diff={p - closed_tail:+.4f}")
print("== L07 Part C ==")
target = math.sqrt(2 / math.pi)
print(f"sqrt(2/pi)={target:.6f}")
for g in grids:
    xs = maxes[g]
    mu = sum(xs) / PATHS
    var = sum((x - mu) ** 2 for x in xs) / (PATHS - 1)
    se = math.sqrt(var / PATHS)
    print(f"N={g} mean={mu:.4f} se={se:.4f} diff={mu - target:+.4f}")

# ---------- L07 Part D ----------
print("== L07 Part D ==")
erfc_val = math.erfc(1 / math.sqrt(2)) / 2
# independent Simpson on [1, 13] with 4000 intervals, using a different density expression
def dens(x):
    return (2 * math.pi) ** -0.5 * math.exp(-0.5 * x * x)
N_S = 4000
h = 12.0 / N_S
s = dens(1.0) + dens(13.0)
for i in range(1, N_S):
    s += (4 if i % 2 else 2) * dens(1.0 + i * h)
s *= h / 3
print(f"erfc {erfc_val:.10f} simpson4000 {s:.10f} diff {abs(erfc_val - s):.3e}")

# ---------- L08 Part A ----------
print("== L08 Part A ==")
pairs_ok = 0
seq_pairs = 0
agree = 0
for n in range(1, 13):
    for a in range(1, n + 1):
        pairs_ok += 1
        cnt = 0
        for bits in range(2**n):
            pos = 0
            top = 0
            first = None
            for k in range(1, n + 1):
                pos += 1 if (bits >> (k - 1)) & 1 else -1
                top = max(top, pos)
                if first is None and pos >= a:
                    first = k
            seq_pairs += 1
            agree += (first is not None) == (top >= a)
            if first is not None and first <= n:
                cnt += 1
        # identity count vs DP
        assert cnt == 2**n - count_max_below(n, a), (n, a)
print(f"pairs {pairs_ok} seq-level pairs {seq_pairs} agree {agree}")
# first passage to 3 at step k, n = 12
n, a = 12, 3
by_k = {k: 0 for k in range(a, n + 1)}
for bits in range(2**n):
    pos = 0
    first = None
    for k in range(1, n + 1):
        pos += 1 if (bits >> (k - 1)) & 1 else -1
        if pos >= a:
            first = k
            break
    if first is not None and first in by_k:
        by_k[first] += 1
print("by step", [by_k[k] for k in range(a, n + 1)])
hits = sum(by_k.values())
print("hits", hits, "P", f"{hits / 2**12:.6f}", "P(S12>=3)", f"{sum(1 for b in range(2**12) if 2*bin(b).count('1')-12>=3)}/4096 = {sum(1 for b in range(2**12) if 2*bin(b).count('1')-12>=3)/4096:.6f}")

# ---------- L08 Part B: P(nu_1 > k) by DP over positions <= 0 for k steps ----------
print("== L08 Part B ==")
def survive_probs(K):
    """Exact P(nu_1 > k) for k = 0..K-1, by DP over positions (stay < 1)."""
    out = []
    dp = {0: 1}  # counts, paths that have stayed below 1 so far, at step 0
    total = 1
    for k in range(K):
        out.append(Fraction(sum(dp.values()), 2**k))
        new = {}
        for p, c in dp.items():
            for q in (p + 1, p - 1):
                if q < 1:
                    new[q] = new.get(q, 0) + c
        dp = new
    return out

sp = survive_probs(256)
for N in (16, 64, 256):
    val = sum(sp[:N])  # sum over k < N of P(nu_1 > k)
    print(f"N={N} E[min(nu1,N)]={float(val):.6f}")

# ---------- L08 Part C: same draw order as the twin (early stop at first hit) ----------
print("== L08 Part C ==")
rng = random.Random(20260508)
caps = []
for _ in range(1000):
    pos = 0
    first = 256
    for k in range(1, 257):
        pos += 1 if rng.random() < 0.5 else -1
        if pos >= 1:
            first = k
            break
    caps.append(first)
for N in (16, 64, 256):
    xs = [float(min(c, N)) for c in caps]
    mu = sum(xs) / len(xs)
    var = sum((x - mu) ** 2 for x in xs) / (len(xs) - 1)
    se = math.sqrt(var / len(xs))
    ex = float(sum(sp[:N]))
    print(f"N={N} mean={mu:.4f} se={se:.4f} exact={ex:.4f} z={(mu - ex) / se:+.2f}")

# ---------- L08 Part D ----------
print("== L08 Part D ==")
def cdf(a, H):
    return math.erfc(a / math.sqrt(2 * H))
for H in (1.0, 2.0):
    a = 1.0
    f = a / (math.sqrt(2 * math.pi) * H ** 1.5) * math.exp(-a * a / (2 * H))
    d = 1e-5
    num = (cdf(a, H + d) - cdf(a, H - d)) / (2 * d)
    print(f"H={H:g} cdf={cdf(a, H):.6f} dens={f:.6f} numeric={num:.6f} absdiff={abs(f-num):.2e}")
print("erfc(1/sqrt2)", f"{math.erfc(1/math.sqrt(2)):.10f}", "1-Phi(1)", f"{0.5*math.erfc(1/math.sqrt(2)):.10f}")
print("H=1 cdf 10dp", f"{cdf(1.0,1.0):.10f}", "H=2 cdf", f"{cdf(1.0,2.0):.10f}")
