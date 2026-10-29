import math
from fractions import Fraction as F
print("pi/4", math.pi/4, "arctan2-pi/4", math.atan(2)-math.pi/4)
print("9*c", 9*(math.atan(2)-math.pi/4), "10*c", 10*(math.atan(2)-math.pi/4))
print("quad err", 0.7853982936-math.pi/4, -0.7853982936+math.pi/4)
print("E1 diff", 0.7853982936-0.7853981634)
print("L05 quiz 4/3", abs(4/3-1.3333), "pi/4 vs .7854", abs(math.pi/4-0.7854), "q8", abs(math.atan(2)-math.pi/4-0.3217505544))
print("L06 q5 1/3 vs .3333", abs(1/3-0.3333), "L08 q5", abs(2/3-0.6667), abs(-2/3+0.6667), "L07 q9", abs(767/140-5.4785714286))
# L05 M1
I1 = F(1,2)*(F(1)*F(1,3)+F(2)*F(2,3)) + F(1,2)*(F(3)*F(1,3))
I2 = F(1,3)*(F(1)*F(1,2)+F(3)*F(1,2)) + F(2,3)*(F(2)*F(1,2))
print("L05 M1", I1, I2)
# L06 M2, M3, E1, Remark 2.4, R1
mu=(F(1,4),)*4; nu=(F(1,8),F(1,8),F(1,4),F(1,2))
f=[n/m for n,m in zip(nu,mu)]; g=(0,1,2,3)
print("L06 M2 f", f, "M3", sum(gi*n for gi,n in zip(g,nu)), sum(gi*fi*m for gi,fi,m in zip(g,f,mu)))
# L07 M1 M3
X=[1,2,3,6]; Y=[F(3,2),F(3,2),F(9,2),F(9,2)]
print("L07 M3", sum((F(x)-y)**2 for x,y in zip(X,Y))/4, sum((F(x)-3)**2 for x in X)/4)
# L08 M2 M3 R1
p=F(1,3)
paths=[(a,b) for a in (1,-1) for b in (1,-1)]
w=lambda P: (p if P[0]==1 else 1-p)*(p if P[1]==1 else 1-p)
print("L08 M2 E[S2]", sum(w(P)*sum(P) for P in paths), "weights", [w(P) for P in paths])
print("L08 M3 avg", (p*2+(1-p)*0))
# L07 Part C spot: MSE of cell average recomputed independently
P=[F(n,16) for n in (1,2,1,3,2,3,2,2)]; XX=[F(v) for v in (2,-1,4,0,3,-2,1,5)]
cells=[(0,1,2),(3,4),(5,6,7)]
Yv=[None]*8
for c in cells:
    pc=sum(P[i] for i in c); av=sum(P[i]*XX[i] for i in c)/pc
    for i in c: Yv[i]=av
print("L07 avg mse", sum(P[i]*(XX[i]-Yv[i])**2 for i in range(8)), float(sum(P[i]*(XX[i]-Yv[i])**2 for i in range(8))))
print("L07 E[X]", sum(P[i]*XX[i] for i in range(8)))
# L07 E2 / projection
print("E2 proj on cell0", F(6,7)-F(1,5)+F(12,35))
