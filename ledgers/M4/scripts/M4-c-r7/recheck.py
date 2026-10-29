import math, random, statistics
from fractions import Fraction
from statistics import NormalDist
print("== L08 ==")
A=[[2,0],[1,1]]; Q=[[0,-1],[1,0]]
def mm(X,Y): return [[sum(X[i][k]*Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))] for i in range(len(X))]
def T(X): return [list(r) for r in zip(*X)]
AAt=mm(A,T(A)); AtA=mm(T(A),A); B=mm(A,Q); BBt=mm(B,T(B))
print("AAt",AAt,"AtA",AtA,"B",B,"BBt==AAt",BBt==AAt,"AtA-AAt",[[AtA[i][j]-AAt[i][j] for j in range(2)] for i in range(2)])
# Example 1.5 A = LL^T lower-tri uniqueness check: a=2,b=1,c=1
# E1 gaps and E2/E3 from printed matrices
Xs=[[4.0073,2.0187],[2.0187,1.9936]]; Ys=[[3.9070,1.9385],[1.9385,1.9636]]
g=lambda M,E: max(abs(M[i][j]-E[i][j]) for i in range(2) for j in range(2))
print("X gap from Sigma",round(g(Xs,AAt),4),"X gap from AtA",round(g(Xs,AtA),4),"Y gap from Sigma",round(g(Ys,AAt),4))
print("entry gaps X", [round(abs(Xs[0][0]-4),4), round(abs(Xs[0][1]-2),4), round(abs(Xs[1][1]-2),4)])
se=math.sqrt(0.8552*0.1448/4000); print("SE",round(se,6), "gap/se printed", round(0.0139/0.0056,2), "unrounded", round(0.013855/0.005564,2))
print("mean-X gap", round(1-0.9770,4), round(-2.0055+2,4))
# L08 run-level recheck with independent generator
rng=random.Random(2026); rows=[]
N=20000
import itertools
sa=[0.0,0.0]; 
for _ in range(N):
    z=[rng.gauss(0,1), rng.gauss(0,1)]
    x=[1+2*z[0], -2+z[0]+z[1]]
    rows.append(x)
m=[sum(r[i] for r in rows)/N for i in range(2)]
print("recheck X mean",[round(v,4) for v in m])
print("== L09 ==")
mass=[Fraction(1)]
phi1=NormalDist().cdf(1.0); print("Phi1",round(phi1,6))
for n in (1,5,10,20,40):
    mass=[Fraction(1)]
    for _ in range(n):
        new=[Fraction(0)]*(len(mass)+6)
        for t,p in enumerate(mass):
            for f in range(1,7): new[t+f]+=p/6
        mass=new
    thr=math.floor(3.5*n+math.sqrt(35*n/12))
    p=sum(mass[:thr+1],Fraction(0))
    print(n,thr,float(p),round(float(p)-phi1,6), "real thr", 3.5*n+math.sqrt(35*n/12))
sig2=35/12
for n in (100,10,1000,10000): print("cheb",n,round(sig2/(n*0.25),6))
print("E1 40.4006", 35+math.sqrt(29.1667))
print("E3", (35/12)/(10000*0.25))
r=random.Random(2026); path=[r.randint(1,6) for _ in range(10000)]
for n in (10,100,1000,10000): print("run mean",n,round(sum(path[:n])/n,4))
print("M2 35/48",35/48, "M1", (35/12)/25)
print("E-prob pair", Fraction(1,2))
print("== L10 ==")
def tail_C(x): return 2/math.pi*math.atan(1/x)
def tail_V_closed(x):
    y=math.sqrt(3)/x
    return 2/math.pi*(math.atan(y)-y/(1+y*y))
dens=lambda t: 2/(math.pi*math.sqrt(3))*(1+t*t/3)**-2
# numeric tail of V over (10,inf) using substitution t=1/u
def num_tail(x,N=400000):
    # integral_x^inf f(t) dt with t = x/u, u in (0,1]
    h=1.0/N; s=0.0
    for k in range(N):
        u=(k+0.5)*h
        t=x/u
        s+= dens(t)*x/(u*u)*h
    return 2*s
print("P|C|>10",tail_C(10),"x P",10*tail_C(10),"1000P",1000*tail_C(1000),"100P",100*tail_C(100))
print("P|V|>10 closed",tail_V_closed(10),"numeric",num_tail(10))
print("x^3 P|V|>x", [round(x**3*tail_V_closed(x),6) for x in (10,100,1000)])
print("limits 2/pi",2/math.pi,"4sqrt3/pi",4*math.sqrt(3)/math.pi)
print("normal tail 10",math.erfc(10/math.sqrt(2)), "ratio", tail_C(10)/math.erfc(10/math.sqrt(2)))
print("P|Z|>10 bound 2e^-50",2*math.exp(-50))
# integral of t3 density over [-2,2]
N2=200000; h=4.0/N2
print("midpoint",sum(dens(-2+(k+0.5)*h) for k in range(N2))*h)
F=lambda x: 0.5+(math.atan(x/math.sqrt(3))+(x/math.sqrt(3))/(1+x*x/3))/math.pi
print("F2-F-2",F(2)-F(-2))
print("atan(0.1)",math.atan(0.1))
print("F_V(sqrt3)",F(math.sqrt(3)), 0.75+1/(2*math.pi))
print("Var check t3",3/(3-2))
print("4*sqrt3/pi",4*math.sqrt(3)/math.pi)
print("E|V|^... fine")
# Lab Part C recheck: IQR of Cauchy and normal, same seeds
def draw_cauchy(rng): return math.tan(math.pi*(rng.random()-0.5))
def draw_normal(rng): return rng.gauss(0,1)
def draw_t3(rng):
    z=rng.gauss(0,1); w=sum(rng.gauss(0,1)**2 for _ in range(3)); return z/math.sqrt(w/3)
for name,d,seed,sig in (("normal",draw_normal,2026,1.0),("t3",draw_t3,2027,math.sqrt(3)),("cauchy",draw_cauchy,2028,None)):
    for n in (10,100):
        rng=random.Random(seed+100*n)
        means=[sum(d(rng) for _ in range(n))/n for _ in range(400)]
        q1,_,q3=statistics.quantiles(means,n=4,method="inclusive")
        extra=""
        if sig: extra=round(statistics.variance([math.sqrt(n)*m/sig for m in means]),4)
        print("C",name,n,round(q3-q1,4),extra)
