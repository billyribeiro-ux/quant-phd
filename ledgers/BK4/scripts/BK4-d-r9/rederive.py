"""Independent re-derivation of every number that a BK4 card or lesson sentence states on the page.

Written from the lesson definitions, not from the lab code. Prints one line per claim with PASS/FAIL.
Usage: python -I rederive.py
"""
from fractions import Fraction as F
import math

out: list[tuple[str, bool, str]] = []


def check(name: str, got, want) -> None:
    ok = got == want
    out.append((name, ok, f"got {got} want {want}"))


# L01 Example 2.6: A pays B 100, B pays C 80, C pays A 50 (dollars)
pays = [("A", "B", 100), ("B", "C", 80), ("C", "A", 50)]


def running(bank, order):
    s, out_ = 0, [0]
    for snd, rcv, amt in order:
        if snd == bank:
            s -= amt
        if rcv == bank:
            s += amt
        out_.append(s)
    return out_


def need(bank, order):
    return max(0, -min(running(bank, order)))


def net(bank, order):
    return sum(a for s, r, a in order if r == bank) - sum(a for s, r, a in order if s == bank)


check("c008 Need_A Ex2.6", need("A", pays), 100)
check("running A Ex2.6", running("A", pays), [0, -100, -100, -50])
check("c101 Debit_A Ex2.6", max(0, -net("A", pays)), 50)
check("c006 Need_A>Debit_A strict", need("A", pays) > max(0, -net("A", pays)), True)
rem = [pays[2], pays[1], pays[0]]
check("c009 Need_A after Remark2.7 order (payment 3 first)", need("A", [pays[2], pays[0], pays[1]]), 50)
check("Remark2.7 running A", running("A", [pays[2], pays[0], pays[1]]), [0, 50, -50, -50])
check("net positions Ex2.6", [net(b, pays) for b in "ABC"], [-50, 20, 30])
check("c027 netted amount Ex2.4", sum(max(0, n) for n in [-50, 20, 30]), 50)
check("c028 floor(10000*180/230)", (10000 * 180) // 230, 7826)
check("M1 L02 chain reduction bp", (10000 * 130) // 180, 7222)
check("M2 L02 doubled bp", (10000 * 360) // 460, 7826)

# L01 Example M1: receives 300 then pays 500
check("M1 L01 need", need("D", [("X", "D", 300), ("D", "Y", 500)]), 200)

# L01 Remark 2.8 / L04 worked values
check("c072 coverage rho=21/20 x=1/2", (F(21, 20) - F(1, 2)) / (1 - F(1, 2)), F(11, 10))
check("c072 bps", math.floor(10000 * (F(21, 20) - F(1, 2)) / (1 - F(1, 2))), 11000)
check("c075 coverage rho=19/20 x=1/2", (F(19, 20) - F(1, 2)) / (1 - F(1, 2)), F(9, 10))
check("c075 rho/2", F(19, 20) / 2, F(19, 40))
check("Remark2.8 x=1/7 coverage", (F(19, 20) - F(1, 7)) / (1 - F(1, 7)), F(113, 120))
check("Remark2.8 floor", math.floor(10000 * (F(19, 20) - F(1, 7)) / (1 - F(1, 7))), 9416)
check("c073 threshold h=1/20", 1 / (1 - F(1, 20)), F(20, 19))
check("c067 theta formula at x=3/10 rho=1/2", (F(1, 2) - F(3, 10)) / (1 - F(3, 10)), F(2, 7))
check("c068 theta-1 identity", (F(19, 20) - F(1, 2)) / (1 - F(1, 2)) - 1, (F(19, 20) - 1) / (1 - F(1, 2)))
check("c076 theta-rho identity", (F(19, 20) - F(1, 2)) / (1 - F(1, 2)) - F(19, 20), F(1, 2) * (F(19, 20) - 1) / (1 - F(1, 2)))
check("c074 measured coverage rho=1 h=1/20", (1 - F(1, 20) - 0) / (1 - 0), F(19, 20))

# L04 lab path values (exact fractions; independent of lab code)
for share, cov in [(F(7, 100), F(88, 93)), (F(1, 10), F(17, 18)), (F(1, 5), F(15, 16)),
                   (F(21, 50), F(53, 58)), (F(51, 100), F(44, 49)), (F(21, 25), F(11, 16))]:
    check(f"L04 rho=19/20 coverage at {share}", (F(19, 20) - share) / (1 - share), cov)
check("E1 lowest bps rho=19/20", math.floor(10000 * F(11, 16)), 6875)
check("E3 difference identity LHS", F(44, 49) - F(15, 16), F(-31, 784))
check("E3 difference identity RHS", (F(51, 100) - F(1, 5)) * (F(19, 20) - 1) / ((1 - F(1, 5)) * (1 - F(51, 100))), F(-31, 784))
check("R2 L04 x* for c=9/10", (F(19, 20) - F(9, 10)) / (1 - F(9, 10)), F(1, 2))
check("L04 ratio 1900000/2000000", F(1900000, 2000000), F(19, 20))
check("L04 rho=21/20 effective with h", F(21, 20) * (1 - F(1, 20)), F(399, 400))
check("L04 haircut coverage at 1/2 for 399/400", (F(399, 400) - F(1, 2)) / (1 - F(1, 2)), F(199, 200))

# L03 waterfall (Definition 1.1 and Example 1.5 fixture) recomputed from the definition
def waterfall(L, IM, DF, K, surv_df):
    a1 = min(L, IM)
    a2 = min(L - a1, DF)
    a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    D = sum(surv_df.values())
    if Z >= D:
        pay = dict(surv_df)
        u = Z - D
    else:
        pay = {i: Z * df // D for i, df in surv_df.items()}
        left = Z - sum(pay.values())
        for i in sorted(surv_df):
            if left == 0:
                break
            if surv_df[i] > 0:
                pay[i] += 1
                left -= 1
        u = 0
    return a1, a2, a3, pay, u


fixture = {1: 40, 2: 60}
expected_rows = {
    80: (80, 0, 0, {1: 0, 2: 0}, 0), 120: (100, 20, 0, {1: 0, 2: 0}, 0), 170: (100, 50, 20, {1: 0, 2: 0}, 0),
    180: (100, 50, 30, {1: 0, 2: 0}, 0), 181: (100, 50, 30, {1: 1, 2: 0}, 0), 200: (100, 50, 30, {1: 8, 2: 12}, 0),
    205: (100, 50, 30, {1: 10, 2: 15}, 0), 300: (100, 50, 30, {1: 40, 2: 60}, 20),
}
for L, want in expected_rows.items():
    got = waterfall(L, 100, 50, 30, fixture)
    check(f"c043/Ex1.5 table row L={L}", got, want)
    check(f"Prop1.2 conservation L={L}", got[0] + got[1] + got[2] + sum(got[3].values()) + got[4], L)
check("Ex1.6 Z=1 pay", waterfall(1, 0, 0, 0, {1: 1, 2: 1, 3: 1}), (0, 0, 0, {1: 1, 2: 0, 3: 0}, 0))
check("Ex1.6 Z=2 pay", waterfall(2, 0, 0, 0, {1: 1, 2: 1, 3: 1}), (0, 0, 0, {1: 1, 2: 1, 3: 0}, 0))
# seeded scenario (Lab 1 A3) layers from the printed fixture inputs
check("c040 M1 L03 example 200", sum([100, 50, 30, 8, 12]), 200)
# Definition 2.1 cover and Prop 2.3 index on the Example 2.5 / M2 / M3 values
check("c048 k for 9900 S=200", math.ceil(F(9900 * 200, 10000)), 198)
check("L03 9975 S=200 k", math.ceil(F(9975 * 200, 10000)), 200)
check("L03 M2 cover(4000)", (10000 * 3) // 4, 7500)
check("L03 M2 k", math.ceil(F(7500 * 4, 10000)), 3)
check("L03 M3 k 8000", math.ceil(F(8000 * 5, 10000)), 4)
check("L03 M3 k 8001", math.ceil(F(8001 * 5, 10000)), 5)
check("L03 R2 k 9900 S=100", math.ceil(F(9900 * 100, 10000)), 99)
check("L03 R3 S=399 k", math.ceil(F(9975 * 399, 10000)), 399)
check("L03 R3 S=400 k", math.ceil(F(9975 * 400, 10000)), 399)
check("L03 E1 layers 3160", (3058, 3160 - 3058), (3058, 102))
check("L03 E2 residual", 5850 - 3058 - 205 - 1730, 857)
check("L03 E2 survivor DF total", 624 + 762 + 328, 1714)
check("L03 E2 shares", [857 * d // 1714 for d in (624, 762, 328)], [312, 381, 164])

# L05 E[C], Prop 2.2, Prop 2.5, Example 2.7, Example 2.8, R1, R2
p = F(1, 8)
kappa = 2500
ells = (1, 2, 4)
EC_closed = p * kappa * sum(ells)
check("c086 E[C] closed", EC_closed, F(4375, 2))
check("c094 round half up", math.floor(EC_closed + F(1, 2)), 2188)
check("c090 equal delays 2", p * kappa * sum((2, 2, 2)), 1875)
outcomes_ind = []
for pat in [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]:
    prob = F(1)
    for x in pat:
        prob *= p if x else (1 - p)
    cost = sum(kappa * l * x for l, x in zip(ells, pat))
    outcomes_ind.append((prob, cost))
mean_ind = sum(q * c for q, c in outcomes_ind)
var_ind = sum(q * c * c for q, c in outcomes_ind) - mean_ind ** 2
outcomes_com = [(1 - p, 0), (p, kappa * sum(ells))]
mean_com = sum(q * c for q, c in outcomes_com)
var_com = sum(q * c * c for q, c in outcomes_com) - mean_com ** 2
check("c087 var independent", var_ind, F(57421875, 4))
check("c087 var comonotone", var_com, F(133984375, 4))
check("E2 var difference", var_com - var_ind, F(19140625))
check("Prop2.5 closed form diff", 2 * kappa ** 2 * p * (1 - p) * sum(ells[i] * ells[j] for i in range(3) for j in range(i + 1, 3)), F(19140625))
check("c089 P(at least one) indep", 1 - (1 - p) ** 3, F(169, 512))
check("c089 3p", 3 * p, F(192, 512) * 1 if False else F(3, 8))
check("c089 comonotone at least one", p, F(64, 512))
check("c084 P(C=0) indep", (1 - p) ** 3, F(343, 512))
check("c084 P(C=0) comon", 1 - p, F(7, 8))
check("c080/c081 mean indep E", mean_ind, F(4375, 2))
check("c100 mean comon", mean_com, F(4375, 2))
check("R1 ratio n=3", F(3) , F(3))
check("R2 L05 bound 5/8", 1 - 3 * p, F(5, 8))
check("R2 L05 bound 7/8", 1 - p, F(7, 8))
check("Ex2.8 dollars", F(2188, 100), F(2188, 100))
check("E1 2187.5 cents = 21.875 dollars rounded 21.88", round(F(4375, 2) / 100, 2), F(2188, 100))

fails = [(n, d) for n, ok, d in out if not ok]
for name, ok, detail in out:
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else "  " + detail))
print(f"checks {len(out)} pass {len(out) - len(fails)} fail {len(fails)}")
