"""FC2 slice a, round 1: independent recomputation of every displayed number in index.html, L01-L03."""
import math
from fractions import Fraction as Fr

def show(label, value, displayed):
    print(f"{label}: unrounded={value!r} displayed={displayed}")

# Hub placement
show("Pq5 NPV", -100 + 60 / 1.1 + 60 / 1.21, "4.13")
show("Pq6 DF2", 1 / 1.05**2, "0.9070")
show("skill1 parity gap", 10 - 4 - (100 - 105 * 0.95), "5.75")
show("skill2 forward", 100 * math.exp(0.05), "105.13")
print("7/9 =", round(7 / 9 * 100, 2), "percent; 8/9 =", round(8 / 9 * 100, 2), "percent")
print("hours: lessons", 6 + 8 + 9 + 7 + 8 + 8 + 8 + 6, "project 30, share", round(30 / 90 * 100, 1))

# L02
F = 5000 * math.exp(0.025)
show("L02 Ex2.4 F (dollars)", 50 * math.exp(0.025), "51.2658 (51.27 to cent)")
show("L02 Part A F (cents)", F, "5126.58")
show("L02 Part C quote-fair (cents)", 5200 - F, "73.42")
show("L02 E3 discounted (unrounded F)", F * math.exp(-0.0125), "5062.89")
show("L02 E3 discounted (displayed 5126.58)", 5126.58 * math.exp(-0.0125), "5062.89 (page text)")
show("L02 E3 value (unrounded F)", 5300 - F * math.exp(-0.0125), "237.11")
show("L02 E3 value (displayed 5126.58)", 5300 - 5126.58 * math.exp(-0.0125), "237.11 (page text)")
show("L02 M1 F (50 e^0.025)", 50 * math.exp(0.025), "51.265756")
show("L02 M1 from displayed 1.0253151", 50 * 1.0253151, "51.265756 (page text)")
show("L02 M2 F (80 e^0.01)", 80 * math.exp(0.01), "80.80401")
show("L02 M2 from displayed 1.0100502", 80 * 1.0100502, "80.80401 (page text)")
show("L02 M2 profit", 81 - 80 * math.exp(0.01), "0.20")
show("L02 M3 value", 104 - 100 * math.exp(-0.015), "5.49 (5.4888)")
show("L02 R3 e^0.1 - 1.05^2", math.exp(0.1) - 1.05**2, "0.0027")
show("L02 quiz e^0.1", math.exp(0.1), "1.1052")

# L03
dfs = [1 / 1.06, 1 / 1.06**2, 1 / 1.06**3]
show("L03 M3 annuity", sum(dfs), "2.673012")
print("L03 M3 annuity from displayed digits 0.943396+0.889996+0.839619 =", round(0.943396 + 0.889996 + 0.839619, 6))
show("L03 M3 value per notional", (0.06 - 0.05) * sum(dfs), "0.02673012")
show("L03 M2 DF3", 1.06**-3, "0.839619")
DF1 = Fr(100, 103)
DF2 = DF1 / Fr(105, 100)
R3 = (1 - DF2) / (DF1 + DF2)
show("L03 R3 par rate", float(R3), "0.039756 (3.9756%)")
show("L03 R3 flat 3% DF2", 1.03**-2, "0.942596")
print("L03 R3 displayed-digit ratio:", round((1 - 0.924642) / (0.970874 + 0.924642), 6))
# sums of discount factors can vanish: counterexample to the DF > 0 hypothesis in Prop 3.3
a, b = Fr(1, 2), Fr(-1, 2)
print("counterexample n=2: DF1=1/2, DF2=-1/2 -> sum DF =", a + b, "; 1-DF2 =", 1 - b, "; equation R*0 = 3/2 has no solution")
