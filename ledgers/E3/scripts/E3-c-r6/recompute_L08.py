from fractions import Fraction as F
import math
W1,WL,W0=110000,95000,100000
def ce(p): return 1/(p/W1+(1-p)/WL)
print("EU avg", ce(F(1,2)), float(ce(F(1,2))), 4180000/41, "premium", 102500-float(ce(F(1,2))), 22500/41)
print("M1 ce(1/4)", float(ce(F(1,4))), float(F(1672000,17)), "exp", 0.25*110000+0.75*95000)
print("M2 ce(3/4)", float(ce(F(3,4))), "ce(1/4)", float(ce(F(1,4))))
print("M3 tau0 value 1/(3/4/W1+1/4/WL)", float(1/(F(3,4)/W1+F(1,4)/WL)))
print("Model4 maxmin", float(ce(F(1,3))), "alpha-meu", 1/(0.5*(1/3/W1+2/3/WL)+0.5*(2/3/W1+1/3/WL)))
print("known red", float(ce(F(1,3))), "known black CE", float(1/(F(2,3)/W1+F(1,3)/(W0))))
# Ex 2.5 with prizes 110000 / 100000
def ceb(p): return 1/(p/110000+(1-p)/100000)
print("Ex2.5 known red", float(ceb(F(1,3))), "black", float(ceb(F(2,3))))
print("R2 ambiguous red min over [1/3,2/3]", float(min(ceb(F(k,90)) for k in range(30,61))), "black min", float(min(ceb(1-F(k,90)) for k in range(30,61))))
# Model 2
v=lambda x: math.sqrt(x) if x>=0 else -2*math.sqrt(-x)
V=0.5*v(100)+0.5*v(-50); print("V",V, "5-sqrt50", 5-math.sqrt(50))
ce_chg=-((-V/2)**2); print("ce change CU", ce_chg, "wealth", W0+100*ce_chg, "check v(ce)", v(ce_chg), V)
# Model 4 alpha-meu at tau=1/2 vs EU
print("expected final wealth", 0.5*W1+0.5*WL)
# Prop 2.4 numeric check: worst prior for bet on red over k in 0..90 gives W0 CE
print("red worst", min(range(0,91), key=lambda k: float(ceb(F(k,90)))), "black worst", min(range(0,91), key=lambda k: float(ceb(1-F(k,90)))))
# Expression in Remark 2.3 vs Theorem: maxmin <= avg for k in 30..60 plus Lab
