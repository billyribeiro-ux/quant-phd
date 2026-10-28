import math
from fractions import Fraction
s1 = math.sin(1.0)
print("sin1", repr(s1))
q = (math.cos(0.995)-math.cos(1.0))/(1-0.995)
print("E3 quotient", repr(q), "gap", repr(s1-q))
# getting the 10-digit values using mpmath-free approach: high precision via decimal series
from decimal import Decimal, getcontext
getcontext().prec = 50
def sin_d(x):
    x = Decimal(x); t = x; s = x; n = 1
    while True:
        t = -t*x*x/((2*n)*(2*n+1)); n += 1
        if abs(t) < Decimal(10)**-45: break
        s += t
    return s
def cos_d(x):
    x = Decimal(x); t = Decimal(1); s = Decimal(1); n = 1
    while True:
        t = -t*x*x/((2*n-1)*(2*n)); n += 1
        if abs(t) < Decimal(10)**-45: break
        s += t
    return s
q_d = (cos_d('0.995')-cos_d('1'))/Decimal('0.005')
print("E3 quotient hp", q_d)
print("sin1 hp", sin_d('1'), "gap hp", sin_d('1')-q_d)
# max over grid pairs
xs=[i/200 for i in range(201)]
best=(0,None,None)
for i,x in enumerate(xs):
    for y in xs[i+1:]:
        r=abs(math.cos(x)-math.cos(y))/(y-x)
        if r>best[0]: best=(r,x,y)
print("grid max", best)
# R2
beta=s1; eps=1e-6
import math
print("R2 bound n*", math.log(1/(eps*(1-beta)))/math.log(1/beta))
for n in (90,91): print(n, beta**n/(1-beta))
# M2 / Example 2.3
print(3/3**13, 3/3**14)
# E2
print(5/math.sqrt(26), 50/math.sqrt(2501))
# sqrt window gap
print(math.sqrt(26)-5, math.sqrt(2501)-50)
# E1
print(2.661258/0.05439523)
