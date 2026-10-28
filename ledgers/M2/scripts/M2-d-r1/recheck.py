# Independent recomputation of slice numbers (verifier's own code, not the twins).
import math
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 50

# L19: f = e^x y + x y^2 at (0.5,0.25), d=(0.6,-0.8)
a, b = 0.5, 0.25
e = math.exp(a)
fx = e*b + b*b; fy = e + 2*a*b
fxx = e*b; fxy = e + 2*b; fyy = 2*a
print("L19 grad", round(fx,6), round(fy,6), "hess", round(fxx,6), round(fxy,6), round(fyy,6))
d1, d2 = 0.6, -0.8
gp = fx*d1 + fy*d2
gpp = d1*(fxx*d1+fxy*d2) + d2*(fxy*d1+fyy*d2)
# g(s) = f(p+sd) exact third derivative via polynomial/exp decomposition
c, dd = b, -0.8  # y(s)=b+dd s ; x(s)=a+d1 s
e_a = math.exp(a)
g3 = e_a*(d1**3*c + 3*d1**2*dd) + 6*(d1*(dd**2) * 0 + 0)  # placeholder, recomputed below
# direct: term2 = (a+d1 s)(b+dd s)^2 cubic coefficient = d1*dd^2 ; third derivative = 6*d1*dd^2
g3 = e_a*(d1**3*c + 3*d1**2*dd) + 6*d1*dd*dd
print("L19 g'(0)", round(gp,6), "g''(0)", round(gpp,6), "g'''(0)", round(g3,6))
def f(x,y): return math.exp(x)*y + x*y*y
for s in (0.1,0.05,0.025,0.0125):
    E1 = f(a+s*d1,b+s*d2)-f(a,b)-s*gp
    E2 = E1 - 0.5*s*s*gpp
    print("L19 s",s,"E1",f"{E1:.6e}","E2",f"{E2:.6e}")
# ratios with printed rounding:
E1s=[f(a+s*d1,b+s*d2)-f(a,b)-s*gp for s in (0.1,0.05,0.025,0.0125)]
E2s=[E-0.5*s*s*gpp for E,s in zip(E1s,(0.1,0.05,0.025,0.0125))]
print("L19 ratios1", [round(E1s[i-1]/E1s[i],4) for i in range(1,4)], "ratios2", [round(E2s[i-1]/E2s[i],4) for i in range(1,4)])

# L20: exact sums
def mids(lo,hi,n):
    w=(hi-lo)/n; return [lo+(i+Fraction(1,2))*w for i in range(n)]
for n in (1,2,4,8,16,32):
    dx=Fraction(1,n); dy=Fraction(2,n)
    S=sum((x*y+x*x)*dx*dy for x in mids(Fraction(0),Fraction(1),n) for y in mids(Fraction(0),Fraction(2),n))
    print("L20 n",n,S, S-Fraction(5,3), Fraction(-1,6*n*n)==S-Fraction(5,3))

# L21: root and formula
def root(x):
    y=1.0
    for _ in range(200):
        y -= (y**3+x*y-1)/(3*y*y+x)
    return y
for x in (0.25,0.5,1.0,2.0):
    y=root(x); h=1e-5
    fd=(root(x+h)-root(x-h))/(2*h)
    form=-y/(3*y*y+x)
    print("L21 x",x,f"y {y:.10f} formula {form:.10f} cd {fd:.10f} diff {abs(form-fd):.1e} Fy {3*y*y+x:.6f}")

# L22: Part A/B values
for A in (1.5,2,3,4):
    xs=A-1
    V=lambda aa: aa*math.log(aa)-(aa-1)
    print("L22 A a",A,"V' cd",(V(A+1e-4)-V(A-1e-4))/2e-4, "ln", math.log(A))
for A in (1.0,2.0,3.0):
    V=lambda aa: aa*aa/4
    print("L22 B a",A,"V' exact",A/2, "x* a/2",A/2)

# L23: bond
cf={t:5000+(100000 if t==10 else 0) for t in range(1,11)}
def P(y): return sum(cf[t]/(1+y)**t for t in cf)
def P1(y): return -sum(t*cf[t]/(1+y)**(t+1) for t in cf)
def P2(y): return sum(t*(t+1)*cf[t]/(1+y)**(t+2) for t in cf)
def P3(y): return -sum(t*(t+1)*(t+2)*cf[t]/(1+y)**(t+3) for t in cf)
y0=0.04
print("L23 P(y0)", f"{P(y0):.6f}", "round", round(P(y0)), "P1", f"{P1(y0):.6f}", "P2", f"{P2(y0):.6f}")
print("L23 P(0.05)", f"{P(0.05):.9f}", round(P(0.05)))
print("L23 -P1/P", f"{-P1(y0)/P(y0):.6f}", "P2/P", f"{P2(y0)/P(y0):.6f}")
T1=lambda dy: P(y0)+P1(y0)*dy
T2=lambda dy: T1(dy)+0.5*P2(y0)*dy*dy
E1s=[];E2s=[]
for dy in (0.01,0.005,0.0025):
    E1s.append(P(y0+dy)-T1(dy)); E2s.append(P(y0+dy)-T2(dy))
    print("L23 dy",dy,f"e1 {E1s[-1]:.6e} e2 {E2s[-1]:.6e}")
print("L23 ratios", [round(E1s[i-1]/E1s[i],4) for i in (1,2)], [round(E2s[i-1]/E2s[i],4) for i in (1,2)])
for dy in (0.01,-0.01):
    print("L23 shift",dy, f"exact {P(y0+dy):.4f} round {round(P(y0+dy))}, T2 {T2(dy):.4f} round {round(T2(dy))}, diff {round(P(y0+dy))-round(T2(dy))}")
print("L23 P3 sign", P3(y0)<0, "P1<0", P1(y0)<0, "P2>0", P2(y0)>0)

# L24: quotients
for k in range(1,16):
    h=10.0**-k
    ef=abs((math.exp(1+h)-math.exp(1))/h-math.e)
    ec=abs((math.exp(1+h)-math.exp(1-h))/(2*h)-math.e)
    print("L24 k",k,f"fwd {ef:.3e} cen {ec:.3e}")
print("L24 lemma numbers: 2sqrt(delta/e)=", 2*math.sqrt(2.22e-16/math.e), " (3delta/e)^(1/3)=", (3*2.22e-16/math.e)**(1/3))
print("L24 half-ulp e:", 2**-52*2/2, math.ulp(math.e)/2)
