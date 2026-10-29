import math
from fractions import Fraction
e=math.exp
print("c021", 50*e(0.025))
r=0.05; s=0.2; t=1.0; h=0.25
u=e(s*math.sqrt(h)); d=1/u; R=e(r*h); q=(R-d)/(u-d)
print("c115 u d R q", round(u,6), round(d,6), round(R,6), round(q,7), h < s*s/(r*r))
u1=e(0.2); q1=(e(0.05)-1/u1)/(u1-1/u1); print("c116", u1, q1, 100*( q1*(100*u1-100)/e(0.05)) if False else None)
V1=(q1*max(100*u1-100,0)+(1-q1)*0)*e(-0.05); print("c116 V1", V1)
print("c109 BS", None)
print("c126 L", 100-100*e(-0.05))
print("c131", 120*e(-0.05))
print("c076", 100*e(-0.1)-50)
print("c056 10*(9/10)^4", 10*(0.9)**4)
print("c057 20*(0.9)^3", 20*0.9**3)
print("c061 profit", 25-8)
