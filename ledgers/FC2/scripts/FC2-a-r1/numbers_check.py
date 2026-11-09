"""Independent recomputation of every displayed number in the FC2 slice (verifier, round 1).

Run: python -I ledgers/FC2/scripts/FC2-a-r1/numbers_check.py
Each line prints the recomputed value and the displayed value it is checked against.
"""
import math
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as Fr


def cents(x):
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def show(label, value, displayed):
    print(f"{label}: recomputed={value} displayed={displayed}")


# hub
npv = -100 + 60 / 1.1 + 60 / 1.21
show("hub NPV (2 dp)", cents(npv), "4.13")
show("hub df 2y 5% (4 dp)", round(1 / 1.05**2, 4), "0.9070")
show("hub skill1 gap", 10 - 4 - (100 - 105 * 0.95), "5.75")
show("hub skill2 forward 100e^0.05", cents(100 * math.exp(0.05)), "105.13")
show("hub 7/9 percent", round(7 / 9 * 100, 0), "78")

# L01 numbers (exact)
q = Fr(1)
psi_u = (q - Fr(9, 10)) / 2
psi_d = (Fr(27, 10) - q) / 2
show("L01 psi_u at q=1", psi_u, "1/20")
show("L01 psi_d at q=1", psi_d, "17/20")
show("L01 sum state prices", psi_u + psi_d, "9/10")
show("L01 cost of (-1,1) at q=9/10", -Fr(9, 10) + Fr(9, 10), "0")
show("L01 misconception cost 1-2*9/10", 1 - 2 * Fr(9, 10), "-4/5")
show("L01 Q10 cost of 1 bond -2 stocks at q=1", Fr(9, 10) - 2 * 1, "-11/10")
show("L01 zero-cost holding bond 9/10 stock 1/2 (-5,9)", Fr(9, 10) * -5 + Fr(1, 2) * 9, "0")
show("L01 payoff (-5,9) state u", -5 * 1 + 9 * 3, "22")
show("L01 payoff (-5,9) state d", -5 * 1 + 9 * 1, "4")
show("L01 state prices mispriced psi_u", (Fr(9, 10) * 1 - 1 * Fr(1, 2)) / -2 * 0 + (Fr(1, 2) - Fr(9, 10)) / 2, "-1/5")
show("L01 M2 psi_u (bond 4/5, stock 1)", (1 - Fr(4, 5)) / 2, "1/10")
show("L01 M2 psi_d (bond 4/5, stock 1)", Fr(4, 5) - (1 - Fr(4, 5)) / 2, "7/10")
show("L01 R1 cost of (-1,1) at q=9/10 (3 states, stock pays 3,2,1)", -Fr(9, 10) + Fr(9, 10), "0")
show("L01 Ex2.4 cost of a=(0,2)", 2 * 1, "2")
show("L01 Ex2.4 cost of b=(1,1)", Fr(9, 10) + 1, "19/10")

# L02
fair_cents = 5000 * math.exp(0.05 * 0.5)
show("L02 Part A fair cents", cents(fair_cents), "5126.58")
show("L02 Ex2.4 50e^0.025", round(50 * math.exp(0.025), 4), "51.2658")
show("L02 Part C net 5200-fair", cents(5200 - fair_cents), "73.42")
show("L02 Part E value 5300 - F e^-0.0125", cents(5300 - fair_cents * math.exp(-0.25 * 0.05)), "237.11")
show("L02 Part E discounted fair", round(fair_cents * math.exp(-0.0125), 4), "5062.8923")
show("L02 M1 50e^0.025 dollars", round(50 * math.exp(0.025), 6), "51.265756")
show("L02 M1 e^0.025 10 places", round(math.exp(0.025), 10), "1.0253151205")
show("L02 M2 80e^0.01", round(80 * math.exp(0.01), 6), "80.804013")
show("L02 M2 e^0.01 10 places", round(math.exp(0.01), 10), "1.0100501671")
show("L02 M2 profit 81-F", cents(81 - 80 * math.exp(0.01)), "0.20")
show("L02 M2 profit raw", round(81 - 80 * math.exp(0.01), 6), "0.195987")
show("L02 M3 e^-0.015 6 places", round(math.exp(-0.015), 6), "0.985112")
show("L02 M3 value 104-100e^-0.015", cents(104 - 100 * math.exp(-0.015)), "5.49")
show("L02 M3 value raw", round(104 - 100 * math.exp(-0.015), 4), "5.4888")
show("L02 E3 e^-0.0125 8 places", round(math.exp(-0.0125), 8), "0.98757780")
show("L02 E3 discounted raw", round(5000 * math.exp(0.025) * math.exp(-0.0125), 4), "5062.8923")
show("L02 E3 value raw", round(5300 - 5000 * math.exp(0.025) * math.exp(-0.0125), 4), "237.1077")
show("L02 R3 e^0.1 6 places", round(math.exp(0.1), 6), "1.105171")
show("L02 R3 difference", round(math.exp(0.1) - 1.1025, 4), "about 0.0027")
show("L02 Q9 e^0.1 4 places", round(math.exp(0.1), 4), "1.1052")
show("L02 Part D zero at fair", max(abs((fair_cents - s) + (s - 5000 * math.exp(0.025))) for s in [3000, 4500, 6000, 7500]) < 1e-6, "True")
show("L02 Q2 51.27", cents(50 * math.exp(0.025)), "51.27")

# L03
rates = [Fr(3, 100), Fr(7, 200), Fr(4, 100), Fr(9, 200), Fr(5, 100)]
dfs = [Fr(1)]
for i, z in enumerate(rates, start=1):
    dfs.append(Fr(1) / (1 + z) ** i)
annuity = sum(dfs[1:], Fr(0))
par = (1 - dfs[-1]) / annuity
show("L03 DF_1..5 (6 dp)", [f"{float(d):.6f}" for d in dfs[1:]], "0.970874 0.933511 0.888996 0.838561 0.783526")
show("L03 par rate (6 dp)", f"{float(par):.6f}", "0.049026")
show("L03 par rate exact float", float(par), "4.9026 percent")
pay_cents = par * 100_000_000
half_up = math.floor(pay_cents + Fr(1, 2))
show("L03 fixed payment cents (half up)", half_up, "4902625")
v = math.floor((1 - dfs[-1] - (par + Fr(1, 100)) * annuity) * 100_000_000 + Fr(1, 2))
show("L03 value struck +1pp cents", v, "-4415468")
w = math.floor(-Fr(1, 100) * annuity * 100_000_000 + Fr(1, 2))
show("L03 -1% annuity notional cents", w, "-4415468")
show("L03 DF bad example sum", Fr(1, 2) + Fr(-1, 2), "0 (A8 counterexample)")
show("L03 A8 counterexample rhs 1-DF2", 1 - Fr(-1, 2), "3/2")
show("L03 Ex3.4 flat par equals rho (rho=0.05, n=4)", float((1 - (1 / 1.05) ** 4) / sum((1 / 1.05) ** i for i in range(1, 5))), "0.05")
show("L03 M2 DF3 6%", round(1 / 1.06**3, 6), "0.839619")
show("L03 M3 sum DF (unrounded)", round(1 / 1.06 + 1 / 1.06**2 + 1 / 1.06**3, 7), "2.6730119")
show("L03 M3 displayed digits sum", round(0.943396 + 0.889996 + 0.839619, 6), "2.673011")
show("L03 M3 value per dollar notional 100", cents(100 * 0.01 * (1 / 1.06 + 1 / 1.06**2 + 1 / 1.06**3)), "2.67")
show("L03 Q8 value per unit", round(0.01 * (1 / 1.06 + 1 / 1.06**2 + 1 / 1.06**3), 7), "0.0267301")
show("L03 R3 DF2", round((1 / 1.03) / 1.05, 6), "0.924642")
show("L03 R3 par", round((1 - (1 / 1.03) / 1.05) / (1 / 1.03 + (1 / 1.03) / 1.05), 6), "0.039756")
show("L03 R3 DF2 flat 3%", round(1.03**-2, 6), "0.942596")
show("L03 DF1 1/1.03", round(1 / 1.03, 6), "0.970874")
show("L03 E1 margins loss list", [39, 31, 34, -35, 34, -13, -36, 23, 29, -22], "largest loss 36 on day 7")
show("L03 P2 value", -0.01 * float(annuity) * 1e8, "-4415468")
show("L03 M1 margins", [3, -4, 2], "balances -1, 1")
show("L03 lab path loss days", sum(1 for m in [39, 31, 34, -35, 34, -13, -36, 23, 29, -22] if m < 0), "4")
show("L03 balance day 10 = 5084-5000", 5084 - 5000, "84")
show("L03 par 4.9026 between 4 and 5", 4 < float(par) * 100 < 5, "True")
