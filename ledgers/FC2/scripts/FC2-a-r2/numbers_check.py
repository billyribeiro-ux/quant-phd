"""FC2-a round 2: independent recomputation of every displayed number in the hub and L01-L03 prose and quizzes.

Each line prints the recomputed value (exact Fraction or 80-digit Decimal where it matters) and the value the page
displays. Run from anywhere: python3 -I ledgers/FC2/scripts/FC2-a-r2/numbers_check.py
"""

from __future__ import annotations

import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 40


def e(x: Decimal) -> Decimal:
    return x.exp()


def show(label: str, value: object, displayed: str) -> None:
    print(f"{label}: computed {value} | page {displayed}")


print("== Hub placement items")
show("Pq1 E[X] die", Fraction(sum(range(1, 7)), 6), "3.5")
show("Pq2 Bernoulli(1/2) variance", Fraction(1, 2) * Fraction(1, 2), "0.25")
show("Pq5 NPV 100 out, 60 at 1 and 2 years, 10%", Decimal(-100) + Decimal(60) / Decimal("1.1") + Decimal(60) / Decimal("1.21"), "4.13 (4.1322)")
show("Pq6 DF two years 5%", Decimal(1) / Decimal("1.1025"), "0.9070")
show("Pq8 parity gap 10-4-(100-105*0.95)", Decimal(10) - Decimal(4) - (Decimal(100) - Decimal(105) * Decimal("0.95")), "5.75")
show("Pq9 F = 100 e^0.05", Decimal(100) * e(Decimal("0.05")), "105.13 (105.1271)")
show("7/9 correct as percent", Decimal(7) / Decimal(9) * 100, "78 (77.8) percent")
show("8/9 correct as percent", Decimal(8) / Decimal(9) * 100, "88.9")
show("hub bar lessons share 60/90 percent", Decimal(60) / Decimal(90) * 100, "66.7 / 33.3 percent width")

print("== L01")
p_bond, p_stock = Fraction(9, 10), Fraction(1)
psi_u = (p_stock - p_bond) / 2
psi_d = (Fraction(27, 10) - p_stock) / 2
show("Example 3.4 psi_u at q=1", psi_u, "1/20")
show("Example 3.4 psi_d at q=1", psi_d, "17/20")
show("state prices sum", psi_u + psi_d, "9/10")
q = Fraction(1, 2)
show("Part B psi_u at q=1/2", (q - Fraction(9, 10)) / 2, "-1/5")
show("Part B psi_d at q=1/2", (Fraction(27, 10) - q) / 2, "11/10")
show("Part B zero-cost holding (-5,9) cost", Fraction(-5) * Fraction(9, 10) + 9 * q, "0")
show("Part B payoff in u", -5 * 1 + 9 * 3, "22")
show("Part B payoff in d", -5 * 1 + 9 * 1, "4")
show("M1 cost 2 bonds - 1 stock at q=1", 2 * p_bond - 1, "4/5")
show("M1 payoff u", 2 * 1 - 3, "-1")
show("M2 psi_u with bond 4/5 stock 1", (Fraction(1) - Fraction(4, 5)) / 2, "1/10")
show("M2 psi_d", Fraction(4, 5) - Fraction(1, 10), "7/10")
show("misconception cost 1 - 2*9/10", Fraction(1) - 2 * p_bond, "-4/5")
show("R1 range check psi_w example eps", "n/a", "symbolic")
show("E2/box count 30 (recomputed in lab_check.py)", "see lab_check.py", "30")

# Lab 1 counts: recomputed independently in lab_check.py below
print("== L02")
S = Decimal(50)
show("Example 2.4 50 e^0.025", S * e(Decimal("0.025")), "51.2658 (51.27)")
show("Lab 2 A fair cents 5000 e^0.025", Decimal(5000) * e(Decimal("0.025")), "5126.58")
show("Lab 2 C gain 5200 - fair", Decimal(5200) - Decimal(5000) * e(Decimal("0.025")), "73.42")
for s in (3000, 4500, 6000, 7500):
    fwd = Decimal(s) - Decimal(5000) * e(Decimal("0.025"))
    print(f"  Lab 2 B spot {s}: forward payoff {fwd:.4f} (page shows {fwd:.2f})")
    gain = (Decimal(5200) - Decimal(s)) + (Decimal(s) - Decimal(5000) * e(Decimal("0.025")))
    print(f"  Lab 2 C spot {s}: net {gain:.4f}")
v = Decimal(5300) - Decimal(5000) * e(Decimal("0.025")) * e(Decimal("-0.0125"))
show("Lab 2 E value after 0.25 y spot 5300", v, "237.11 (E3 text 237.1077)")
show("E3 e^-0.0125", e(Decimal("-0.0125")), "0.98757780")
show("E3 F e^-0.0125", Decimal(5000) * e(Decimal("0.025")) * e(Decimal("-0.0125")), "5062.8923")
show("Lab 2 A fair price, unrounded", Decimal(5000) * e(Decimal("0.025")), "5126.5756 (E3)")
show("M1 50 e^0.025 dollars", Decimal(50) * e(Decimal("0.025")), "51.265756")
show("e^0.025", e(Decimal("0.025")), "1.0253151205")
show("M2 80 e^0.01", Decimal(80) * e(Decimal("0.01")), "80.804013")
show("M2 e^0.01", e(Decimal("0.01")), "1.0100501671")
show("M2 profit 81 - 80.804013", Decimal(81) - Decimal("80.804013"), "0.195987 -> 0.20")
show("M3 100 e^-0.015", Decimal(100) * e(Decimal("-0.015")), "98.5112")
show("M3 e^-0.015", e(Decimal("-0.015")), "0.985112")
show("M3 value 104 - 98.5112", Decimal(104) - Decimal("98.5112"), "5.4888 -> 5.49")
show("R3 annual 1.05^2", Decimal("1.05") ** 2, "1.1025")
show("R3 e^0.1", e(Decimal("0.1")), "1.105171")
show("R3 difference e^0.1 - 1.1025", e(Decimal("0.1")) - Decimal("1.1025"), "0.002671 -> 0.0027")
show("quiz e^0.1 to four places", e(Decimal("0.1")).quantize(Decimal("0.0001")), "1.1052")
show("Prop 3.1 hub 5 e^-0.0125 ... see above", "-", "-")
show("Remark 2.5 no value", "-", "-")

print("== L03")
flat = Fraction(3, 100)
rates = [Fraction(3, 100), Fraction(7, 200), Fraction(4, 100), Fraction(9, 200), Fraction(5, 100)]
dfs = [Fraction(1)]
for i, z in enumerate(rates, start=1):
    dfs.append(Fraction(1) / (1 + z) ** i)
for i in range(1, 6):
    print(f"  DF_{i} = {float(dfs[i]):.6f}")
annuity = sum(dfs[1:], Fraction(0))
par = (1 - dfs[5]) / annuity
show("par rate (exact)", float(par), "0.049026")
show("par rate in percent to four places", f"{float(par) * 100:.4f}", "4.9026")
notional = 100_000_000
payment = par * notional
show("fixed payment cents unrounded", float(payment), "4902625 (half-up)")
show("value to payer cents unrounded", float(-Fraction(1, 100) * annuity * notional), "-4415468")
show("annuity", float(annuity), "4.415468 (not printed)")
show("payment dollars", float(payment) / 100, "49026.25")
for rate in rates:
    print(f"  zero rate {float(rate):.4f} vs par {float(par):.6f}")
show("M2 DF_3 at 6%", 1 / 1.06**3, "0.839619")
show("M2 1.06^3", 1.06**3, "1.191016")
dfm = [1 / 1.06, 1 / 1.06**2, 1 / 1.06**3]
show("M3 sum DF flat 6%", sum(dfm), "2.6730119")
show("M3 displayed digits 0.943396 0.889996 0.839619 sum", round(dfm[0], 6) + round(dfm[1], 6) + round(dfm[2], 6), "2.673011")
show("M3 value per unit", 0.01 * sum(dfm), "0.026730119")
show("M3 on 100 dollars", 100 * 0.01 * sum(dfm), "2.67")
show("R3 DF_1", Fraction(1) / Fraction(103, 100), "0.970874")
df2 = Fraction(1) / Fraction(103, 100) / Fraction(105, 100)
show("R3 DF_2 = DF_1/1.05", float(df2), "0.924642")
show("R3 par", float((1 - df2) / (Fraction(1) / Fraction(103, 100) + df2)), "0.039756 (3.9756 percent)")
show("R3 flat 3% DF_2", 1.03 ** -2, "0.942596")
show("R2 example weights sum", "n/a", "symbolic")
show("E3/P2 value -h annuity", float(-Fraction(1, 100) * annuity * notional), "-4415468")
show("Lab 3 A start/path check", "see lab_check.py", "path printed")
print("== L03 E1 check, margins from printed path")
path = [5000, 5039, 5070, 5104, 5069, 5103, 5090, 5054, 5077, 5106, 5084]
margins = [path[i] - path[i - 1] for i in range(1, len(path))]
show("margins", margins, "39 31 34 -35 34 -13 -36 23 29 -22")
show("sum of margins minus (path[-1]-path[0])", sum(margins) - (path[-1] - path[0]), "0")
show("loss days", sum(1 for m in margins if m < 0), "4")
show("largest loss", min(margins), "-36 on day 7")
print("== numeric check of the value using floats (not used for any page claim)")
print("math.exp(0.025)*5000 =", 5000 * math.exp(0.025))
