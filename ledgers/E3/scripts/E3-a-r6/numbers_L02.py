import math
from fractions import Fraction as F
outs=[(40,F(1,4)),(100,F(1,2)),(160,F(1,4))]
EU=sum(float(p)*math.sqrt(x) for x,p in outs); CE=EU**2; EW=float(sum(p*x for x,p in outs))
print("W: EW",EW,"EU",round(EU,6),"CE",round(CE,6),"premium",round(EW-CE,6), "half-up cents CE", (CE*100))
g=[(-60,F(1,4)),(0,F(1,2)),(60,F(1,4))]
mean=sum(p*x for x,p in g); var=sum(p*x*x for x,p in g)-mean*mean
print("mean",mean,"var",var)
def ce(eps):
    e=sum(float(p)*math.sqrt(100+eps*x) for x,p in g); return e*e
for eps in [1,0.5,0.25,0.1,0.01]:
    prem=100-ce(eps); print("eps",eps,"ratio",round(prem/eps**2,6),"gap",round(abs(prem/eps**2-4.5),6))
print("rA",0.5/100, "rR",100*0.5/100, "approx", 0.5*0.005*1800)
print("err share exact", (5.065835-4.5)/5.065835, "over approx", (5.065835-4.5)/4.5)
print("half var", 0.5*1800, 900/5.065835)
print("gap ratio", 0.028811/0.004565, (0.25/0.1)**2)
print("cents 94.934165 ->", 94.934165*100, "5.065835 ->", 5.065835*100)
