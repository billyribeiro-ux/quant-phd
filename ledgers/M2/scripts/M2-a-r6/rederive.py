"""Independent re-derivation of the numbers printed or claimed on M2 hub and L01-L06 (verifier round 6)."""
from fractions import Fraction as F
import math, re, html, sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyB6-M2-a/course/modules/M/M2/"
out = []
def check(name, got, want, tol=0.0):
    ok = abs(float(got) - float(want)) <= tol if tol else got == want
    out.append((name, ok, got, want))

# L01 Example 2.3 and Lab 1
a = lambda n: F(2*n+1, n+1)
check("L01 err(999)=1/1000", abs(a(999)-2), F(1,1000))
check("L01 least N eps=1/1000 is 1000", min(N for N in range(1,5001) if all(abs(a(n)-2) < F(1,1000) for n in range(N,5001))), 1000)
check("L01 a_1000 to 6dp", round(float(a(1000)),6), 1.999001, 1e-9)
check("L01 N for eps=1e-4 is 10000", min(N for N in range(1,20001) if all(abs(a(n)-2) < F(1,10**4) for n in range(N,20001))), 10000)
check("L01 |a_9-2|=0.1", abs(a(9)-2), F(1,10))
# L01 mech-1: a_n=(3n-1)/(n+4), eps=0.01 threshold 1297
b = lambda n: F(3*n-1, n+4)
check("L01 mech-1 N=1297", min(N for N in range(1,3000) if all(abs(b(n)-3) < F(1,100) for n in range(N,3000))), 1297)
# L01 mech-2: least N with 1/n^2<0.01 for all n>=N is 11
check("L01 mech-2 N=11", min(N for N in range(1,100) if all(F(1,n*n) < F(1,100) for n in range(N,100))), 11)
# L01 R3 / res-2 fine; L02 Lab errors
A = lambda n: F(2*n+1,n+1); B = lambda n: F(n+2,n)
for n in (1,10,100,1000,10000):
    se = abs(A(n)+B(n)-3); pe = abs(A(n)*B(n)-2); qe = abs(A(n)/B(n)-2)
    check(f"L02 sum closed form n={n}", se, F(n+2, n*(n+1)))
    check(f"L02 prod closed form n={n}", pe, F(3*n+2, n*(n+1)))
    check(f"L02 quot closed form n={n}", qe, F(5*n+4, (n+1)*(n+2)))
check("L02 E2 302/10100", F(302,10100), F(3*100+2, 100*101))
check("L02 E1 6/55", F(12,110), F(6,55))
check("L02 E3 quotient n=1 = 3/2", abs(A(1)/B(1)-2), F(3,2))
# L03 gap formula 1+4h-h^2 and values
f3 = lambda x: x*x if x < 1 else 2*x
for k in range(1,5):
    h = F(1,10**k)
    check(f"L03 gap 1+4h-h^2 k={k}", f3(1+h)-f3(1-h), 1+4*h-h*h)
check("L03 E2 1+4(.01)-(.01)^2", 1+4*F(1,100)-F(1,10000), F(10399,10000))
check("L03 h=0.1 gap 1.39", f3(1+F(1,10))-f3(1-F(1,10)), F(139,100))
# L04 quotient of x^3 at 1
Q = lambda h: ((1+h)**3-1)/h
for k in range(1,7):
    h = F(1,10**k)
    check(f"L04 Q=3+3h+h^2 k={k}", Q(h), 3+3*h+h*h)
check("L04 Q(0.001)=3.003001", Q(F(1,1000)), F(3003001,1000000))
check("L04 E2 error at 1e-5", Q(F(1,10**5))-3, F(3,10**5)+F(1,10**10))
# L04 M3: f=1/x, Q at 2
check("L04 M3 Q(h)=-1/(2(2+h))", (1/(2+F(1,10**6))-F(1,2))/F(1,10**6), -1/(2*(2+F(1,10**6))))
# L05 analytic values and exact central-difference errors
x = F(3,2)
p = lambda t: (t*t+1)*t**3
q = lambda t: (t*t+1)/(t+2)
c = lambda t: (t*t+1)**3
pp = lambda t: 2*t*t**3 + (t*t+1)*3*t*t
qp = lambda t: (t*t+4*t-1)/(t+2)**2
cp = lambda t: 6*t*(t*t+1)**2
H = F(1,10**4)
cd = lambda f_, t: (f_(t+H)-f_(t-H))/(2*H)
check("L05 p'(1.5)=32.0625", pp(x), F(513,16))
check("L05 q'(1.5)=29/49", qp(x), F(29,49))
check("L05 c'(1.5)=95.0625", cp(x), F(1521,16))
check("L05 cd-exact p err ~2.350e-7", float(abs(cd(p,x)-pp(x))), 2.350e-7, 1e-10)
check("L05 cd-exact q err ~3.328e-10", float(abs(cd(q,x)-qp(x))), 3.328e-10, 1e-13)
check("L05 cd-exact c err ~8.550e-7", float(abs(cd(c,x)-cp(x))), 8.550e-7, 1e-10)
check("L05 p'''(1.5)=141", 60*x*x+6, 141)
check("L05 x^3 central diff error = h^2 exactly", cd(lambda t: t**3, F(1)) - 3, H*H)
# L06 sign / counts
fp = lambda t: 3*t*t-3
grid = [F(-2)+F(i,4) for i in range(17)]
ff = lambda t: t**3-3*t
inc = sum(1 for lo,hi in zip(grid,grid[1:]) if ff(hi)>ff(lo))
check("L06 increasing intervals 8 of 16", inc, 8)
check("L06 f(-1)=2 f(1)=-2", (ff(F(-1)), ff(F(1))), (2,-2))
check("L06 midpoint sign agrees 16/16", sum(1 for lo,hi in zip(grid,grid[1:]) if (ff(hi)>ff(lo)) == (fp((lo+hi)/2)>0)), 16)
check("L06 M1 f(2)=-3", F(2)**2-4*2+1, -3)
check("L06 M2 c=2/sqrt3", 2/math.sqrt(3), 1.1547, 1e-4)
check("L06 E3 mean value c(x^3 on [0,1])", 1/math.sqrt(3), 0.577, 1e-3)
# Hub numbers
check("hub 6/8=75%", F(6,8), F(3,4))
check("hub 7/8=87.5%", float(F(7,8))*100, 87.5)
check("hub 60/300=20%", F(60,300), F(1,5))
check("hub 24*10=240", 24*10, 240)
check("hub rung3 R3 2 at h=0.1 numeric 3.01", 3+F(1,10)**2, F(301,100))
check("hub skill-check rung2 3+0.1^2", float(3+F(1,100)), 3.01)
check("L04 Q(0.1)=3.31 (quiz)", Q(F(1,10)), F(331,100))
check("L02 q5 0.02990099 within 1e-8 of 302/10100", abs(float(F(302,10100))-0.02990099) < 1e-8, True, True)

bad = [o for o in out if not o[1]]
for name, ok, got, want in out:
    print(("PASS " if ok else "FAIL ") + name + f" got={got} want={want}")
print(f"TOTAL {len(out)} checks, {len(bad)} failing")
