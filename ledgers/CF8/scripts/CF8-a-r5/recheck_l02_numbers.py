from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP
def r2(x):
    return Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) if not isinstance(x, F) else (Decimal(x.numerator)/Decimal(x.denominator)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
def simple(d, early, late):
    return d/(1-d)*F(365, late-early)
def compound(d, early, late):
    return (1/(1-d))**(365/(late-early)) - 1
for lab, d, k, N in [("2/10 n30", F(2,100),10,30), ("1/10 n30", F(1,100),10,30), ("2/10 n60", F(2,100),10,60), ("3/15 n45", F(3,100),15,45), ("1/15 n45", F(1,100),15,45), ("fin 0.5 k10 N60", F(5,1000),10,60)]:
    s = simple(d,k,N)
    c = compound(float(d),k,N)
    print(lab, "simple exact", float(s*100), "compound%", c*100, "rounded", round(c*100,4))
# Example 1.4 digits
print("0.02/0.98*365/20 =", float(F(2,100)/F(98,100)*F(365,20)))
# Example 3.4 / lab B
rev0=F(12000000); N0=30; N1=45; drev=F(1500000); r=F(1,10)
dI = (rev0+drev)*N1/F(365) - rev0*N0/F(365)
print("dI", float(dI), "m*", float(r*dI/drev), "m* pct", float(r*dI/drev*100))
def npv(m, n, dI=dI, drev=drev, r=r):
    A = sum((1/(1+r))**t for t in range(1,n+1))
    return -dI + m*drev*A + dI/(1+r)**n
print("NPV at 5% n=5 =", float(npv(F(5,100),5)), "exact", npv(F(5,100),5))
print("NPV at m* n=5 exact:", npv(r*dI/drev,5)==0)
# M3
dI4 = F(216000000,365)
A4 = sum((1/F(108,100))**t for t in range(1,5))
t1 = -dI4; t2 = F(1,10)*600000*A4; t3 = dI4/F(108,100)**4
print("M2 dI", float(dI4), "A4", float(A4))
print("M3 terms", float(t1), float(t2), float(t3), "sum", float(t1+t2+t3))
print("M2 m* pct", float(F(8,100)*dI4/600000*100))
print("M3 check: (1-1.08^-4)/0.08=", float((1-F(1,1)/F(108,100)**4)/F(8,100)))
# E2
dI5 = F(990000000-600000000,365)
print("E2 dI", float(dI5), "m* pct", float(F(9,100)*dI5/2000000*100))
A5 = sum((1/F(109,100))**t for t in range(1,4))
print("E2 A(0.09,3)", float(A5))
npv5 = -dI5 + F(6,100)*2000000*A5 + dI5/F(109,100)**3
print("E2 NPV exact", float(npv5), "rounded", r2(npv5))
# R1
print("R1 m_nr", float(dI4/(600000*A4)), "pct", float(dI4/(600000*A4)*100), "ratio", float(1/(1-F(1,1)/F(108,100)**4)))
# E1 terms
print("E1 costs", float(simple(F(2,100),10,30)*100), float(simple(F(1,100),15,45)*100), float(simple(F(2,100),10,60)*100))
print("E1 bank 9% vs", float(F(9,100)))
print("M1 cost 1/15 n45 pct", float(simple(F(1,100),15,45)*100))
