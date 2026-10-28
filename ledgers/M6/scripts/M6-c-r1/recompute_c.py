"""Independent recomputation for M6 slice c (L09-L12). Uses dynamic programming and float Riemann sums, not the lab code."""
from fractions import Fraction as F
import math

def walk_hit_dist(N):
    # distribution of the state (S_k, hit flag) via DP; returns P(tau<=k) for k=0..N, tau = first k>=1 with S_k=+1
    dist = {(0, False): F(1)}
    out = [F(0)]
    cum = []
    hit_by = F(0)
    for k in range(1, N + 1):
        new = {}
        for (s, h), p in dist.items():
            for step in (1, -1):
                ns = s + step
                nh = h or ns == 1
                new[(ns, nh)] = new.get((ns, nh), F(0)) + p / 2
        dist = new
        out.append(sum(p for (s, h), p in dist.items() if h))
    return out

P = walk_hit_dist(10)
print("L09 P(tau<=k) for k=0..10:", [str(x) for x in P])
print("L09 P(tau<=3)=", P[3], " P(tau<=5)=", P[5], float(P[5]), " horizon-5 differs from 5/8:", P[5] != F(5, 8))
# P(tau=3) = P(tau<=3)-P(tau<=2)
print("L09 P(tau=3)=", P[3] - P[2], " P(tau=1)=", P[1])
print("L09 P(tau<=8)=", P[8], float(P[8]), "count of 256 paths:", P[8] * 256)

def ruin_chain(K):
    # exact expectation and outcome probabilities for doubling with capital K, by recursion on wealth
    # state: (bet index k, wealth w); stake 2^(k-1); returns dict outcome->(prob, wealth) and expectation
    res = {}
    def rec(k, w, p):
        stake = 2 ** (k - 1)
        if stake > w:
            res.setdefault(("ruin", w), F(0))
            res[("ruin", w)] += p
            return
        # win
        res.setdefault(("win", w + stake), F(0))
        res[("win", w + stake)] += p / 2
        rec(k + 1, w - stake, p / 2)
    rec(1, K, F(1))
    exp = sum(p * w for (kind, w), p in res.items())
    ruin = sum(p for (kind, w), p in res.items() if kind == "ruin")
    return res, exp, ruin

for K in (1, 6, 10, 100, 1000):
    res, exp, ruin = ruin_chain(K)
    m = (K + 1).bit_length() - 1
    wins = sorted(w for (kind, w) in res if kind == "win")
    ruins = sorted(w for (kind, w) in res if kind == "ruin")
    print(f"L10 K={K} m={m} ruin={ruin} (2^-m={F(1, 2**m)}) win_wealth={wins} ruin_wealth={ruins} E={exp} E==K {exp == K}")

# unbounded doubling: P(tau>n) and expectation of stopped net gain
for n in (1, 2, 3, 5, 10):
    # exact: stopped value = +1 on win at index <= n, -(2^n-1) if all n lose
    p_lose = F(1, 2**n)
    E_stop = (1 - p_lose) * 1 + p_lose * (-(2**n - 1))
    print(f"L10 n={n} P(tau>n)={p_lose} E[D_tau^n]={E_stop} win_part={1-p_lose}")

# L10 K=3 ruin wealth check (claim 'only when K=1')
for K in (1, 3, 7, 15):
    m = (K + 1).bit_length() - 1
    print(f"L10 K={K}: wealth after ruin K+1-2^m = {K + 1 - 2**m}")

# L11: Doob ratios by DP over (S_k, running max) for |S_k|
def doob(N):
    worst = F(0); worst_lam = None; worst_p = None
    # distribution of path (S_N, max_k |S_k| ) by enumeration via DP on (S, M)
    dist = {(0, 0): F(1)}
    for _ in range(N):
        new = {}
        for (s, mx), p in dist.items():
            for st in (1, -1):
                ns = s + st
                key = (ns, max(mx, abs(ns)))
                new[key] = new.get(key, F(0)) + p / 2
        dist = new
    EX = sum(p * abs(s) for (s, mx), p in dist.items())
    for j in range(1, 2 * (N + 1) + 1):
        lam = F(j, 2)
        prob = sum(p for (s, mx), p in dist.items() if mx >= lam)
        if EX == 0:
            continue
        r = lam * prob / EX
        assert prob <= EX / lam
        if r > worst:
            worst, worst_lam, worst_p = r, lam, prob
    return EX, worst, worst_lam, worst_p

for N in (1, 2, 3, 4, 12):
    EX, r, lam, p = doob(N)
    print(f"L11 N={N} E|S_N|={EX} largest_ratio={float(r):.6f} at lambda={lam} P(A)={p}")

# L11 signed walk N=1,2 lambda=1
print("L11 signed N=1: P(max S>=1)=1/2, E S_1=0 ; N=2 P=1/2")

# L12 dyadic error numeric check (independent float Riemann sum)
import numpy as _np  # NOTE: numpy used only for an independent float check, not in any lab
for n in (0, 1, 2, 3):
    x = (_np.arange(2**20) + 0.5) / 2**20
    cell = _np.floor(x * 2**n)
    c = (cell + 0.5) / 2**n
    err = _np.mean((c - x) ** 2)
    print(f"L12 n={n} float E[(M_n-Y)^2]={err:.10f} formula={1/(12*4**n):.10f}")
print("L12 E[M_2^2] exact =", F(21, 64), " 1/3-1/192 =", F(1, 3) - F(1, 192))
print("L12 1/(12*4^10) =", F(1, 12 * 4**10), " 2^-11 =", F(1, 2048))
print("L12 1/192 decimal =", f"{1/192:.8f}")
print("L11 693/768 =", F(693, 768), float(F(693, 768)), " 781/1024 =", float(F(781, 1024)), " ratio=", F(3) * F(781, 1024) / F(693, 256), float(F(3) * F(781, 1024) / F(693, 256)))
