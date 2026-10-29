import math, random
from fractions import Fraction as F
from decimal import Decimal, getcontext
getcontext().prec=50
# L02 numerics
S=5000; r=0.05; tau=0.5
fair=S*math.exp(r*tau); print("L02 fair", fair, "E3 value", 5300-fair*math.exp(-r*0.25), "F*e^-0.0125", fair*math.exp(-0.0125), "e^-0.0125", math.exp(-0.0125))
print("M1 e^.025", math.exp(0.025), "50x", 50*math.exp(0.025))
print("M2 e^.01", math.exp(0.01), 80*math.exp(0.01), 81-80*math.exp(0.01))
print("M3 e^-.015", math.exp(-0.015), 104-100*math.exp(-0.015))
print("R3 annual vs cont", 1.05**2, math.exp(0.1), math.exp(0.1)-1.05**2)
print("e^0.1 4dp", round(math.exp(0.1),4), math.exp(0.1))
# L03 numerics
rates=[F(3,100),F(7,200),F(4,100),F(9,200),F(5,100)]
dfs=[F(1)]+[F(1)/(1+z)**i for i,z in enumerate(rates,1)]
ann=sum(dfs[1:],F(0)); R=(1-dfs[-1])/ann
print("DFs", [round(float(d),9) for d in dfs[1:]], "par", float(R), "par digits", float(R)*100)
N=100_000_000
pay=R*N; print("payment exact", float(pay), "half-up", math.floor(pay+F(1,2)))
val=-F(1,100)*ann*N; print("value", float(val), math.floor(val+F(1,2)))
M3=[1/1.06,1/1.06**2,1/1.06**3]; print("M3 DFs", M3, sum(M3), [round(x,6) for x in M3], sum(round(x,6) for x in M3))
print("M3 value per notional 100", 100*0.01*sum(M3))
print("M2 DF3", 1/1.06**3, round(1/1.06**3,6))
# R3 two-period
DF1=1/1.03; DF2=DF1/1.05
print("R3 DF1 DF2", DF1, DF2, "par", (1-DF2)/(DF1+DF2), "flat3 DF2", 1.03**-2)
d1=round(DF1,6); d2=round(DF2,6); print("R3 rounded inputs", (1-d2)/(d1+d2))
# L03 path
rng=random.Random(20261028); path=[5000]
for _ in range(10): path.append(path[-1]+rng.randint(-40,40))
print("path", path)
m=[path[i]-path[i-1] for i in range(1,11)]; print("margins", m, sum(m), sum(1 for x in m if x<0))
# E3 payment dollars
print("payment dollars", 4902625/100)
# C-check: DF rounded sum used in lab text
print("sum 6dp DF M3", 0.943396+0.889996+0.839619)
