# Independent recomputation for FC2 slice c (L07, L08). Standard library only.
import math
from decimal import Decimal, ROUND_HALF_UP

def Phi(x): return 0.5*(1+math.erf(x/math.sqrt(2)))
def phi(x): return math.exp(-x*x/2)/math.sqrt(2*math.pi)
def bs(S,K,r,t,s):
    d1=(math.log(S/K)+(r+s*s/2)*t)/(s*math.sqrt(t)); d2=d1-s*math.sqrt(t)
    return S*Phi(d1)-K*math.exp(-r*t)*Phi(d2), d1, d2
def bsput(S,K,r,t,s):
    _,d1,d2=bs(S,K,r,t,s); return K*math.exp(-r*t)*Phi(-d2)-S*Phi(-d1)
def tree(S,K,r,t,s,n):
    h=t/n; u=math.exp(s*math.sqrt(h)); d=1/u; R=math.exp(r*h); q=(R-d)/(u-d)
    vals=[max(S*u**j*d**(n-j)-K,0.0) for j in range(n+1)]
    for _ in range(n): vals=[(q*vals[j+1]+(1-q)*vals[j])/R for j in range(len(vals)-1)]
    return vals[0], q, u, d, R
def half_up(x, places=0):
    return float(Decimal(repr(x)).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))

C,d1,d2=bs(100,100,0.05,1,0.2)
print("C unrounded", repr(C), "d1", d1, "d2", d2)
print("put M2:", C-100+100*math.exp(-0.05), "cents", (C-100+100*math.exp(-0.05))*100)
print("Ke^-rt", 100*math.exp(-0.05))
for n in (1,2,5,10,25,50,100,200,400):
    v,q,u,d,R=tree(100,100,0.05,1,0.2,n)
    e=v-C
    print(n, "tree", v, "err", e, "err_cents", e*100, "h<s2/r2", (1/n)<0.04/0.0025)
v4=tree(100,100,0.05,1,0.2,4)
print("M3 n=4 u,d,R,q", v4[2], v4[3], v4[4], v4[1], "sig*sqrt h", 0.2*math.sqrt(0.25))
v1=tree(100,100,0.05,1,0.2,1)
print("E3 V1", v1[0], "q1", v1[1], "u1", v1[2], "d1", v1[3], "R1", v1[4])
print("E3 manual", math.exp(-0.05)*0.577493*22.1403)
# Lemma 1.2 / 1.4 numeric
print("Phi(x)+Phi(-x)", max(abs(Phi(x)+Phi(-x)-1) for x in (0,0.35,1.7,3)))
# R2 alt inputs
print("R2 tau4 sig0.1 r0.0125", bs(100,100,0.0125,4,0.1)[0], "sig sqrt tau", 0.1*2, "r tau", 0.0125*4)
# Misconception: different S with same r tau and sig sqrt tau
print("counterexample S=100 vs S=110 same r tau, sig sqrt tau:", bs(100,100,0.05,1,0.2)[0], bs(110,100,0.05,1,0.2)[0])
# R2 vega and L08 R2 quote
vega=100*phi(0.35)*1.0
print("vega ATM", vega, "dsigma", 0.01/vega, "vol pts", 0.01/vega*100)
print("quiz vega to 2dp", round(vega,2))
# L08 values
print("L08 L", 100-100*math.exp(-0.05), "unrounded 4.877058?", 100-100*math.exp(-0.05))
print("K=120 L", max(100-120*math.exp(-0.05),0), "120e^-0.05", 120*math.exp(-0.05))
print("E2 price K=120 sig0.1", bs(100,120,0.05,1,0.10)[0]*100)
print("E3 price 0.5 at K=120 implied vol: bisection")
def implied(S,K,r,t,price,lo=1e-6,hi=10.0,tol=1e-10):
    low,high=lo,hi; k=0
    while high-low>tol:
        m=(low+high)/2
        if bs(S,K,r,t,m)[0]<price: low=m
        else: high=m
        k+=1
    return (low+high)/2,k
print("E3 vol", implied(100,120,0.05,1,0.5))
print("C(1e-6)", bs(100,120,0.05,1,1e-6)[0], "C(10)", bs(100,120,0.05,1,10)[0])
