import math
from fractions import Fraction as F
P=[5000,10000,20000]; Q=[F(1,4),F(1,2),F(1,4)]
print("E", sum(q*x for q,x in zip(Q,P)), "geo", math.exp(sum(float(q)*math.log(x) for q,x in zip(Q,P))))
for g in [0,0.25,0.5,2,4]:
    s=1-g
    M=sum(float(q)*x**s for q,x in zip(Q,P))
    ce=M**(1/s)
    print("gamma",g,"ce",round(ce,4),"half-up",math.floor(ce+0.5))
print("harm", 1/sum(q/x for q,x in zip(Q,P)), float(1/sum(q/x for q,x in zip(Q,P))))
# M1 of L03, M2, M3, E1-E3, example 2.5
print("M2 CE", 1/(F(1,4)*F(1,1000)+F(3,4)*F(1,9000)), "M3", 1/(F(1,4)*F(1,3000)+F(3,4)*F(1,27000)))
print("ex2.5", 1/(F(1,2)*F(1,1000)+F(1,2)*F(1,4000)), math.exp(0.5*math.log(1000)+0.5*math.log(4000)))
# R1 check numeric: two-outcome, x1->0
for g in [2.0,0.5]:
    s=1-g
    for x1 in [1e-2,1e-4,1e-8]:
        M=0.5*x1**s+0.5*100.0**s
        print("R1 g",g,"x1",x1,"CE",M**(1/s))
