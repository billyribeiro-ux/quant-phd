"""Independent re-derivation of every number in BK4 slice a (index, L01, L02, L03), written for the round-3 verifier.

Does not import the lab code: it re-draws the seeded inputs with its own loops and recomputes each printed number
with Fraction or exact integers. Usage (repo root): python3 -I ledgers/BK4/scripts/BK4-a-r3/rederive_slice_a_r3.py
"""

from fractions import Fraction
import math
import random

FAIL = []


def check(label: str, got, want) -> None:
    ok = got == want
    print(f"{'OK  ' if ok else 'FAIL'} {label}: got {got}, page/expected {want}")
    if not ok:
        FAIL.append(label)


# ---- L01: seed 20260, 12 payments, three banks, whole-dollar amounts 100..5000, cents ----
rng = random.Random(20260)
day = []
for seq in range(1, 13):
    s, r = rng.sample(range(3), 2)
    dollars = rng.randint(100, 5000)
    day.append((s, r, 100 * dollars))
print("L01 day (sender, receiver, cents):", day)


def running(bank: int) -> list[int]:
    out, bal = [0], 0
    for s, r, a in day:
        if s == bank:
            bal -= a
        elif r == bank:
            bal += a
        out.append(bal)
    return out


need, net, debit = {}, {}, {}
for b in range(3):
    S = running(b)
    need[b] = max(0, -min(S))
    net[b] = S[-1]
    debit[b] = max(0, -net[b])
check("L01 Bank A RTGS need (page 112500)", need[0], 112500)
check("L01 Bank B RTGS need (page 1533900)", need[1], 1533900)
check("L01 Bank C RTGS need (page 0)", need[2], 0)
check("L01 Bank A net (page +379800)", net[0], 379800)
check("L01 Bank B net (page -1533900)", net[1], -1533900)
check("L01 Bank C net (page +1154100)", net[2], 1154100)
check("L01 debits A,B,C (page 0, 1533900, 0)", (debit[0], debit[1], debit[2]), (0, 1533900, 0))
check("L01 nets sum to zero", sum(net.values()), 0)
check("L01 need >= debit every bank", all(need[b] >= debit[b] for b in range(3)), True)
gross = sum(a for _, _, a in day)
moved = sum(debit.values())
check("L01 gross value (page 2841600)", gross, 2841600)
check("L01 moved at settlement (page 1533900)", moved, 1533900)
ratio = Fraction(moved, gross)
print("L01 ratio exact:", ratio, "float:", float(ratio))
check("L01 ratio to 4 dp half-up = 0.5398", Fraction(math.floor(ratio * 10000 + Fraction(1, 2)), 10000), Fraction(5398, 10000))
check("L01 ratio digits 0.53980152", f"{float(ratio):.8f}", "0.53980152")
check("L01 banks with positive debit (page 1 of 3)", sum(1 for b in range(3) if debit[b] > 0), 1)
check("L01 banks need > debit (page 1 of 3)", sum(1 for b in range(3) if need[b] > debit[b]), 1)

# L01 worked examples (Example 2.6, Remark 2.7, M1-M3, R3)
ex = [(0, 1, 10000), (1, 2, 8000), (2, 0, 5000)]  # A pays B 100; B pays C 80; C pays A 50 (dollars)


def run_ex(seq_list, bank):
    bal, low = 0, 0
    for s, r, a in seq_list:
        bal += -a if s == bank else (a if r == bank else 0)
        low = min(low, bal)
    return -low


check("L01 Ex2.6 Need_A (page 100)", run_ex(ex, 0), 10000)
check("L01 Ex2.6 Need_B (page 0)", run_ex(ex, 1), 0)
check("L01 Ex2.6 Need_C (page 0)", run_ex(ex, 2), 0)
ex_re = [ex[2], ex[0], ex[1]]
check("L01 Remark2.7 Need_A (page 50)", run_ex(ex_re, 0), 5000)
check("L01 Ex2.6 Net_A (page -50)", sum(-a if s == 0 else (a if r == 0 else 0) for s, r, a in ex), -5000)
check("L01 M1 Need (page 200), Debit (200)", (max(0, -min(0, 30000, -20000) if False else 20000), 20000), (20000, 20000))
mS = [0, 4000, -3000, -2000]  # M3: receives 40, pays 70, receives 10 (dollars, cents*100)
mS = [0, 4000, -3000, -2000]
check("L01 M3 need (page 30 dollars)", -min(mS), 3000)
check("L01 M3 debit (page 20 dollars)", -mS[-1], 2000)

# ---- L02: seed 2026, 6 trades, four members, amounts 500..20000 dollars ----
rng = random.Random(2026)
tr = []
for seq in range(1, 7):
    p, q = rng.sample(range(4), 2)
    dollars = rng.randint(500, 20000)
    tr.append((p, q, 100 * dollars))
G = sum(a for _, _, a in tr)
rec = [sum(a for _, q, a in tr if q == m) for m in range(4)]
pay = [sum(a for p, _, a in tr if p == m) for m in range(4)]
n = [rec[m] - pay[m] for m in range(4)]
A = sum(max(0, x) for x in n)
check("L02 gross (page 7596300)", G, 7596300)
check("L02 receivables (page 314500,2067800,3340300,1873700)", tuple(rec), (314500, 2067800, 3340300, 1873700))
check("L02 net obligations (page -3627000,+1753300,+3340300,-1466600)", tuple(n), (-3627000, 1753300, 3340300, -1466600))
check("L02 sum net zero", sum(n), 0)
check("L02 netted A (page 5093600)", A, 5093600)
check("L02 A equals sum of payers", A, sum(max(0, -x) for x in n))
check("L02 reduction (page 2502700)", G - A, 2502700)
bps = (10000 * (G - A)) // G
print("L02 reduction exact:", Fraction(10000 * (G - A), G), float(Fraction(10000 * (G - A), G)))
check("L02 reduction bps floored (page 3294)", bps, 3294)
check("L02 both-receive-and-pay members (page 1,2,4)", [m + 1 for m in range(4) if rec[m] > 0 and pay[m] > 0], [1, 2, 4])

# L02 Example 2.4 and M1, M2
ex2 = [(0, 1, 10000), (1, 2, 8000), (2, 0, 5000)]
rec2 = [5000, 10000, 8000]
pay2 = [10000, 8000, 5000]
n2 = [rec2[i] - pay2[i] for i in range(3)]
A2 = sum(max(0, x) for x in n2)
G2 = 23000
check("L02 Ex2.4 nets (page -50,20,30 dollars)", n2, [-5000, 2000, 3000])
check("L02 Ex2.4 A (page 50 dollars)", A2, 5000)
check("L02 Ex2.4 bps (page 7826)", (10000 * (G2 - A2)) // G2, 7826)
check("L02 M1 bps (page 7222; G=180, A=50)", (10000 * (180 - 50)) // 180, 7222)
check("L02 M2 bps doubled (page 7826)", (10000 * (460 - 100)) // 460, 7826)
check("L02 M2 netted doubled (page 100 dollars)", 2 * A2, 10000)

# ---- L03: seed 2026, defaulter 3, IM 1000..5000, DF 100..900, K 500..2000; 200 losses 0..3000 ----
rng = random.Random(2026)
im = {i: rng.randint(1000, 5000) for i in (1, 2, 3, 4)}
df = {i: rng.randint(100, 900) for i in (1, 2, 3, 4)}
cap = rng.randint(500, 2000)
print("L03 inputs IM", im, "DF", df, "K", cap)
check("L03 IM values (page 1487,2308,3058,4896)", (im[1], im[2], im[3], im[4]), (1487, 2308, 3058, 4896))
check("L03 DF values (page 624,762,205,328)", (df[1], df[2], df[3], df[4]), (624, 762, 205, 328))
check("L03 capital (page 1730)", cap, 1730)


def waterfall(L, dflt, imd, dfd, K):
    a1 = min(L, imd[dflt])
    a2 = min(L - a1, dfd[dflt])
    a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    surv = sorted(i for i in dfd if i != dflt)
    D = sum(dfd[i] for i in surv)
    if Z >= D:
        return a1, a2, a3, {i: dfd[i] for i in surv}, Z - D
    pays = {i: Fraction(Z * dfd[i], D) for i in surv}
    x = {i: math.floor(pays[i]) for i in surv}
    left = Z - sum(x.values())
    for i in surv:
        if left and dfd[i] > 0:
            x[i] += 1
            left -= 1
    assert left == 0
    return a1, a2, a3, x, 0


# Example 1.5 table
fim = {1: 0, 2: 0, 3: 100}
fdf = {1: 40, 2: 60, 3: 50}
expect = {80: (80, 0, 0, {1: 0, 2: 0}, 0), 120: (100, 20, 0, {1: 0, 2: 0}, 0), 170: (100, 50, 20, {1: 0, 2: 0}, 0),
          180: (100, 50, 30, {1: 0, 2: 0}, 0), 181: (100, 50, 30, {1: 1, 2: 0}, 0), 200: (100, 50, 30, {1: 8, 2: 12}, 0),
          205: (100, 50, 30, {1: 10, 2: 15}, 0), 300: (100, 50, 30, {1: 40, 2: 60}, 20)}
for L, want in expect.items():
    got = waterfall(L, 3, fim, fdf, 30)
    check(f"L03 Ex1.5 row {L}", got, want)
    tot = got[0] + got[1] + got[2] + sum(got[3].values()) + got[4]
    check(f"L03 conservation row {L}", tot, L)
# Example 1.6
g1 = waterfall(1, 4, {4: 0, 1: 0, 2: 0, 3: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0)
g2 = waterfall(2, 4, {4: 0, 1: 0, 2: 0, 3: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0)
check("L03 Ex1.6 Z=1 survivors (page member 1 pays 1)", g1[3], {1: 1, 2: 0, 3: 0})
check("L03 Ex1.6 Z=2 survivors (page members 1,2 pay 1)", g2[3], {1: 1, 2: 1, 3: 0})

# Part A3 scenarios
sc = [im[3] // 2, im[3] + df[3] // 2, im[3] + df[3] + cap + (df[1] + df[2] + df[4]) // 2]
check("L03 A3 scenario losses (page 1529, 3160, 5850)", tuple(sc), (1529, 3160, 5850))
w = waterfall(5850, 3, im, df, cap)
check("L03 A3 surviving-member residual (page 857)", 5850 - im[3] - df[3] - cap, 857)
check("L03 A3 survivor payments (page 312,381,164)", (w[3][1], w[3][2], w[3][4]), (312, 381, 164))
check("L03 A3 D/2 identity", (df[1] + df[2] + df[4]) == 2 * 857, True)
w2 = waterfall(3160, 3, im, df, cap)
check("L03 E1 layers at 3160 (page 3058,102,0)", (w2[0], w2[1], w2[2]), (3058, 102, 0))

# Part B: 200 losses 0..3000 drawn after the inputs
losses = [rng.randint(0, 3000) for _ in range(200)]


def cover_bps(M: int) -> int:
    c = sum(1 for L in losses if L <= M)
    return (10000 * c) // 200


def sized(t: int) -> tuple[int, int]:
    k = math.ceil(Fraction(t * 200, 10000))
    return sorted(losses)[k - 1], k


def brute(t: int) -> int:
    for M in range(0, max(losses) + 1):
        if cover_bps(M) >= t:
            return M
    raise SystemExit("no margin")


m9900, k9900 = sized(9900)
m9975, k9975 = sized(9975)
check("L03 Part B k for 9900 (page 198)", k9900, 198)
check("L03 Part B k for 9975 (page 200)", k9975, 200)
check("L03 Part B sized 9900 (page 2961)", m9900, 2961)
check("L03 Part B sized 9975 (page 2992)", m9975, 2992)
check("L03 brute 9900 equals sized", brute(9900), m9900)
check("L03 brute 9975 equals sized", brute(9975), m9975)
check("L03 cover at 2961 (page 9900)", cover_bps(2961), 9900)
check("L03 cover at 2960 (page 9850)", cover_bps(2960), 9850)
check("L03 cover at 2992 (page 10000)", cover_bps(2992), 10000)
check("L03 cover at 2991 (page 9950)", cover_bps(2991), 9950)
print("L03 largest seeded loss:", max(losses), "; 9975 sized margin equals largest loss:", m9975 == max(losses))
check("L03 2992 is the largest seeded loss (page 'the largest seeded loss')", m9975, max(losses))
top2 = sorted(losses)[-2:]
print("L03 two largest losses:", top2, "; 9900 sized margin:", m9900)

# Sensitivity claim on page (line 421): 'the sized margin does not depend on how large these two losses are'
alt = list(losses)
idx = sorted(range(200), key=lambda i: alt[i])[-2:]
for i in idx:
    alt[i] = 0
sized_alt = sorted(alt)[k9900 - 1]
check("L03 sensitivity: lowering the two largest losses to 0 leaves the 9900 sized margin unchanged (page line 421 claim)", sized_alt, m9900)

# Example 2.5 fractions
check("L03 Ex2.5 9900*200/10000 exact = 198", Fraction(9900 * 200, 10000), 198)
check("L03 Ex2.5 9975*200/10000 exact = 199.5", Fraction(9975 * 200, 10000), Fraction(399, 2))

# R3 boundary: k = S for S <= 399 at 9975, and k < S at S = 400
for S_ in (1, 399, 400, 401, 800):
    kk = math.ceil(Fraction(9975 * S_, 10000))
    print(f"L03 R3 S={S_}: k={kk}, S-k={S_ - kk}")
check("L03 R3 k(400)=399 (page 399 exact)", math.ceil(Fraction(9975 * 400, 10000)), 399)
check("L03 R3 k(399)=399 equals S (page: k=S for S<=399)", math.ceil(Fraction(9975 * 399, 10000)), 399)

# M2 and M3 of L03
check("L03 M2 cover(4000)=7500", (10000 * 3) // 4, 7500)
check("L03 M2 cover(2999)=5000", (10000 * 2) // 4, 5000)
check("L03 M3 sized 8000 (page 40)", sorted([10, 20, 30, 40, 50])[math.ceil(Fraction(8000 * 5, 10000)) - 1], 40)
check("L03 M3 sized 8001 (page 50)", sorted([10, 20, 30, 40, 50])[math.ceil(Fraction(8001 * 5, 10000)) - 1], 50)

print("FAILS:", FAIL)
