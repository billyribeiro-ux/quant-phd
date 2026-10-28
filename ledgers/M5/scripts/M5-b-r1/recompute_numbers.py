import math
from fractions import Fraction as F
b=math.sin(1)
print("sin1", b)
print("E3 quotient", (math.cos(0.995)-math.cos(1))/(1-0.995), "gap to sin1", b-(math.cos(0.995)-math.cos(1))/0.005)
print("E2 f'(5)", 5/math.sqrt(26), "f'(50)", 50/math.sqrt(2501))
print("E1 ratio", 2.661258/0.05439523, "bound n=5", b**5/(1-b), "err n=5 recomputed")
x=0.0
xs=[]
for _ in range(400): x=math.cos(x)
xstar=x
y=0.0
for n in range(6):
    if n==5: print("iterate5",y,"err",abs(y-xstar),"bound",b**5/(1-b))
    y=math.cos(y)
print("R2 n", (math.log(1/(1e-6*(1-b))))/math.log(1/b))
print("R2 bound at 91 and 90", b**91/(1-b), b**90/(1-b))
print("M2 3^-13*3", 3/3**13, "3/3^14", 3/3**14)
print("L07 Example 2.3 check", all(abs(abs((3-3*3.0**-n)-3)-3*3.0**-n)<1e-15 for n in range(20)))
print("L05 0.99^100", 0.99**100, math.log(0.99))
print("L06 gap", F(1,4)-F(12,49), float(F(1,4)-F(12,49)))
print("L06 width", 1/256)
# Lab L07 Part C with a second-check: is there any pair with ratio >=1 on grid? (should be no)
def ratio(half,N=200):
    xs=[-half+2*half*i/N for i in range(N+1)]
    f=lambda t: math.sqrt(t*t+1)
    best=0
    for i,x in enumerate(xs):
        for yy in xs[i+1:]:
            best=max(best,abs(f(x)-f(yy))/(yy-x))
    return best
print("ratio half 5", ratio(5), "half 50", ratio(50))
# maximum of |cos'| on [0,1]
print("sin t max on [0,1]", math.sin(1))
