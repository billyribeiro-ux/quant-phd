"""Independent recomputation of project.html numbers (round 2). Uses Fraction-free float and exact spreads."""
import math, random, sys
from fractions import Fraction
from pathlib import Path
import numpy as np

SEED, Q, W = 2026, 24, 20

def path(seed=SEED):
    rng = random.Random(seed)
    gdp=[20000.0]
    for _ in range(Q-1): gdp.append(gdp[-1]*(1+0.004+0.012*(rng.random()-0.5)))
    price=[100.0]
    for _ in range(Q-1): price.append(price[-1]*(1+0.005+0.004*(rng.random()-0.5)))
    un=[4.2]
    for _ in range(Q-1): un.append(min(7.0,max(3.5,un[-1]+0.4*(rng.random()-0.5))))
    pol=[1.0]
    for _ in range(Q-1): pol.append(max(0.0,pol[-1]+0.5*(rng.random()-0.5)))
    return gdp,price,un,pol

gdp,price,un,pol = path()
def lab(k):
    m=9+3*k; return f"{2020+m//12} Q{(m%12)//3+1}"
def trend(t):
    x=np.arange(W,dtype=float); y=np.array([math.log(gdp[t-W+1+k]) for k in range(W)])
    b,a=np.polyfit(x,y,1)  # slope, intercept
    return a,b
def loggap(t):
    a,b=trend(t); return 100*(math.log(gdp[t])-(a+b*(W-1)))
def pctgap(t):
    a,b=trend(t); tr=math.exp(a+b*(W-1)); return 100*(gdp[t]-tr)/tr
def growth(t): return 100*((gdp[t]/gdp[t-1])**4-1)
def infl(t): return 100*(price[t]/price[t-4]-1)
def taylor(t): return 2.0+infl(t)+0.5*(infl(t)-2.0)+0.5*loggap(t)

# spreads from the snapshot
spreads={}
with open(sys.argv[1]) as f:
    hdr=next(f).strip().split(",")
    rows=[l.strip().split(",") for l in f]
print("header",hdr,"rows",len(rows),"first",rows[0][0],"last",rows[-1][0])
blank=[r for r in rows if len(r)!=3 or r[1]=="" or r[2]==""]
print("rows with blank or malformed yields:",len(blank), "sample", blank[:3])
tot={};cnt={}
for d,tb,cm in rows:
    if tb=="" or cm=="": continue
    lbl=f"{int(d[:4])} Q{(int(d[5:7])-1)//3+1}"
    tot[lbl]=tot.get(lbl,Fraction(0))+(Fraction(cm)-Fraction(tb)); cnt[lbl]=cnt.get(lbl,0)+1
sp={k:(tot[k]/cnt[k], cnt[k]) for k in tot}

for t in range(Q-4,Q):
    print(lab(t), f"g={growth(t):.5f} pi={infl(t):.5f} ylog={loggap(t):.5f} ypct={pctgap(t):.5f} taylor={taylor(t):.5f} pgap={pol[t]-taylor(t):.5f} spread={float(sp[lab(t)][0]):.5f} days={sp[lab(t)][1]} policy={pol[t]:.5f} un={un[t]:.5f}")
t=Q-1
print("2026Q3 unrounded: growth",growth(t),"infl",infl(t),"ylog",loggap(t),"ypct",pctgap(t),"taylor",taylor(t),"pgap",pol[t]-taylor(t),"spread",float(sp['2026 Q3'][0]))
# ratio of log gap to percent gap sign check over window
print("sign agreement over window:", all((loggap(k)>0)==(pctgap(k)>0) for k in range(W-1,Q)))
# exemplar A: sensitivity to output coefficient 0.5->1.0
ta=taylor(t); print("coef change effect", ta-(ta+0.5*loggap(t)), "pgap new", pol[t]-(ta+0.5*loggap(t)))
# inflation rounding corners
for pi_ in (1.895,1.905):
    for g_ in (-0.185,-0.175):
        print("corner", pi_, g_, 2+pi_+0.5*(pi_-2)+0.5*g_)
print("2dp of 2026Q3 spread", round(float(sp['2026 Q3'][0]),6))
