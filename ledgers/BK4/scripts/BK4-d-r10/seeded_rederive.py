"""Independent re-derivation of the seeded and printed numbers used by BK4 cards.

Written from the definitions in the lesson text, not from the lab code. The inputs are the printed Lab 1 payments
(L01), the printed trades (L02) and the seeded scenario losses (L03), which are regenerated from seed 2026 with
random.Random and checked against the printed lab output. Prints PASS/FAIL per claim.
Usage: python -I seeded_rederive.py
"""
import random
from fractions import Fraction as F
import math

out: list[tuple[str, bool, str]] = []


def check(name: str, got: object, want: object) -> None:
    out.append((name, got == want, f"got {got} want {want}"))


# ---- L01 printed day (sending order), amounts in cents, banks indexed A=0, B=1, C=2
pay = [(1, 2, 101800), (1, 0, 324400), (1, 2, 318300), (1, 2, 278600), (1, 2, 218000), (2, 0, 149400),
       (0, 2, 269700), (1, 0, 173600), (0, 2, 91800), (0, 1, 398400), (1, 2, 25300), (1, 0, 492300)]


def running(bank: int) -> list[int]:
    s, acc = 0, [0]
    for snd, rcv, amt in pay:
        if snd == bank:
            s -= amt
        if rcv == bank:
            s += amt
        acc.append(s)
    return acc


def net(bank: int) -> int:
    return sum(a for s, r, a in pay if r == bank) - sum(a for s, r, a in pay if s == bank)


needs = [max(0, -min(running(b))) for b in range(3)]
nets = [net(b) for b in range(3)]
debits = [max(0, -n) for n in nets]
check("c011 Bank A RTGS need 112500", needs[0], 112500)
check("c010 Bank B need equals debit 1533900", (needs[1], debits[1]), (1533900, 1533900))
check("c014 Bank A net +379800", nets[0], 379800)
check("c014 Bank A debit 0", debits[0], 0)
check("L01 Bank C need 0", needs[2], 0)
check("L01 nets sum to zero", sum(nets), 0)
gross = sum(a for _, _, a in pay)
check("c012 gross 2841600", gross, 2841600)
check("c012 ratio to four places 0.5398", round(F(1533900, 2841600), 4), F(5398, 10000))
check("L01 E3 ratio digits 0.53980152", f"{1533900 / 2841600:.8f}", "0.53980152")

# ---- L02 printed trades: (payer, receiver, cents), members 1..4 indexed 0..3
trades = [(0, 1, 1696600), (0, 3, 1873700), (3, 2, 1845000), (3, 2, 1495300), (1, 0, 314500), (0, 1, 371200)]
G = sum(a for _, _, a in trades)
rec = [sum(a for p, r, a in trades if r == m) for m in range(4)]
pay2 = [sum(a for p, r, a in trades if p == m) for m in range(4)]
n = [rec[m] - pay2[m] for m in range(4)]
A = sum(max(0, x) for x in n)
check("c031 netted amount 5093600", A, 5093600)
check("c092 gross notional 7596300", G, 7596300)
check("c092 receivables sum to gross", sum(rec), 7596300)
check("L02 net obligations sum zero", sum(n), 0)
check("c031/E1 reduction 2502700", G - A, 2502700)
check("c031 floor bps 3294", (10000 * (G - A)) // G, 3294)
check("E2 positive net obligations sum", sum(x for x in n if x > 0), 5093600)
check("E2 largest creditor member 3", n.index(max(n)) + 1, 3)
check("E2 largest debtor member 1", n.index(min(n)) + 1, 1)
check("c028 Ex2.4 floor(10000*180/230) = 7826", (10000 * 180) // 230, 7826)
check("c027 Ex2.4 netted 50", max(0, 20) + max(0, 30), 50)

# ---- L03 seeded inputs: regenerate with the same draw order as the lab, then size the margin from definitions
rng = random.Random(2026)
im = {i: rng.randint(1000, 5000) for i in (1, 2, 3, 4)}
df = {i: rng.randint(100, 900) for i in (1, 2, 3, 4)}
cap = rng.randint(500, 2000)
check("L03 seeded IM values", im, {1: 1487, 2: 2308, 3: 3058, 4: 4896})
check("L03 seeded DF values", df, {1: 624, 2: 762, 3: 205, 4: 328})
check("L03 seeded capital", cap, 1730)
losses = [rng.randint(0, 3000) for _ in range(200)]
srt = sorted(losses)


def cover_bps(M: int) -> int:
    return (10000 * sum(1 for x in losses if x <= M)) // len(losses)


for t, want in ((9900, 2961), (9975, 2992)):
    k = math.ceil(F(t * 200, 10000))
    M = srt[k - 1]
    brute = next(m for m in range(0, 3001) if cover_bps(m) >= t)
    check(f"c049/c050 target {t} k", k, 198 if t == 9900 else 200)
    check(f"c049/c050 target {t} sized margin", M, want)
    check(f"c049/c050 target {t} brute force equals sized", brute, want)
check("c050 cover at 2992 is 10000 bps", cover_bps(2992), 10000)
check("c049 cover at 2961 is 9900 bps", cover_bps(2961), 9900)
check("E3 count above 2961 is 2", sum(1 for x in losses if x > 2961), 2)

# Example 1.5 and Example 1.6 by the definitions (independent of the lab code)


def waterfall(L: int, im_d: int, df_d: int, K: int, surv: dict[int, int]) -> tuple[int, int, int, dict[int, int], int]:
    a1 = min(L, im_d)
    a2 = min(L - a1, df_d)
    a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    D = sum(surv.values())
    if Z >= D:
        return a1, a2, a3, dict(surv), Z - D
    pay_ = {i: Z * v // D for i, v in surv.items()}
    left = Z - sum(pay_.values())
    for i in sorted(surv):
        if left == 0:
            break
        if surv[i] > 0:
            pay_[i] += 1
            left -= 1
    return a1, a2, a3, pay_, 0


w = waterfall(200, 100, 50, 30, {1: 40, 2: 60})
check("c043 Ex1.5 member 1 pays 8, member 2 pays 12, no uncovered", (w[3], w[4]), ({1: 8, 2: 12}, 0))
w = waterfall(181, 100, 50, 30, {1: 40, 2: 60})
check("Ex1.5 L=181 leftover to member 1", w[3], {1: 1, 2: 0})
w = waterfall(300, 100, 50, 30, {1: 40, 2: 60})
check("Ex1.5 L=300 uncovered 20", (w[3], w[4]), ({1: 40, 2: 60}, 20))
w = waterfall(2, 0, 0, 0, {1: 1, 2: 1, 3: 1})
check("c044 Ex1.6 Z=2 members 1 and 2 pay one cent each", w[3], {1: 1, 2: 1, 3: 0})

# ---- L05 numbers by enumeration (independent code)
from itertools import product
p = F(1, 8)
kappa = 2500
ell = (1, 2, 4)
mean_enum = F(0)
for pat in product((0, 1), repeat=3):
    pr = F(1)
    for x in pat:
        pr *= p if x else 1 - p
    mean_enum += pr * sum(kappa * l * x for l, x in zip(ell, pat))
check("c086 E[C] enumeration 4375/2", mean_enum, F(4375, 2))
check("c094 round half up 2188", math.floor(mean_enum + F(1, 2)), 2188)
check("c090 equal delays 2 gives 1875", sum(F(1, 8) * 2500 * 2 for _ in range(3)), 1875)
a = [kappa * l for l in ell]
var3 = sum(x * x for x in a) * p * (1 - p)
var4 = kappa * kappa * sum(ell) ** 2 * p * (1 - p)
check("c087 var independent 57421875/4", var3, F(57421875, 4))
check("c087 var comonotone 133984375/4", var4, F(133984375, 4))
check("c083 difference 2 kappa^2 p(1-p) sum_{i<j} l_i l_j", var4 - var3,
      2 * kappa * kappa * p * (1 - p) * (1 * 2 + 1 * 4 + 2 * 4))
check("E2 L05 difference 19140625", var4 - var3, 19140625)
check("c089 P(at least one) indep 169/512", 1 - (1 - p) ** 3, F(169, 512))
check("c089 3p 192/512", 3 * p, F(192, 512))
check("c084 P(C=0) indep (1-p)^3", (1 - p) ** 3, F(343, 512))
check("c084 P(C=0) comon 1-p", 1 - p, F(7, 8))
check("c100 mean comonotone", p * kappa * sum(ell), F(4375, 2))

# ---- L04 ratio/coverage numbers
check("c072 rho 21/20 x 1/2 bps 11000", math.floor(10000 * (F(21, 20) - F(1, 2)) / (1 - F(1, 2))), 11000)
check("c075 rho 19/20 x 1/2 bps 9000", math.floor(10000 * (F(19, 20) - F(1, 2)) / (1 - F(1, 2))), 9000)
check("c075 rho/2 = 19/40", F(19, 20) / 2, F(19, 40))
check("c073 threshold 20/19", 1 / (1 - F(1, 20)), F(20, 19))
check("c074 measured ratio 1-h at rho=1", 1 * (1 - F(1, 20)), F(19, 20))

fails = [o for o in out if not o[1]]
for name, ok, detail in out:
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " :: " + detail))
print(f"checks {len(out)} pass {len(out) - len(fails)} fail {len(fails)}")
