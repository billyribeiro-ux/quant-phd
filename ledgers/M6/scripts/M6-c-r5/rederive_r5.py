# Independent re-derivation of the numbers printed or claimed in M6 L09-L12 (verifier round 5).
from fractions import Fraction as F
import itertools, math

# L09: fair walk, 8 steps, hitting time of +1
N = 8
paths = list(itertools.product((-1, 1), repeat=N))
def hit(p):
    s = 0
    for k, x in enumerate(p, 1):
        s += x
        if s == 1:
            return k
    return None
for k in range(N + 1):
    cnt = sum(1 for p in paths if (h := hit(p)) is not None and h <= k)
    print("L09 k", k, "hit_by_k", cnt, F(cnt, 256))
print("L09 P(tau=3) =", F(sum(1 for p in paths if hit(p) == 3), 256), "(M1 claims 1/8)")

# L10: doubling with capital K; m = floor(log2(K+1))
for K in (1, 6, 10, 100, 1000):
    m = (K + 1).bit_length() - 1
    ruin = F(1, 2**m)
    wealth_ruin = K + 1 - 2**m
    e = (1 - ruin) * (K + 1) + ruin * wealth_ruin
    print("L10 K", K, "m", m, "ruin", ruin, "win_wealth", K + 1, "ruin_wealth", wealth_ruin, "E", e)
for n in (1, 2, 3, 5, 10):
    p_gt = F(1, 2**n)
    e_stopped = (1 - p_gt) * 1 + p_gt * (-(2**n - 1))
    print("L10 n", n, "P(tau>n)", float(p_gt), "E[D_tau^n]", e_stopped, "win_part", 1 - p_gt)

# L11: Doob ratio for |S_k| at N = 12, lambda = 3, and E|S_N| values
def ratio_stats(n):
    sample = list(itertools.product((-1, 1), repeat=n))
    w = F(1, 2**n)
    ps = lambda p: [sum(p[:k]) for k in range(n + 1)]
    e_last = sum(w * abs(ps(p)[n]) for p in sample)
    best = (F(0), None, None)
    for j in range(1, 2 * (n + 1) + 1):
        lam = F(j, 2)
        pa = w * sum(1 for p in sample if max(abs(s) for s in ps(p)) >= lam)
        r = lam * pa / e_last
        if r > best[0]:
            best = (r, lam, pa)
    return e_last, best
for n in (1, 2, 4, 12):
    e, (r, lam, pa) = ratio_stats(n)
    print("L11 N", n, "E|S_N|", e, "largest_ratio", float(r), "at", lam, "P(A)", pa)
print("L11 781/924 =", float(F(781, 924)), " 231/256 =", F(231, 256))
print("L11 atoms total", sum(2**k for k in range(12)))
print("L11 signed N=1,2 at lambda=1:", [(n, F(sum(1 for p in itertools.product((-1,1),repeat=n) if max(sum(p[:k]) for k in range(n+1)) >= 1), 2**n), 0) for n in (1, 2)])

# L12: dyadic martingale errors and second moments
for n in range(0, 11):
    cells = 2**n
    err = sum(F(1, 1) * 0 for _ in range(1))  # placeholder replaced below
    err = F(0)
    sec = F(0)
    for j in range(cells):
        a, b = F(j, cells), F(j + 1, cells)
        c = (a + b) / 2
        err += ((b - c) ** 3 - (a - c) ** 3) / 3
        sec += c * c * (b - a)
    assert err == F(1, 12 * 4**n) and sec == F(1, 3) - F(1, 12 * 4**n)
print("L12 dyadic formulas verified for n = 0..10; n=10 error", F(1, 12 * 4**10), "largest grid error", F(1, 2**11))
print("L12 M2 E[M_2^2] =", F(84, 256), "= 21/64:", F(84, 256) == F(21, 64), "; 1/3-1/192 =", F(1, 3) - F(1, 192))
print("L12 quiz 21/64 =", float(F(21, 64)), " 693/256 =", float(F(693, 256)), " 1/192 =", float(F(1, 192)))
