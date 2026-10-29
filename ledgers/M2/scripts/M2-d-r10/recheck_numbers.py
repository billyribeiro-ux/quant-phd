from fractions import Fraction
import math
N=10; F=100000; C=5000
cf={t:(C+(F if t==N else 0)) for t in range(1,N+1)}
def P(y):
    v=1+Fraction(y); return sum(Fraction(cf[t])/v**t for t in range(1,N+1))
def P1(y):
    v=1+Fraction(y); return -sum(Fraction(t*cf[t])/v**(t+1) for t in range(1,N+1))
def P2(y):
    v=1+Fraction(y); return sum(Fraction(t*(t+1)*cf[t])/v**(t+2) for t in range(1,N+1))
y0=0.04
print("P(y0)", float(P(y0)), "round", round(P(y0)))
print("P'(y0)", float(P1(y0)), "P''(y0)", float(P2(y0)))
print("P(0.05)", float(P(0.05)), round(P(0.05)), "P(0.03)", float(P(0.03)), round(P(0.03)))
print("-P'/P", float(-P1(y0)/P(y0)), "P''/P", float(P2(y0)/P(y0)))
def tf(dy): return P(y0)+P1(y0)*Fraction(dy)
def ts(dy): return tf(dy)+Fraction(1,2)*P2(y0)*Fraction(dy)**2
for dy in (0.01,0.005,0.0025):
    e1=P(y0+dy)-tf(dy); e2=P(y0+dy)-ts(dy)
    print("dy",dy,float(e1),float(e2))
for dy in (0.01,-0.01):
    ex=round(P(y0+dy)); ap=round(ts(dy)); print("shift",dy,ex,ap,ex-ap, float(P(y0+dy)), float(ts(dy)))
# R3 quiz: two cash flows c1=-1, c2=1000, N=2 at y=0.04
v=1/1.04
print("quiz P' two cf", -(1*(-1)*v**2 + 2*1000*v**3))
# L24 unrounded central errors
def central(f,x,h): return (f(x+h)-f(x-h))/(2*h)
for h in (1e-5,1e-7):
    c=central(math.exp,1.0,h)
    print("central err", h, abs(c-math.e), "fwd", abs((math.exp(1.0+h)-math.exp(1.0))/h-math.e))
for k in range(1,16):
    h=10.0**-k
    print(k, "%.3e"%abs((math.exp(1+h)-math.exp(1))/h-math.e), "%.3e"%abs(central(math.exp,1.0,h)-math.e))
print("e ulp", math.ulp(math.e), "half", math.ulp(math.e)/2)
print("pred M2 min", 2*math.sqrt(2.22e-16/math.e), "M3 min", (3*2.22e-16/math.e)**(1/3))
