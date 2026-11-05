"""Independent re-derivation of BK4 L03 Lab 1 printed values, worked examples and problem numbers (exact integers)."""
import random
from fractions import Fraction
import math

def pay_layers(L, IM, DF, K, defaulter, survivors_all):
    a1 = min(L, IM[defaulter])
    a2 = min(L - a1, DF[defaulter])
    a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    surv = sorted(i for i in DF if i != defaulter)
    D = sum(DF[i] for i in surv)
    if Z >= D:
        pays = {i: DF[i] for i in surv}
        u = Z - D
    else:
        pays = {i: Fraction(Z * DF[i], D) for i in surv}
        pays = {i: math.floor(v) for i, v in pays.items()}
        left = Z - sum(pays.values())
        for i in surv:
            if left and DF[i] > 0:
                pays[i] += 1
                left -= 1
        assert left == 0
        u = 0
    total = a1 + a2 + a3 + sum(pays.values()) + u
    return (a1, a2, a3, pays, u, total == L)

# Part A1 fixture
fim = {1: 0, 2: 0, 3: 100}
fdf = {1: 40, 2: 60, 3: 50}
printed_rows = {80: (80, 0, 0, 0, 0, 0), 120: (100, 20, 0, 0, 0, 0), 170: (100, 50, 20, 0, 0, 0),
                180: (100, 50, 30, 0, 0, 0), 181: (100, 50, 30, 1, 0, 0), 200: (100, 50, 30, 8, 12, 0),
                205: (100, 50, 30, 10, 15, 0), 300: (100, 50, 30, 40, 60, 20)}
for L in (80, 120, 170, 180, 181, 200, 205, 300):
    a1, a2, a3, pays, u, ok = pay_layers(L, fim, fdf, 30, 3, None)
    got = (a1, a2, a3, pays[1], pays[2], u)
    exp = printed_rows[L]
    print("A1", L, got, "sum ok", ok, "matches printed", got == exp)
# Part A2
for L in (1, 2):
    r = pay_layers(L, {4: 0, 1: 0, 2: 0, 3: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0, 4, None)
    print("A2", L, r[:5], "sum ok", r[5])
# seeded inputs
rng = random.Random(2026)
MEMBERS = (1, 2, 3, 4)
im = {i: rng.randint(1000, 5000) for i in MEMBERS}
df = {i: rng.randint(100, 900) for i in MEMBERS}
cap = rng.randint(500, 2000)
print("IM", im, "DF", df, "cap", cap)
surv_df = sum(df[i] for i in MEMBERS if i != 3)
print("A3 scenario losses", im[3] // 2, im[3] + df[3] // 2, im[3] + df[3] + cap + surv_df // 2)
for L in (im[3] // 2, im[3] + df[3] // 2, im[3] + df[3] + cap + surv_df // 2):
    a1, a2, a3, pays, u, ok = pay_layers(L, im, df, cap, 3, None)
    print("A3", L, (a1, a2, a3), pays, u, ok)
print("survivor DF total", surv_df, "residual", (im[3] + df[3] + cap + surv_df // 2) - (im[3] + df[3] + cap))
losses = [rng.randint(0, 3000) for _ in range(200)]
srt = sorted(losses)
print("max loss", srt[-1], "L(198)", srt[197], "L(199)", srt[198])
for t in (9900, 9975):
    k = math.ceil(Fraction(t * 200, 10000))
    M = srt[k - 1]
    def cover(M):
        return 10000 * sum(1 for x in losses if x <= M) // 200
    brute = next(m for m in range(max(losses) + 1) if cover(m) >= t)
    print("target", t, "k", k, "margin", M, "cover", cover(M), "cover-1", cover(M - 1), "brute", brute, "agree", brute == M)
# Examples and problems
print("Ex1.5 L=300 uncovered", 300 - 100 - 50 - 30 - 40 - 60)
ex = [1000, 2000, 3000, 5000]
print("M2 cover(4000)", 10000 * sum(1 for x in ex if x <= 4000) // 4, "k", math.ceil(Fraction(7500 * 4, 10000)), "L3", sorted(ex)[2])
print("M3", [sorted([10, 20, 30, 40, 50])[math.ceil(Fraction(t * 5, 10000)) - 1] for t in (8000, 8001, 10000)])
print("R2 k", math.ceil(Fraction(9900 * 100, 10000)), "k2", math.ceil(Fraction(10000 * 100, 10000)))
print("R3 k(399,400)", [math.ceil(Fraction(9975 * S, 10000)) for S in (399, 400, 401)])
print("Ex2.5 k", math.ceil(Fraction(9900 * 200, 10000)), math.ceil(Fraction(9975 * 200, 10000)), Fraction(9975 * 200, 10000))
print("E3 cover", [10000 * c // 200 for c in (197, 198, 199)])
