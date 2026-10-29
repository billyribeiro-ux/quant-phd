from fractions import Fraction as Fr
import math
m=2500-1150; F=120000; S=2700000
q1=Fr(F,m); q2=Fr(F+S,m)
print("q1",float(q1),"ceil",math.ceil(q1),"q2",float(q2))
OI=lambda u: m*u-F-(S if u>2000 else 0)
print("OI88",OI(88),"OI89",OI(89),"OI2000",OI(2000),"OI2001",OI(2001),"OI2088",OI(2088),"OI2089",OI(2089))
print("margin_safety", 2500-float(q2), (2500-float(q2))/2500*100)
print("DOL", m*2500/OI(2500), "1pct", (OI(2525)-OI(2500))/OI(2500)*100)
print("dF 10000 move", float(Fr(F+10000,m)-q1), "per 100 USD", 100/13.5)
print("R2 deriv per USD", -F/(m**2)*100, "exact 1USD", float(Fr(F,1450)-Fr(F,1350)), float(Fr(F,1450)))
print("revenue BE", 2500*0+25*float(q1)/1, float(Fr(F,1)*Fr(2500,1)/Fr(m,1))/100)
print("E2 from first", 2500-float(q1))
print("M1",45000/30,30/80,45000/0.375, 45000+50*1500)
print("M2",10000/7, 7*1429-10000, 7*1428-10000)
print("prop 3.3 ex", 10000/13.5)
