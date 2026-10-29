import random, math
from fractions import Fraction as Fr
SEED=20261028; N=20000; n=5; a=2000
def run(shade):
    rng=random.Random(SEED); tot=0; profits=[]
    for _ in range(N):
        v=rng.randint(5000,15000)
        sig=[v+rng.randint(-a,a) for _ in range(n)]
        bids=[s-shade for s in sig]
        best=0
        for i in range(1,n):
            if bids[i]>bids[best]: best=i   # strict > keeps lower index on ties
        p=v-bids[best]; profits.append(p); tot+=p
    m=sum(profits); sumsq=sum(p*p for p in profits)
    var=(N*sumsq-m*m)/(N*(N-1))  # sample variance of profits
    se_total=math.sqrt(N*var)
    return tot, se_total
EM=Fr(85418692002000,64048012001)
naive,se=run(0)
shaded,se2=run(1334)
print('naive total',naive,'se',round(se_total:=se,2))
print('shaded total',shaded,'se',round(se2,2))
print('naive diff from exact (-20000*EM):', naive-float(-20000*EM), 'in SE units', (naive-float(-20000*EM))/se)
print('shaded diff from exact (20000*(1334-EM)):', shaded-float(20000*(1334-EM)), 'SE units', (shaded-float(20000*(1334-EM)))/se2)
print('shaded-naive', shaded-naive, 20000*1334)
