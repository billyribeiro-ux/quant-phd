"""Independent re-derivation (stdlib only, written by the round-2 verifier, not from the lab code) of every number
that a BK4-d card states from Lab 1 of L01, L02, L03 and L05, and of the cards' closed-form claims.

Usage: python3 -I ledgers/BK4/scripts/BK4-d-r2/rederive_numbers_r2.py
Each line prints CHECK name: value and OK/MISMATCH against the number the card or lesson states.
"""
import random
from fractions import Fraction
from itertools import product

fails = 0


def check(name, got, want):
    global fails
    ok = got == want
    fails += 0 if ok else 1
    print(f"{'OK      ' if ok else 'MISMATCH'} {name}: got {got}, card/lesson states {want}")


# ---------- L01: one seeded day, seed 20260, 12 payments, 3 banks ----------
rng = random.Random(20260)
day = []
for seq in range(1, 13):
    s, r = rng.sample(range(3), 2)
    dollars = rng.randint(100, 5000)
    day.append((seq, s, r, 100 * dollars))
for seq, s, r, amt in day:
    pass
bal = {b: 0 for b in range(3)}
low = {b: 0 for b in range(3)}
where = {b: None for b in range(3)}
for seq, s, r, amt in day:
    bal[s] -= amt
    bal[r] += amt
    for b in range(3):
        if bal[b] < low[b]:
            low[b] = bal[b]
            where[b] = seq
net = {b: sum(a for _, s2, r2, a in day if r2 == b) - sum(a for _, s2, r2, a in day if s2 == b) for b in range(3)}
need = {b: -low[b] for b in range(3)}
debit = {b: max(0, -net[b]) for b in range(3)}
gross = sum(a for *_, a in day)
print("L01 running sum of Bank A (index 0 = A):")
runA = 0
for seq, s, r, amt in day:
    if s == 0:
        runA -= amt
    elif r == 0:
        runA += amt
    print(f"   after payment {seq:2d}: {runA}")
check("L01 Bank A RTGS need (c011)", need[0], 112500)
check("L01 Bank A net (c011, c014)", net[0], 379800)
check("L01 Bank A DNS debit (c011)", debit[0], 0)
check("L01 Bank A running minimum first reached after payment (c011 says 10)", where[0], 10)
check("L01 Bank B RTGS need (c010)", need[1], 1533900)
check("L01 Bank B DNS debit (c010, c012)", debit[1], 1533900)
check("L01 Bank C RTGS need (c010 family)", need[2], 0)
check("L01 Bank C net (c014 context)", net[2], 1154100)
check("L01 gross value (c012)", gross, 2841600)
check("L01 moved under DNS (c012)", sum(debit.values()), 1533900)
check("L01 share 1533900/2841600 to 4 dp (c012: 0.5398)", round(Fraction(1533900, 2841600) * 10000) / 10000, 0.5398)
check("L01 sum of net positions is zero (Prop 2.3)", sum(net.values()), 0)

# ---------- L02: six trades, four members, seed 2026 ----------
rng = random.Random(2026)
trades = []
for seq in range(1, 7):
    p_, r_ = rng.sample(range(4), 2)
    dollars = rng.randint(500, 20000)
    trades.append((p_, r_, 100 * dollars))
G = sum(a for *_, a in trades)
rec = [sum(a for _, r_, a in trades if r_ == m) for m in range(4)]
pay = [sum(a for p_, _, a in trades if p_ == m) for m in range(4)]
n = [rec[m] - pay[m] for m in range(4)]
A = sum(max(0, x) for x in n)
check("L02 gross notional (c092 = 7596300)", G, 7596300)
check("L02 sum of receivables = G (c092)", sum(rec), 7596300)
check("L02 netted amount A (c031 = 5093600)", A, 5093600)
check("L02 sum of positive net = sum of payers' negative net (Prop 2.2c)", sum(max(0, -x) for x in n), 5093600)
check("L02 reduction bps floored (c028 family; Lab 1 Part D says 3294)", (10000 * (G - A)) // G, 3294)
check("L02 net obligations sum to zero (Prop 2.2b)", sum(n), 0)

# Example 2.4 (card c027, c028)
G4 = 230
A4 = 50
check("L02 Example 2.4 reduction bps (c028 = 7826)", (10000 * 180) // 230, 7826)
check("L02 Example 2.4 A (c027 = 50)", max(0, 20) + max(0, 30), 50)

# ---------- L03: Part A fixture and Part B sizing ----------
def waterfall(L, im_d, df_d, K, surv_df):
    a1 = min(L, im_d)
    a2 = min(L - a1, df_d)
    a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    D = sum(surv_df.values())
    pay = {}
    unc = 0
    if Z >= D:
        pay = dict(surv_df)
        unc = Z - D
    else:
        pay = {i: (Z * df) // D for i, df in surv_df.items()}
        left = Z - sum(pay.values())
        for i in sorted(surv_df):
            if left == 0:
                break
            if surv_df[i] > 0:
                pay[i] += 1
                left -= 1
    return a1, a2, a3, Z, pay, unc


# Example 1.5 (c043)
a1, a2, a3, Z, pay, unc = waterfall(200, 100, 50, 30, {1: 40, 2: 60})
check("L03 Ex 1.5 residual (c043 says 20)", Z, 20)
check("L03 Ex 1.5 member 1 pays (c043 = 8)", pay[1], 8)
check("L03 Ex 1.5 member 2 pays (c043 = 12)", pay[2], 12)
check("L03 Ex 1.5 uncovered (c043 says 0)", unc, 0)
# Example 1.6 (c044)
a1, a2, a3, Z, pay, unc = waterfall(2, 0, 0, 0, {1: 1, 2: 1, 3: 1})
check("L03 Ex 1.6 residual 2: member 1 pays 1 (c044)", pay[1], 1)
check("L03 Ex 1.6 residual 2: member 2 pays 1 (c044)", pay[2], 1)
check("L03 Ex 1.6 residual 2: member 3 pays 0 (c044)", pay[3], 0)

rng = random.Random(2026)
im = {i: rng.randint(1000, 5000) for i in (1, 2, 3, 4)}
df = {i: rng.randint(100, 900) for i in (1, 2, 3, 4)}
capital = rng.randint(500, 2000)
losses = [rng.randint(0, 3000) for _ in range(200)]
S = len(losses)


def cover(M):
    c = sum(1 for L in losses if L <= M)
    return (10000 * c) // S


def sized(t):
    k = -((-t * S) // 10000)
    return sorted(losses)[k - 1], k


for t, want_margin, want_k in ((9900, 2961, 198), (9975, 2992, 200)):
    m, k = sized(t)
    check(f"L03 Part B k for {t} bps (c049/c050 family)", k, want_k)
    check(f"L03 Part B sized margin for {t} bps", m, want_margin)
    brute = next(M for M in range(0, 3001) if cover(M) >= t)
    check(f"L03 Part B brute-force margin for {t} bps", brute, want_margin)
    if t == 9900:
        check("L03 cover at 2961 is 9900 bps (c049)", cover(2961), 9900)
        check("L03 cover one cent below 2961 is 9850 bps (lab)", cover(2960), 9850)
    else:
        check("L03 cover at 2992 is 10000 bps (c050)", cover(2992), 10000)
        check("L03 cover one cent below 2992 is 9950 bps (lab)", cover(2991), 9950)
check("L03 Example 2.5 k at 9900 with S=200 (c048 = 198)", Fraction(9900 * 200, 10000), 198)

# ---------- L05: closed forms and enumeration (c086, c087, c090, c094, c085, c084) ----------
p = Fraction(1, 8)
kappa = 2500
ell = (1, 2, 4)
mean_closed = p * kappa * sum(ell)
check("L05 E[C] closed form (c086 = 4375/2)", mean_closed, Fraction(4375, 2))
check("L05 rounded half up (c094 = 2188)", int(mean_closed + Fraction(1, 2)), 2188)
ind = Fraction(0)
for x in product((0, 1), repeat=3):
    P = Fraction(1)
    for xi in x:
        P *= p if xi else 1 - p
    ind += P * kappa * sum(l * xi for l, xi in zip(ell, x))
check("L05 enumeration E[C] independent (c086)", ind, Fraction(4375, 2))
var4 = Fraction(0)
mu4 = Fraction(0)
outcomes4 = [(1 - p, 0), (p, kappa * sum(ell))]
mu4 = sum(q * c for q, c in outcomes4)
var4 = sum(q * c * c for q, c in outcomes4) - mu4 * mu4
check("L05 Var under A4 (c087 = 133984375/4)", var4, Fraction(133984375, 4))
var3 = Fraction(0)
mu3 = Fraction(0)
outs3 = []
for x in product((0, 1), repeat=3):
    P = Fraction(1)
    for xi in x:
        P *= p if xi else 1 - p
    outs3.append((P, kappa * sum(l * xi for l, xi in zip(ell, x))))
mu3 = sum(q * c for q, c in outs3)
var3 = sum(q * c * c for q, c in outs3) - mu3 * mu3
check("L05 Var under A3 (c087 = 57421875/4)", var3, Fraction(57421875, 4))
check("L05 mean under A3 equals mean under A4 (c088)", mu3, mu4)
check("L05 Var4 - Var3 = 2 kappa^2 p(1-p) sum_{i<j} l_i l_j (c083)", var4 - var3,
      2 * kappa**2 * p * (1 - p) * sum(ell[i] * ell[j] for i in range(3) for j in range(i + 1, 3)))
check("L05 Var4 - Var3 in square cents (lesson E2 = 19140625)", var4 - var3, 19140625)
check("L05 P(no failure) under A3 (c084/c085 = 343/512)", (1 - p) ** 3, Fraction(343, 512))
check("L05 P(no failure) under A4 (c084 = 1-p = 7/8)", 1 - p, Fraction(7, 8))
check("L05 P(at least one) A3 (c085 = 169/512)", 1 - (1 - p) ** 3, Fraction(169, 512))
check("L05 P(at least one) A4 (c085 = 1/8 = 64/512)", p, Fraction(64, 512))
check("L05 3p = 192/512 (c089)", 3 * p, Fraction(192, 512))
check("L05 Part C closed form equal delays 2 (c090 = 1875)", p * kappa * (2 + 2 + 2), 1875)

print()
print("MISMATCH count:", fails)
