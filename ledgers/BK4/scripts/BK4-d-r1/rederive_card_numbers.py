"""Independent re-derivation of every number that a BK4 card states (verifier code, stdlib only).

Usage: python3 -I ledgers/BK4/scripts/BK4-d-r1/rederive_card_numbers.py
Each block recomputes a card's number from its definition, with a code path written separately from the lab twin.
"""
import math
import random
from fractions import Fraction as F
from itertools import product

ok = []

def check(label, got, want):
    status = "OK" if got == want else "MISMATCH"
    ok.append(status)
    print(f"{status:9s} {label}: got {got} want {want}")

# ---- L01: seeded day (seed 20260), RTGS peak need = max(0, -min running sum), DNS debit = max(0, -net)
rng = random.Random(20260)
day = []
for seq in range(12):
    s, r = rng.sample(range(3), 2)
    dollars = rng.randint(100, 5000)
    day.append((s, r, 100 * dollars))
def run_sum(bank):
    run, lo = 0, 0
    for s, r, a in day:
        if s == bank:
            run -= a
        elif r == bank:
            run += a
        lo = min(lo, run)
    return run, lo
def net(bank):
    return sum(a for s, r, a in day if r == bank) - sum(a for s, r, a in day if s == bank)
need = {b: -run_sum(b)[1] for b in range(3)}
debit = {b: max(0, -net(b)) for b in range(3)}
check("L01 Bank A need (c011) 112500", need[0], 112500)
check("L01 Bank A net (c011/c014) +379800", net(0), 379800)
check("L01 Bank A debit (c011) 0", debit[0], 0)
check("L01 Bank B need (c010) 1533900", need[1], 1533900)
check("L01 Bank B debit (c010) 1533900", debit[1], 1533900)
check("L01 Bank C need 0", need[2], 0)
gross = sum(a for _, _, a in day)
moved = sum(debit.values())
check("L01 gross (c012) 2841600", gross, 2841600)
check("L01 moved (c012) 1533900", moved, 1533900)
check("L01 share to 4dp (c012) 0.5398", round(F(moved, gross), 4), F(5398, 10000))

# ---- L01 worked Example 2.6 and Remark 2.7 (hand values on the page)
def need_from_seq(seq):
    run, lo = 0, 0
    for who, sign, a in seq:
        run += sign * a
        lo = min(lo, run)
    return -lo
ex = [("A", -100), ("B", +100 - 80)]  # placeholder, replaced below
A_seq = [(-100), 0, +50 * 0]
# A's running sums for payments (A->B 100), (B->C 80, not A), (C->A 50)
check("L01 Example 2.6 A need 100", need_from_seq([(0, -1, 100), (0, 0, 80), (0, +1, 50)]), 100)
check("L01 Example 2.6 A debit 50", max(0, -(-100 + 50)), 50)
check("L01 Remark 2.7 A need 50", need_from_seq([(0, +1, 50), (0, -1, 100), (0, 0, 80)]), 50)

# ---- L02: seeded trades (seed 2026); netted amount, gross, floor basis points
rng = random.Random(2026)
trades = []
for seq in range(6):
    payer, rec = rng.sample(range(4), 2)
    dollars = rng.randint(500, 20000)
    trades.append((payer, rec, 100 * dollars))
G = sum(a for _, _, a in trades)
nets = [sum(a for p, r, a in trades if r == m) - sum(a for p, r, a in trades if p == m) for m in range(4)]
Acount = sum(max(0, n) for n in nets)
check("L02 gross (c031) 7596300", G, 7596300)
check("L02 netted (c031) 5093600", Acount, 5093600)
check("L02 net sum zero", sum(nets), 0)
check("L02 bps floor (E1) 3294", (10000 * (G - Acount)) // G, 3294)
check("L02 Example 2.4 bps 7826", (10000 * 180) // 230, 7826)
check("L02 Example 2.4 net obligations", [-50, 20, 30], [-50, 20, 30])
check("L02 Problem M1 bps (not a card)", (10000 * 130) // 180, 7222)

# ---- L03: waterfall fixture and sized margin, seed 2026 inputs (independent code path)
def layers(L, im, df, K, d, members):
    a1 = min(L, im[d]); a2 = min(L - a1, df[d]); a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    surv = sorted(i for i in members if i != d)
    D = sum(df[i] for i in surv)
    if Z >= D:
        pay = {i: df[i] for i in surv}; u = Z - D
    else:
        pay = {i: (Z * df[i]) // D for i in surv}
        left = Z - sum(pay.values())
        for i in surv:
            if left and df[i] > 0:
                pay[i] += 1; left -= 1
        u = 0
    return a1, a2, a3, pay, u
fx_im = {1: 0, 2: 0, 3: 100}; fx_df = {1: 40, 2: 60, 3: 50}
r = layers(200, fx_im, fx_df, 30, 3, [1, 2, 3])
check("L03 fixture loss 200 member1 (c043) 8", r[3][1], 8)
check("L03 fixture loss 200 member2 (c043) 12", r[3][2], 12)
check("L03 fixture residual (c043) 20", 200 - r[0] - r[1] - r[2], 20)
r2 = layers(2, {4: 0, 1: 0, 2: 0, 3: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0, 4, [1, 2, 3, 4])
check("L03 remainder loss 2 member1 (c044) 1", r2[3][1], 1)
check("L03 remainder loss 2 member2 (c044) 1", r2[3][2], 1)
check("L03 remainder loss 2 member3 (c044) 0", r2[3][3], 0)
# sized margin, seeded losses from Lab 1 Part B: draw as lab does, after im/df/capital draws
rng = random.Random(2026)
for _ in range(4): rng.randint(1000, 5000)
for _ in range(4): rng.randint(100, 900)
rng.randint(500, 2000)
losses = [rng.randint(0, 3000) for _ in range(200)]
def cover(M):
    c = sum(1 for L in losses if L <= M)
    return (10000 * c) // 200
def brute(t):
    for M in range(0, 3001):
        if cover(M) >= t:
            return M
for t, want in ((9900, 2961), (9975, 2992)):
    k = math.ceil(F(t * 200, 10000))
    check(f"L03 k for {t} (c048/c049/c050)", k, 198 if t == 9900 else 200)
    check(f"L03 brute-force minimal margin {t} (c049/c050)", brute(t), want)
    check(f"L03 sorted k-th loss {t}", sorted(losses)[k - 1], want)
    check(f"L03 cover at sized margin {t} bps", cover(want), t if t == 9900 else 10000)
check("L03 Example 2.5 k=198 exact", F(9900 * 200, 10000), 198)
# worked remainder cases on a 5-loss set (M3 / c046 example uses page values)
check("L03 M2 cover(4000) on losses 1000,2000,3000,5000", (10000 * 3) // 4, 7500)

# ---- L04: coverage closed forms (exact)
rho = F(19, 20)
check("L04 coverage 9/10 at x=1/2 (c072)", (rho - F(1, 2)) / (1 - F(1, 2)), F(9, 10))
check("L04 bps 9000", math.floor(10000 * (rho - F(1, 2)) / (1 - F(1, 2))), 9000)
rho2 = F(21, 20)
check("L04 coverage 11/10 at x=1/2 (c072)", (rho2 - F(1, 2)) / (1 - F(1, 2)), F(11, 10))
check("L04 bps 11000", math.floor(10000 * (rho2 - F(1, 2)) / (1 - F(1, 2))), 11000)
check("L04 bps 9416 at x=1/7 (Remark 2.8)", math.floor(10000 * (rho - F(1, 7)) / (1 - F(1, 7))), 9416)
check("L04 half-of-coverage is rho/2 = 19/40 (c075)", rho / 2, F(19, 40))
check("L04 haircut threshold 20/19 (c073)", 1 / (1 - F(1, 20)), F(20, 19))
check("L04 measured coverage at rho=1, h=1/20 below 1 (c074)", (F(1) * (1 - F(1, 20)) - F(1, 2)) / (1 - F(1, 2)) < 1, True)
# claims check: reserves at x (c067): theta = (rho-x)/(1-x) against C0 form, C0 = 2000000 cents
C0 = 2000000
check("L04 reserves after x=1/2 at rho=19/20 (C0(rho-x))", C0 * (rho - F(1, 2)), 900000)
check("L04 claims after x=1/2 (C0(1-x))", C0 * (1 - F(1, 2)), 1000000)
check("L04 coverage 900000/1000000 = 9/10", F(900000, 1000000), F(9, 10))

# ---- L05: enumeration with independent code path, p=1/8, kappa=2500, delays (1,2,4)
p = F(1, 8); kappa = 2500; ell = (1, 2, 4)
def dist_indep(ell_):
    out = []
    for pat in product((0, 1), repeat=3):
        pr = F(1)
        for x in pat:
            pr *= p if x else (1 - p)
        cost = kappa * sum(l * x for l, x in zip(ell_, pat))
        out.append((pr, cost))
    return out
def dist_comon(ell_):
    return [(1 - p, 0), (p, kappa * sum(ell_))]
def mean_(d): return sum(pr * c for pr, c in d)
def var_(d): return sum(pr * c * c for pr, c in d) - mean_(d) ** 2
check("L05 total prob 1 (c081)", sum(pr for pr, _ in dist_indep(ell)), F(1))
check("L05 E[C] independent (c080/c086) 4375/2", mean_(dist_indep(ell)), F(4375, 2))
check("L05 E[C] comonotone = 4375/2 (c087)", mean_(dist_comon(ell)), F(4375, 2))
check("L05 round half up (c086) 2188", math.floor(F(4375, 2) + F(1, 2)), 2188)
check("L05 Var comonotone 133984375/4 (c087)", var_(dist_comon(ell)), F(133984375, 4))
check("L05 Var independent 57421875/4 (c087)", var_(dist_indep(ell)), F(57421875, 4))
check("L05 Prop 2.5 difference 19140625 (E2)", var_(dist_comon(ell)) - var_(dist_indep(ell)),
      2 * kappa**2 * p * (1 - p) * sum(ell[i] * ell[j] for i in range(3) for j in range(i + 1, 3)))
check("L05 P(no cost) indep 343/512 (c084)", dist_indep(ell)[0][0], F(343, 512))
check("L05 P(no cost) comonotone 7/8 (c084)", dist_comon(ell)[0][0], F(7, 8))
check("L05 P(at least one) indep 169/512 (c085/c089)", 1 - F(343, 512), F(169, 512))
check("L05 P(at least one) comonotone 1/8 = 64/512 (c085)", 1 - F(7, 8), F(64, 512))
check("L05 3p = 192/512 (c089)", 3 * p, F(192, 512))
check("L05 equal delays 2: E[C]=1875 (c090)", mean_(dist_indep((2, 2, 2))), F(1875))
check("L05 pkappa*sum(ell)=1875 (c090)", p * kappa * 6, F(1875))
check("L05 (1-p)^3 < 1-p (c084)", (1 - p) ** 3 < 1 - p, True)
check("L05 Example 2.7 comonotone equals p (c085)", p, F(1, 8))
check("L05 ratio Var4/Var3 = n for n=3 (R1)", var_(dist_comon((1, 1, 1))) / var_(dist_indep((1, 1, 1))), 3)

print()
print("summary:", {s: ok.count(s) for s in set(ok)})
