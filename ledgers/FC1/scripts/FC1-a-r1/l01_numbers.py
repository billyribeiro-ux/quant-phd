from fractions import Fraction
import math
d=Fraction(1000); rho=Fraction(1,10)
def cents(x): return math.floor(x*100+Fraction(1,2))
for share in (Fraction(1),Fraction(1,2)):
    D=[d]
    for _ in range(10): D.append(share*(1-rho)*D[-1])
    print(share, float(sum(D)), cents(sum(D,Fraction(0))), float(sum(D)))
print("S10 exact", float(d*(1-Fraction(9,10)**11)/rho), cents(d*(1-Fraction(9,10)**11)/rho))
print("half limit", float(d/(1-Fraction(1,2)*(1-rho))), cents(d/(1-Fraction(1,2)*(1-rho))))
print("ratio exact", (d/(1-Fraction(1,2)*(1-rho)))/(d/rho))
print("M2", 800*(1-Fraction(3,4)**3)/Fraction(1,4))
