"""Independent re-derivation of every printed number in project.html (Labs 1-3 and exemplar B), from the spec.

Written from the page's rules, not from reference.py. Usage: rederive_r6.py (stdlib only, run with -I)."""
import random
from fractions import Fraction
import math

MARGIN = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}
FUND = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}
K_CAP = 20_000
D_ID = 2

def layers(L, im, df, k):
    a1 = min(L, im); a2 = min(L - a1, df); a3 = min(L - a1 - a2, k); R = L - a1 - a2 - a3
    return a1, a2, a3, R

def survivors_pay(R, dfs):  # dfs: dict id->DF for survivors, ids ascending
    D = sum(dfs.values())
    if R >= D:
        return dict(dfs), R - D
    sh = {i: R * dfs[i] // D for i in dfs}
    left = R - sum(sh.values())
    for i in sorted(dfs):
        if left > 0 and dfs[i] > 0:
            sh[i] += 1; left -= 1
    assert left == 0
    return sh, 0

surv = {i: FUND[i] for i in FUND if i != D_ID}
a1, a2, a3, R = layers(80_000, MARGIN[D_ID], FUND[D_ID], K_CAP)
sh, unc = survivors_pay(R, surv)
print("lab1 layers", a1, a2, a3, "residual", R, "pool", sum(surv.values()))
print("lab1 floored shares", {i: R * surv[i] // sum(surv.values()) for i in surv}, "survivor payments", sh, "uncovered", unc)
print("lab1 conservation", a1 + a2 + a3 + sum(sh.values()) + unc == 80_000)

rng = random.Random(1)
losses = [rng.randint(0, 120_000) for _ in range(40)]
S = len(losses)
print("S", S, "largest", max(losses), "sum", sum(losses))
def k_of(t):  # exact fraction, rounded up
    return math.ceil(Fraction(t * S, 10_000))
def cover(M):  # floored
    return 10_000 * sum(1 for x in losses if x <= M) // S
srt = sorted(losses)
print("lab1 exact position 9550:", Fraction(9550 * S, 10_000), float(Fraction(9550 * S, 10_000)), "k", k_of(9550))
for t in (9000, 9500, 9550, 9750):
    k = k_of(t); M = srt[k - 1]
    print(f"target {t}: k {k} margin {M} cover {cover(M)} cover-1 {cover(M - 1)} exact {Fraction(t*S,10000)}")
# brute force over whole-cent margins (independent: smallest M with cover >= t, scanning integers)
def brute(t):
    for M in range(0, max(losses) + 1):
        if cover(M) >= t:
            return M
for t in (9000, 9500, 9750):
    print("brute", t, brute(t))
# part C
margin_for = {t: srt[k_of(t) - 1] for t in (9000, 9500, 9750)}
fund_s = sum(surv.values())
for t in (9500, 9000):
    M = margin_for[t]
    pm = sum(1 for x in losses if x > M)
    pf = sum(1 for x in losses if x > M + FUND[D_ID])
    pc = sum(1 for x in losses if x > M + FUND[D_ID] + K_CAP)
    ps = sum(1 for x in losses if x > M + FUND[D_ID] + K_CAP + fund_s)
    print(f"partC target {t} margin {M} past margin {pm} past fund {pf} past capital {pc} past survivors {ps}")
print("difference 111074-105154 =", 111074 - 105154, "; 9500-9000 =", 9500 - 9000)
# Lab 1 layer-order table and fixtures (page rows)
fx_im, fx_df, fx_k = 100, 50, 30
fx_surv = {1: 40, 2: 60}
rows = []
for L in (80, 100, 120, 150, 151, 170, 180, 181, 200, 205, 300):
    a1, a2, a3, R = layers(L, fx_im, fx_df, fx_k)
    sh, unc = survivors_pay(R, fx_surv)
    rows.append((L, a1, a2, a3, sh[1], sh[2], unc))
for r in rows:
    print("fixture", r)
# remainder fixture
for L in (1, 2, 4):
    a1, a2, a3, R = layers(L, 0, 0, 0)
    sh, unc = survivors_pay(R, {1: 1, 2: 1, 3: 1})
    print("remainder", L, sh, unc)
# sizing fixtures
def mfc(ls, t):
    s = sorted(ls); n = len(ls); return s[math.ceil(Fraction(t * n, 10000)) - 1]
print("sizing", mfc([10,20,30,40,50], 8000), mfc([10,20,30,40,50], 8001), mfc([10,20,30,40,50], 10000), mfc([10,20,30,40], 5000))
def cov(ls, M): return 10_000 * sum(1 for x in ls if x <= M) // len(ls)
print("cover fixtures", cov([1,5,9], 4), cov([1,2,9], 2), Fraction(20000, 3), float(Fraction(20000, 3)))
# exemplar B arithmetic
print("exemplar B: 4000 residual, 1334+1666+1000 =", 1334 + 1666 + 1000, "; 80000 =", 50000 + 6000 + 20000 + 4000)
print("exemplar B: pool 4000+5000+3000 =", 4000 + 5000 + 3000, "; (R*DF)//D 1333,1666,1000:", 4000*4000//12000, 4000*5000//12000, 4000*3000//12000)
print("Lab3 hypothesis checks: 20000 margin only; 55000 -> margin 50000, fund 5000:", min(55000,50000), min(55000-50000,6000))
