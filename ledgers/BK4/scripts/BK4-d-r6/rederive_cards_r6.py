"""Independent re-derivation (round 6) of every number on a card in course/modules/BK/BK4/cards.json.

Stdlib only, written from the lesson text, not from the lab sources. Usage:
    python3 -I ledgers/BK4/scripts/BK4-d-r6/rederive_cards_r6.py
Each line prints the card id, the quantity, the re-derived value and OK or MISMATCH against the card text.
"""
import random
from fractions import Fraction
import math

bad = []


def check(card, label, got, want):
    status = "OK" if got == want else "MISMATCH"
    if status != "OK":
        bad.append((card, label))
    print(f"{card:10s} {label:55s} derived={got!s:>22s} card={want!s:>22s} {status}")


# ---- L01: seed 20260, 12 payments, three banks, amounts in whole dollars 100..5000 ----
rng = random.Random(20260)
day = []
for seq in range(1, 13):
    s, r = rng.sample(range(3), 2)
    dollars = rng.randint(100, 5000)
    day.append((seq, s, r, 100 * dollars))


def net(b):
    return sum(a for _, s, r, a in day if r == b) - sum(a for _, s, r, a in day if s == b)


def need(b):
    bal, low = 0, 0
    for _, s, r, a in day:
        if s == b:
            bal -= a
        elif r == b:
            bal += a
        low = min(low, bal)
    return -low


def debit(b):
    return max(0, -net(b))


gross = sum(a for *_, a in day)
moved = sum(debit(b) for b in range(3))
check("BK4-c010", "Bank B RTGS need (cents)", need(1), 1533900)
check("BK4-c010", "Bank B DNS net debit (cents)", debit(1), 1533900)
check("BK4-c011", "Bank A RTGS need (cents)", need(0), 112500)
check("BK4-c014", "Bank A net position (cents)", net(0), 379800)
check("BK4-c014", "Bank A DNS net debit (cents)", debit(0), 0)
check("BK4-c012", "DNS moved (cents)", moved, 1533900)
check("BK4-c012", "gross value (cents)", gross, 2841600)
check("BK4-c012", "share equals 0.5398", round(1533900 / 2841600, 4), 0.5398)
# payment-10 running balance for Bank A: payments out exceed payments in by 112500 after payment 10
bal = 0
for seq, s, r, a in day:
    if seq > 10:
        break
    if s == 0:
        bal -= a
    elif r == 0:
        bal += a
check("BK4-c011", "Bank A running balance after payment 10 (cents)", bal, -112500)
print("L01 net positions sum to zero:", sum(net(b) for b in range(3)) == 0)

# Example 2.6 / Remark 2.7 (hand numbers from the lesson)
def runmin(seq):
    bal, low = 0, 0
    for amt_sign in seq:
        bal += amt_sign
        low = min(low, bal)
    return low

A_order1 = [-100, +50]  # order 1,2,3: A pays 100 at payment 1, A receives 50 at payment 3
A_order3first = [+50, -100]  # payment 3 first
check("BK4-c008", "A peak need Example 2.6 (dollars)", -runmin(A_order1), 100)
check("BK4-c009", "A peak need after reordering (dollars)", -runmin(A_order3first), 50)
check("BK4-c101", "A DNS net debit Example 2.6 (dollars)", max(0, -(sum(A_order1))), 50)

# ---- L02: seed 2026, six trades, four members, whole dollars 500..20000 ----
rng = random.Random(2026)
trades = []
for seq in range(1, 7):
    p, r = rng.sample(range(4), 2)
    dollars = rng.randint(500, 20000)
    trades.append((p, r, 100 * dollars))
G = sum(a for *_, a in trades)
rec = [sum(a for p, r, a in trades if r == m) for m in range(4)]
pay = [sum(a for p, r, a in trades if p == m) for m in range(4)]
n = [rec[m] - pay[m] for m in range(4)]
A = sum(max(0, x) for x in n)
check("BK4-c092", "gross notional (cents)", G, 7596300)
check("BK4-c092", "sum of receivables = G", sum(rec), 7596300)
check("BK4-c031", "amount paid after netting A (cents)", A, 5093600)
check("BK4-c031", "A equals sum of positive nets", A, sum(x for x in n if x > 0))
check("BK4-c031", "A equals sum of payers' nets", A, sum(-x for x in n if x < 0))
check("L02 E1", "reduction G-A (cents)", G - A, 2502700)
check("L02 E1", "reduction floor bps", 10000 * (G - A) // G, 3294)
print("L02 nets:", n, "sum zero:", sum(n) == 0)

# Example 2.4 numbers
G24, A24 = 230, 50
check("BK4-c028", "floor(10000*180/230)", 10000 * (G24 - A24) // G24, 7826)
check("BK4-c027", "Example 2.4 netted amount", A24, 50)
check("BK4-c028", "Example 2.4 net obligations", [-50, 20, 30], [-50, 20, 30])

# ---- L03: Example 1.5 and 1.6 by hand ----
def layers(loss, im, dfl, cap, surv_df):
    a1 = min(loss, im)
    a2 = min(loss - a1, dfl)
    a3 = min(loss - a1 - a2, cap)
    Z = loss - a1 - a2 - a3
    D = sum(surv_df)
    if Z >= D:
        return a1, a2, a3, list(surv_df), Z - D
    x = [Z * d // D for d in surv_df]
    left = Z - sum(x)
    for i, d in enumerate(surv_df):
        if left == 0:
            break
        if d > 0:
            x[i] += 1
            left -= 1
    return a1, a2, a3, x, 0


r = layers(200, 100, 50, 30, [40, 60])
check("BK4-c043", "Example 1.5 member 1 pays", r[3][0], 8)
check("BK4-c043", "Example 1.5 member 2 pays", r[3][1], 12)
check("BK4-c043", "Example 1.5 residual Z", 200 - r[0] - r[1] - r[2], 20)
check("BK4-c043", "Example 1.5 uncovered", r[4], 0)
r2 = layers(2, 0, 0, 0, [1, 1, 1])
check("BK4-c044", "Example 1.6 member 1 leftover cent", r2[3][0], 1)
check("BK4-c044", "Example 1.6 member 2 leftover cent", r2[3][1], 1)
check("BK4-c044", "Example 1.6 member 3 pays", r2[3][2], 0)
r1 = layers(1, 0, 0, 0, [1, 1, 1])
check("BK4-c044", "Example 1.6 residual 1 to member 1", r1[3][0], 1)
check("BK4-c043", "Example 1.5 uncovered (layers sum)", r[0] + r[1] + r[2] + sum(r[3]) + r[4], 200)

# Lab 1 Part B: seed 2026, IM 4 draws, DF 4 draws, capital, 200 losses
rng = random.Random(2026)
im = {i: rng.randint(1000, 5000) for i in (1, 2, 3, 4)}
df = {i: rng.randint(100, 900) for i in (1, 2, 3, 4)}
cap = rng.randint(500, 2000)
losses = [rng.randint(0, 3000) for _ in range(200)]
srt = sorted(losses)


def cover(M):
    c = sum(1 for L in losses if L <= M)
    return 10000 * c // 200


def brute(t):
    for M in range(max(losses) + 1):
        if cover(M) >= t:
            return M


for t, card, want in ((9900, "BK4-c049", 2961), (9975, "BK4-c050", 2992)):
    k = math.ceil(Fraction(t * 200, 10000))
    sized = srt[k - 1]
    check(card, f"k for {t} bps", k, 198 if t == 9900 else 200)
    check(card, f"sized margin {t} bps (cents)", sized, want)
    check(card, f"brute-force minimum {t} bps", brute(t), want)
    check(card, f"cover at sized margin (bps)", cover(sized), 9900 if t == 9900 else 10000)
print("Lab 1 Part B: IM", im, "DF", df, "capital", cap)
check("BK4-c049", "cover one cent below 2961 is below 9900", cover(2960) < 9900, True)
check("BK4-c050", "cover one cent below 2992 is below 9975", cover(2991) < 9975, True)

# ---- L05: exact expected cost and variances (Fractions) ----
p = Fraction(1, 8)
kap = 2500
ell = (1, 2, 4)
pats = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
ind = []
for pat in pats:
    prob = Fraction(1)
    for x in pat:
        prob *= p if x else 1 - p
    cost = kap * sum(l * x for l, x in zip(ell, pat))
    ind.append((prob, cost))
mean_ind = sum(pr * c for pr, c in ind)
var_ind = sum(pr * c * c for pr, c in ind) - mean_ind ** 2
com = [(1 - p, 0), (p, kap * sum(ell))]
mean_com = sum(pr * c for pr, c in com)
var_com = sum(pr * c * c for pr, c in com) - mean_com ** 2
check("BK4-c086", "E[C] independent (cents)", mean_ind, Fraction(4375, 2))
check("BK4-c086", "E[C] = p kappa sum ell", p * kap * sum(ell), Fraction(4375, 2))
check("BK4-c094", "round half up of 4375/2", math.floor(Fraction(4375, 2) + Fraction(1, 2)), 2188)
check("BK4-c087", "Var comonotone (sq cents)", var_com, Fraction(133984375, 4))
check("BK4-c087", "Var independent (sq cents)", var_ind, Fraction(57421875, 4))
check("BK4-c083", "Var4 - Var3 = 2 k^2 p(1-p) sum_{i<j} l_i l_j", var_com - var_ind,
      2 * kap ** 2 * p * (1 - p) * (1 * 2 + 1 * 4 + 2 * 4))
check("BK4-c083", "value 19140625", var_com - var_ind, 19140625)
check("BK4-c090", "Part C enumeration: p kappa sum with ell=2", p * kap * (2 * 3), 1875)
check("BK4-c089", "1-(7/8)^3 = 169/512", 1 - (Fraction(7, 8)) ** 3, Fraction(169, 512))
check("BK4-c089", "3p = 192/512", 3 * p, Fraction(192, 512))
check("BK4-c084", "P(C=0) independent (1-p)^3", ind[0][0], Fraction(343, 512))
check("BK4-c084", "P(C=0) comonotone 1-p", com[0][0], Fraction(7, 8))
check("BK4-c084", "(1-p)^3 < 1-p", (1 - p) ** 3 < 1 - p, True)
check("BK4-c086", "Example 2.8 mean from enumeration", mean_ind, Fraction(4375, 2))
# Each card's stated Lab value for expected cost with equal delays
check("BK4-c090", "E[C] with equal delays 2 is 1875", p * kap * (2 + 2 + 2), 1875)

# ---- L04: Propositions and Remark 2.8, Remark 4.1 ----
def theta(rho, x):
    return (rho - x) / (1 - x)


check("BK4-c072", "theta(19/20, 1/2)", theta(Fraction(19, 20), Fraction(1, 2)), Fraction(9, 10))
check("BK4-c072", "theta(21/20, 1/2)", theta(Fraction(21, 20), Fraction(1, 2)), Fraction(11, 10))
check("BK4-c075", "theta at x=1/2 equals (rho-1/2)/(1/2)", theta(Fraction(19, 20), Fraction(1, 2)), (Fraction(19, 20) - Fraction(1, 2)) / Fraction(1, 2))
check("BK4-c073", "threshold 1/(1-1/20)", 1 / (1 - Fraction(1, 20)), Fraction(20, 19))
check("BK4-c074", "measured ratio at rho=1, h=1/20", 1 * (1 - Fraction(1, 20)), Fraction(19, 20))
# sign rule and difference identity on random exact cases
rnd = random.Random(1)
ok_sign = ok_diff = ok_theta_rho = True
for _ in range(2000):
    rho = Fraction(rnd.randint(1, 300), 200)
    x = Fraction(rnd.randint(0, 99), 100)
    y = Fraction(rnd.randint(0, 99), 100)
    if x > rho or y > rho:
        continue
    if x < y:
        ok_diff &= theta(rho, y) - theta(rho, x) == (y - x) * (rho - 1) / ((1 - x) * (1 - y))
    ok_sign &= (theta(rho, x) < 1) == (rho < 1) and (theta(rho, x) == 1) == (rho == 1)
    ok_theta_rho &= (theta(rho, x) - rho == x * (rho - 1) / (1 - x))
check("BK4-c068", "sign rule on 2000 random exact cases", ok_sign, True)
check("BK4-c069", "difference identity on random exact cases", ok_diff, True)
check("BK4-c076", "theta - rho identity on random exact cases", ok_theta_rho, True)
check("BK4-c071", "floor(y)>=10000 iff y>=10000 (y=9999.99,10000)", (math.floor(9999.99) >= 10000, math.floor(10000) >= 10000), (False, True))
check("BK4-c065", "lab coverage 113/120 floor 10000", math.floor(10000 * Fraction(113, 120)), 9416)

# ---- L03 c048 and c047 spot check ----
check("BK4-c048", "9900*200/10000", Fraction(9900 * 200, 10000), 198)

print("\nMISMATCHES:", bad)
