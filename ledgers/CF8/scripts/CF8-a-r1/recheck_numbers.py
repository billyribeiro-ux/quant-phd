from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP
import math
def r2(x, q="0.01"):
    return Decimal(x.numerator)/Decimal(x.denominator) if isinstance(x,F) else Decimal(x)
def show(label, x):
    print(label, float(x))
# L02 Part A compounded
for lab,d,k,N in [("2/10 n30",F(2,100),10,30),("1/10 n30",F(1,100),10,30),("2/10 n60",F(2,100),10,60),("3/15 n45",F(3,100),15,45),("0.5 gap50",F(5,1000),10,60)]:
    gap=N-k if N is not None else 0
    simple = d/(1-d)*F(365,gap)
    comp = (1/(1-float(d)))**(365/gap)-1
    print(lab, "simple%", float(simple*100), "comp%", comp*100)
# Example 3.4 / Lab B
R0=F(12000000); dR=F(1500000); dI=((R0+dR)*45 - R0*30)/F(365)
r=F(1,10)
mstar=r*dI/dR
A=lambda r,n: sum((1+r)**-t for t in range(1,n+1))
npv=lambda m,n: -dI + m*dR*A(r,n) + dI*(1+r)**-n
print("dI", float(dI), "m*", float(mstar), "NPV5%", float(npv(F(5,100),5)))
# M3 / Q: M2 example
dI2=F(216000000,365); print("M2 dI", float(dI2), "m*", float(F(8,100)*dI2/600000))
A2=sum(F(1,1)/F(108,100)**t for t in range(1,5)); print("A(0.08,4)", float(A2))
print("NPV(0.10) M2", float(-dI2+F(1,10)*600000*A2+dI2*(F(100,108))**4))
# E2 (6pct)
dI3=F(390000000,365); A3=sum(F(1,1)/F(109,100)**t for t in range(1,4))
print("E2 dI",float(dI3),"m*",float(F(9,100)*dI3/2000000),"A(.09,3)",float(A3),"NPV6%",float(-dI3+F(6,100)*2000000*A3+dI3*F(100,109)**3))
# R1 ratio
print("R1 m_nr", float(dI2/(600000*A2)), "ratio", float(1/(1-F(100,108)**4)))
# M1 L02
print("M1L02", float(F(1,100)/F(99,100)*F(365,30)*100))
# E1 L02 bank: 
print("E1 2/10n60", float(F(2,98)*F(365,50)*100))
# Lab L01 Part D and C
print("L01 Part C exact", float(F(1200000000*0+9000000000*5, 365)))
print("L01 Part C cents", float(F(9000000000*5,365)), math.floor(F(9000000000*5,365)+F(1,2)))
print("65753.42", float(F(2400000*10,365)))
print("DSO2025 avg", float(F(1050000000+1200000000,2)*365/9000000000))
