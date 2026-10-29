"""Independent re-derivation of L02 and L03 prose numbers (FC2-a round 3). Standard library only."""
import math
from fractions import Fraction as F
from decimal import Decimal, getcontext
getcontext().prec = 30
e = lambda x: Decimal(repr(x)).exp() if False else None
def dexp(x):  # high-precision exp via Decimal
    return Decimal(x).exp()
print("e^0.025", dexp(Decimal("0.025")))
print("50 e^0.025", Decimal(50)*dexp(Decimal("0.025")))
print("e^0.01", dexp(Decimal("0.01")), "80e^0.01", Decimal(80)*dexp(Decimal("0.01")))
print("e^-0.015", dexp(Decimal("-0.015")), "100e^-0.015", Decimal(100)*dexp(Decimal("-0.015")))
print("e^-0.0125", dexp(Decimal("-0.0125")))
S = Decimal(5000); fair = S*dexp(Decimal("0.025")); print("fair cents", fair)
print("value cents", Decimal(5300) - fair*dexp(Decimal("-0.0125")))
print("e^0.1", dexp(Decimal("0.1")), "diff vs 1.1025", Decimal("1.1025")-dexp(Decimal("0.1")))
print("e^0.1 vs 1.1052 check", dexp(Decimal("0.1")))
print("QUOTE-fair", 5200 - fair)
# L03 margin path check
import random
rng = random.Random(20261028); path=[5000]
for _ in range(10): path.append(path[-1]+rng.randint(-40,40))
m=[path[i]-path[i-1] for i in range(1,11)]
print("path", path); print("margins", m, "losses", sum(1 for x in m if x<0), "balance", sum(m))
# L03 Part B
Z=[F(3,100),F(7,200),F(4,100),F(9,200),F(5,100)]
DF=[F(1)]+[1/(1+z)**(i) for i,z in enumerate(Z,1)]
ann=sum(DF[1:],F(0)); R=(1-DF[5])/ann
print("DF", [round(float(d),6) for d in DF[1:]]); print("par", float(R), float(R)*100)
print("payment cents", R*100_000_000, "value cents", -F(1,100)*ann*100_000_000)
# M3 and M2
d3=[1/F(106,100), 1/F(1236,1000)*0+1/(F(106,100)**2), 1/(F(106,100)**3)]
print("M3 sum", float(sum(d3)), "DF3", float(1/F(106,100)**3))
print("M2 DF3 check", float(F(1,1)/F(1191016,1000000)))
# R3 two-period
df1 = 1/F(103,100); df2 = df1/F(105,100)
print("R3 df1", float(df1), "df2", float(df2))
Rp = (1-df2)/(df1+df2)
print("R3 Rpar exact", float(Rp), "to 4 places (percent)", round(float(Rp)*100, 4))
print("flat 3pct DF2", 1.03**-2)
# P2 check
print("E3 cents->dollars", 4902625/100)
