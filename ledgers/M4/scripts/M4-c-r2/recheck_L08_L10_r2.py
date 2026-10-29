import math, random, cmath
# Prop 1.3 derivative check for F_V and density
def FV(x): return 0.5 + (math.atan(x/math.sqrt(3)) + (x/math.sqrt(3))/(1+x*x/3))/math.pi
def fV(t): return 2/(math.pi*math.sqrt(3))*(1+t*t/3)**-2
worst=0
for x in [-5,-1.3,-0.2,0.0,0.7,2.0,9.0]:
    h=1e-6
    d=(FV(x+h)-FV(x-h))/(2*h)
    worst=max(worst,abs(d-fV(x)))
print("max |dF_V/dx - f_V| over grid:", f"{worst:.2e}")
# Prop 1.4 closed forms vs numeric integral of density
def tailV(x): return 2/math.pi*(math.atan(math.sqrt(3)/x) - x*math.sqrt(3)/(3+x*x))
for x in [0.5,1.0,3.0,10.0]:
    num=2*(1-FV(x))
    print("P(|V|>%g): closed %.10f  1-2FV form %.10f" % (x, tailV(x), num))
# Prop 1.5(b) lower bound sqrt3/(pi x^3) for x >= sqrt3
for x in [math.sqrt(3), 4.0, 10.0, 100.0]:
    print("x=%.3f  P(|V|>x)=%.6e  bound sqrt3/(pi x^3)=%.6e  holds=%s" % (x, tailV(x), math.sqrt(3)/(math.pi*x**3), tailV(x) >= math.sqrt(3)/(math.pi*x**3)))
# Prop 1.5(a) bound (2/pi)(1/x - 1/(3x^3)) >= 1/(pi x) for x>=1 (checks) and arctan u >= u - u^3/3
ok=all(math.atan(u) >= u-u**3/3 for u in [i/1000 for i in range(0,5000)])
print("arctan u >= u - u^3/3 on [0,5):", ok)
for x in [1.0,2.0,10.0]:
    print("C tail x=%g: %.6f >= 1/(pi x)=%.6f : %s" % (x, 2/math.pi*math.atan(1/x), 1/(math.pi*x), 2/math.pi*math.atan(1/x) >= 1/(math.pi*x)))
# Prop 1.5(c) Gaussian bound
print("normal bound ok:", all(math.erfc(x/math.sqrt(2)) <= 2*math.exp(-x*x/2) for x in [0.5,1,2,5,10]))
# Prop 2.2 bound: |phi_Y(s) - (1 - s^2/2)| <= |s|^3 E|Y|^3/3 for |s|<=1/M, finite laws
rng=random.Random(1)
worst_ratio=0.0
for trial in range(2000):
    k=rng.randint(2,6)
    vals=[rng.uniform(-3,3) for _ in range(k)]
    p=[rng.random() for _ in range(k)]; S=sum(p); p=[q/S for q in p]
    m=sum(a*b for a,b in zip(p,vals)); v=sum(b*b*a for a,b in zip(p,vals))-m*m
    if v<=1e-6: continue
    vals=[(y-m)/math.sqrt(v) for y in vals]
    M=max(abs(y) for y in vals)
    E3=sum(a*abs(y)**3 for a,y in zip(p,vals))
    for s in [i/50/M for i in range(-50,51)]:
        phi=sum(a*cmath.exp(1j*s*y) for a,y in zip(p,vals))
        lhs=abs(phi-(1-s*s/2)); rhs=abs(s)**3*E3/3
        if rhs>0: worst_ratio=max(worst_ratio,lhs/rhs)
print("Prop 2.2 worst lhs/rhs ratio (must be <=1):", round(worst_ratio,6))
# Prop 2.2 pointwise bound |e^{ix}-1-ix+x^2/2| <= |x|^3/3 for |x|<=1
print("pointwise ok:", all(abs(cmath.exp(1j*x)-1-1j*x+x*x/2) <= abs(x)**3/3+1e-15 for x in [i/1000 for i in range(-1000,1001)]))
# Cauchy derivative of arctan check of Prop1.3 for C
print("Cauchy F_C tail equals (2/pi)arctan(1/x) at x=3:", abs(2*(1-(0.5+math.atan(3)/math.pi))-2/math.pi*math.atan(1/3))<1e-15)
# L09 numbers: exact die sums and gaps rechecked independently
from fractions import Fraction
def mass(n):
    m=[Fraction(1)]
    for _ in range(n):
        new=[Fraction(0)]*(len(m)+6)
        for t,p in enumerate(m):
            for f in range(1,7): new[t+f]+=p/6
        m=new
    return m
phi1=0.5*(1+math.erf(1/math.sqrt(2)))
for n in [1,5,10,20,40]:
    m=mass(n); thr=math.floor(3.5*n+math.sqrt(35*n/12))
    c=float(sum(m[:thr+1]))
    print("n=%d thr=%d P=%.6f gap=%+.6f" % (n,thr,c,c-phi1))
# Chebyshev values
print("cheb n=10 bound", (35/12)/(10*0.25), " n=100", (35/12)/(100*0.25), " n=10000", (35/12)/(10000*0.25))
