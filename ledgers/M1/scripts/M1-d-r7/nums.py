import math
from fractions import Fraction
# L04 Part B errors
r=0.05
ce=math.exp(r)
def err(m): return ce-(1+r/m)**m
e1000,e10k,e100k=err(1000),err(10000),err(100000)
print("err", e1000,e10k,e100k)
print("ratio 1k->10k", e1000/e10k, "10k->100k", e10k/e100k)
# Part C
P=1_000_000
def fv(m): return P*(1+0.05/m)**(10*m)
ann,mon,dai,con=fv(1),fv(12),fv(365),P*math.exp(0.5)
print("L04 C unrounded", ann,mon,dai,con)
print("mon-ann", mon-ann, "con-dai", con-dai)
print("mon-dai", dai-mon, "dai-con", con-dai, "ratio", (dai-mon)/(con-dai))
print("mon-ann pr", round(mon)-round(ann), "con-dai pr", round(con)-round(dai), "ratio printed", (round(dai)-round(mon))/(round(con)-round(dai)))
# L05 t=5
for name,v in [("semi",(1.025)**(-10)*1e6),("cont",math.exp(-0.25)*1e6)]: print(name, v)
print("gap semi-cont", (1.025**-10 - math.exp(-0.25))*1e6)
print("L05 semi-cont printed", 781198-778801, "unrounded", ((1.025**-10 - math.exp(-0.25))*1e6))
a=1.05**-0.5; s=1.025**-1; print("t0.5 annual", a, "semi", (1.025)**(-1), "diff", a - (1.025)**-1)
print("diff unrounded to 10", f"{(1.05**-0.5)-(1.025**-1):.12f}")
print("eff", 1.00375**12)
print("monthly rate compounding to 4.5", 1.045**(1/12)-1)
# project loan
L=30_000_000; i=0.045/12; n=300
pay=L*i/(1-(1+i)**-n); print("level unrounded", pay)
bound=n*(1+i)**n+1; print("bound", bound)
r_=0.05
N=next(k for k in range(1,10000) if (1/(1+r_))**k/r_ < 1e-6); print("N", N, "err N-1", (1/(1+r_))**(N-1)/r_, "err N", (1/(1+r_))**N/r_)
