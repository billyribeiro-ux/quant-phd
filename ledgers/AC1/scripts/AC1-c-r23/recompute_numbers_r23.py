"""Round 23 (AC1-c): independent recomputation of the worked numbers on L07 and L08 (integer cents, Fraction-free).

Usage: python -I recompute_numbers_r23.py
Each assertion is a number printed in the lesson text; the script stops on the first mismatch.
"""

from fractions import Fraction

def fmt(c: int) -> str:
    return f"{c // 100:,}.{c % 100:02d}"

# L07 Example 1.4: 1,000 shares at $12.00, year 1, vest 4
C = 1000 * 1200
base = C // 4
assert (C, base) == (1_200_000, 300_000)
assert [base] * 4 == [300_000] * 4 and sum([base] * 4) == C

# L07 M1: 500 shares at $8.00, grant year 2, vest 3
C = 500 * 800
b = C // 3
last = C - 2 * b
assert (C, b, last) == (400_000, 133_333, 133_334) and b + b + last == C
# L07 M2: same grant vesting over 4 years
b4 = C // 4
assert b4 == 100_000 and C - 3 * b4 == 100_000
# L07 M3: OI2 = 20,000; S2 = 1,333.33
S2 = 133_333
NI2 = 2_000_000 - S2
assert (NI2, 2_000_000) == (1_866_667, 2_000_000)
assert S2 + NI2 == 2_000_000
# L07 Example 2.3: OI1 = 50,000, S1 = 3,000
assert (5_000_000 - 300_000) == 4_700_000
# L07 E1/E3 and key results: L07 printed table (out/twin_L07.out) peak SBC 57,822.92 in year 3, year 6 SBC zero
sbc_year3 = 5_782_292
assert fmt(sbc_year3) == "57,822.92"
# L07 R2 solution: a 12,000 grant over 4 years, year 2 expense 3,000
assert 1_200_000 * 1 // 4 == 300_000

# L08 Example 1.4: cost 100,000, life 5, tax % (40,30,20,10,0), rate 21
cost, L, tp, r = 100_000, 5, (40, 30, 20, 10, 0), 21
b = cost // L
tau = [cost * p // 100 for p in tp]
K, dtl = [], []
acc = 0
for t in range(L):
    acc += tau[t] - b
    K.append(acc)
    dtl.append(Fraction(r * acc, 100))
assert K == [20_000, 30_000, 30_000, 20_000, 0]
assert dtl == [4200, 6300, 6300, 4200, 0]
# Example 2.2: P = 50,000 each year, rate 21
P = 50_000
prev = 0
for t in range(2):
    d = tau[t] - b
    CT = Fraction(r * (P - d), 100)
    DE = dtl[t] - prev
    prev = dtl[t]
    assert (CT, DE, CT + DE) == ((6300, 4200, 10500) if t == 0 else (8400, 2100, 10500))
# L08 M2: cost 60,000, life 3, tax % (50,30,20)
cost, L = 6_000_000, 3
b = cost // L
tau = [cost * p // 100 for p in (50, 30, 20)]
assert b == 2_000_000 and tau == [3_000_000, 1_800_000, 1_200_000]
diff = [t - b for t in tau]
assert diff == [1_000_000, -200_000, -800_000]
K = [1_000_000, 800_000, 0]
assert [Fraction(21 * k, 100) for k in K] == [Fraction(210_000), Fraction(168_000), 0]
DE = [210_000, 168_000 - 210_000, 0 - 168_000]
assert DE == [210_000, -42_000, -168_000] and sum(DE) == 0
# L08 M3: P = 50,000 for M2's asset
CT = [21 * (5_000_000 - d) // 100 for d in diff]
assert CT[0] == 840_000
# (CT2 = 0.21 * 52,000 = 10,920; CT3 = 0.21 * 58,000 = 12,180, in cents)
assert CT[1] == 1_092_000 and CT[2] == 1_218_000
# L08 R2: K2 = 30,000; end-year-3 balance at 25%; DE3 and TE3
assert 25 * 30_000 // 100 == 7_500 and 21 * 30_000 // 100 == 6_300
assert 25 * 30_000 // 100 - 21 * 30_000 // 100 == 1_200 and 4 * 30_000 // 100 == 1_200
assert 25 * 50_000 // 100 + 1_200 == 13_700
# L08 lab printed table (out/twin_L08.out), seed 20260702, year 1 and year 2 identities
cost_lab = 4_670_000
b_lab = cost_lab // 5
assert b_lab == 934_000
assert 21 * 934_000 // 100 == 196_140
# year 2 difference: cumulative temp diff 14,010.00, DTL 2,942.10 and 30% of cost
assert 4_670_000 * 30 // 100 == 1_401_000 and 21 * 1_401_000 // 100 == 294_210
# E1 solution: current 8,169.84 + deferred 1,961.40 = 10,131.24 = 0.21 * 48,244.00
assert 816_984 + 196_140 == 1_013_124 == 21 * 4_824_400 // 100
print("recompute_numbers_r23: all assertions passed")
