from fractions import Fraction as F
import math
def hw(x):
    m=abs(x); w=math.floor(m+F(1,2)); return w if x>=0 else -w
y=F(400,10000)
ev=[(1,5000),(2,5000),(3,105000)]
pv=sum(F(a)/(1+y)**t for t,a in ev)
print("L1 exact", float(pv), "%.9f"%float(pv), hw(pv))
# rounding fixture
ev2=[(1,500),(2,500),(3,10500)]
pv2=sum(F(a)/(1+y)**t for t,a in ev2)
print("RF exact %.9f"%float(pv2), hw(pv2))
for t,a in ev2: print("term", t, "%.6f"%float(F(a)/(1+y)**t), hw(F(a)/(1+y)**t))
print("RF term sum", sum(hw(F(a)/(1+y)**t) for t,a in ev2))
print("FixB %.6f"%float(F(10500)/F(95,100)), hw(F(10500)/F(95,100)), F(210000,19)==F(10500)/F(95,100))
print("FixC", hw(F(10001*5000,10000)), "FixD", hw(F(1*5000,10000)))
