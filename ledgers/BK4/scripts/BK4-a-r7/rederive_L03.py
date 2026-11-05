"""Independent re-derivation of the L03 lab numbers and the L03 worked numbers (BK4 slice a, round 7).

The seeded inputs are regenerated here from Random(2026) in the stated draw order; the layers are re-implemented
from Definition 1.1 with exact integer arithmetic; the sized margin is computed two ways (order statistic with
integer ceiling via fractions.Fraction, and brute force over integer margins) and compared.
"""
import random
from fractions import Fraction
from math import ceil

rng = random.Random(2026)
MEMBERS = (1, 2, 3, 4)
im = {i: rng.randint(1000, 5000) for i in MEMBERS}
df = {i: rng.randint(100, 900) for i in MEMBERS}
cap = rng.randint(500, 2000)
print("inputs", im, df, cap)
printed_inputs = ({1: 1487, 2: 2308, 3: 3058, 4: 4896}, {1: 624, 2: 762, 3: 205, 4: 328}, 1730)
print("inputs match printed header:", (im, df, cap) == printed_inputs)


def layers(loss, im_d, df_d, K, surv_df):
    """Definition 1.1, exact integers. surv_df: {member: DF} for survivors."""
    a1 = min(loss, im_d)
    a2 = min(loss - a1, df_d)
    a3 = min(loss - a1 - a2, K)
    Z = loss - a1 - a2 - a3
    D = sum(surv_df.values())
    if Z >= D:
        pay = dict(surv_df)
        u = Z - D
    else:
        x = {i: (Z * surv_df[i]) // D for i in surv_df}
        ell = Z - sum(x.values())
        pay = dict(x)
        for i in sorted(surv_df):
            if ell == 0:
                break
            if surv_df[i] > 0:
                pay[i] += 1
                ell -= 1
        assert ell == 0
        u = 0
    assert a1 + a2 + a3 + sum(pay.values()) + u == loss
    return a1, a2, a3, pay, u


# Part A1 fixture: defaulter 3, IM 100, DF 50, K 30; survivors 1 (40) and 2 (60)
fx = {1: 40, 2: 60}
for L in (80, 120, 170, 180, 181, 200, 205, 300):
    a1, a2, a3, pay, u = layers(L, 100, 50, 30, fx)
    print("A1", L, a1, a2, a3, pay[1], pay[2], u)

# Part A2: defaulter 4 (no IM, no DF), K 0, survivors 1,2,3 DF 1 each
for L in (1, 2):
    a1, a2, a3, pay, u = layers(L, 0, 0, 0, {1: 1, 2: 1, 3: 1})
    print("A2", L, pay, u)

# Part A3: defaulter 3 with seeded IM 3058, DF 205; K 1730; survivors 1,2,4
surv = {i: df[i] for i in MEMBERS if i != 3}
Dtot = sum(surv.values())
s_within = im[3] // 2
s_df = im[3] + df[3] // 2
s_surv = im[3] + df[3] + cap + sum(surv.values()) // 2
for label, L in (("within", s_within), ("default fund", s_df), ("survivors", s_surv)):
    a1, a2, a3, pay, u = layers(L, im[3], df[3], cap, surv)
    print("A3", label, "loss", L, "layers", a1, a2, a3, "survivors", pay, "uncovered", u)
print("A3 survivor total D", Dtot, "residual", s_surv - im[3] - df[3] - cap)

# Part B: 200 seeded losses 0..3000, drawn after the inputs
losses = [rng.randint(0, 3000) for _ in range(200)]
srt = sorted(losses)
S = len(losses)


def cover_bps(M):
    c = sum(1 for L in losses if L <= M)
    return (10000 * c) // S


for t in (9900, 9975):
    k = ceil(Fraction(t * S, 10000))
    sized = srt[k - 1]
    brute = next(M for M in range(max(losses) + 1) if cover_bps(M) >= t)
    print(f"B target {t}: k={k} sized={sized} brute={brute} agree={sized == brute} cover_at={cover_bps(sized)} cover_below={cover_bps(sized - 1)}")
print("B max loss", max(losses), "L(198)", srt[197], "L(199)", srt[198], "L(200)", srt[199])
print("cover 9900 at L(198): c =", sum(1 for L in losses if L <= srt[197]), "above =", sum(1 for L in losses if L > srt[197]))

# Worked examples
print("Ex1.5 residual at 200", 200 - 100 - 50 - 30, "m1", 20 * 40 // 100, "m2", 20 * 60 // 100)
print("M2: cover(4000) for 1000,2000,3000,5000 =", (10000 * sum(1 for L in [1000, 2000, 3000, 5000] if L <= 4000)) // 4, "k", ceil(Fraction(7500 * 4, 10000)))
print("M3 sizes:", [sorted([10, 20, 30, 40, 50])[ceil(Fraction(t * 5, 10000)) - 1] for t in (8000, 8001, 10000)])
print("R2 S=100: k(9900)", ceil(Fraction(9900 * 100, 10000)), "k(10000)", ceil(Fraction(10000 * 100, 10000)))
print("E3: 50*198", 50 * 198, "50*199", 50 * 199)
print("R3: S=400 9975*400/10000 =", Fraction(9975 * 400, 10000), "ceil", ceil(Fraction(9975 * 400, 10000)))
print("R3: S in (399,400) with k==S:", [S_ for S_ in (399, 400) if ceil(Fraction(9975 * S_, 10000)) == S_])
print("Quiz: 8001*5/10000 =", Fraction(8001 * 5, 10000), "k", ceil(Fraction(8001 * 5, 10000)))
print("Quiz survivors residual 2 DF 1 each: floor(2*1/3) =", 2 * 1 // 3)
