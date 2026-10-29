import cmath, math, random
random.seed(1)
worst=0
for _ in range(2000):
    p=random.uniform(0.01,0.99); a=random.uniform(-5,5); b=random.uniform(-5,5); t=random.uniform(-10,10)
    phi=p*cmath.exp(1j*t*a)+(1-p)*cmath.exp(1j*t*b)
    lhs=abs(phi)**2; rhs=p*p+(1-p)**2+2*p*(1-p)*math.cos(t*(a-b))
    worst=max(worst,abs(lhs-rhs))
print("Prop2.5 worst", worst)
# Prop 2.4 numeric check on two-point law
p=0.3;a=1.0;b=-2.0;c=2.0;d=0.5;t=0.7
phi=lambda s: p*cmath.exp(1j*s*a)+(1-p)*cmath.exp(1j*s*b)
lhs=p*cmath.exp(1j*t*(c*a+d))+(1-p)*cmath.exp(1j*t*(c*b+d))
print("Prop2.4 check", abs(lhs-cmath.exp(1j*t*d)*phi(c*t)))
# E[1/W] nu=3 integral
N=400000; L=2000.0; h=L/N
I=sum((1+2*(k+0.5)*h)**-1.5 for k in range(N))*h
print("nu=3 integral of (1+2s)^(-3/2) ~", I, "expected 1/(nu-2)=1")
# E|T| style: E[1/W] for nu=3 by Monte Carlo
rng=random.Random(7); s=0.0; n=200000
for _ in range(n):
    w=sum(rng.gauss(0,1)**2 for _ in range(3)); s+=1/w
print("MC E[1/W3]", s/n)
