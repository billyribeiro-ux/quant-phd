import math
from fractions import Fraction
print("3/4782969 =", 3/4782969, " 3/1594323 =", 3/1594323, " 3/3^13 check:", 3/3**13)
print("M2 n=13", 3*3**-13, "n=14", 3*3**-14)
b=math.sin(1.0); print("sin1", repr(b), "1-sin1", 1-b)
n=None
for k in range(0,200):
    if b**k/(1-b) <= 1e-6: n=k; break
print("R2 smallest n with bound<=1e-6:", n, "b^90/(1-b)=", b**90/(1-b), "b^91/(1-b)=", b**91/(1-b))
print("R2 formula:", math.log(1/(1e-6*(1-b)))/math.log(1/b))
q=(math.cos(0.995)-math.cos(1.0))/(1-0.995); print("E3 quotient", repr(q), "sin1-q", b-q, "sin1-0.8401167257", b-0.8401167257)
print("E1 ratio", 2.661258/0.05439523)
print("bound n=5", b**5/(1-b), "err n=5", abs(math.cos(math.cos(math.cos(math.cos(math.cos(0.0)))))-0.7390851332151607))
# part B max over grid pairs and location
GRID=200
xs=[i/GRID for i in range(GRID+1)]
best=(0,None)
for i,x in enumerate(xs):
    for y in xs[i+1:]:
        r=abs(math.cos(x)-math.cos(y))/(y-x)
        if r>best[0]: best=(r,(x,y))
print("partB max", best)
# E2 numbers
print("f'(5)", 5/math.sqrt(26), "f'(50)", 50/math.sqrt(2501))
def window(half):
    xs=[-half+2*half*i/GRID for i in range(GRID+1)]
    f=lambda x: math.sqrt(x*x+1)
    best=(0,None)
    for i,x in enumerate(xs):
        for y in xs[i+1:]:
            r=abs(f(x)-f(y))/(y-x)
            if r>best[0]: best=(r,(x,y))
    return best
print("win5", window(5.0)); print("win50", window(50.0))
print("L06 gap", Fraction(1,4)-Fraction(12,49), float(Fraction(1,4)-Fraction(12,49)))
