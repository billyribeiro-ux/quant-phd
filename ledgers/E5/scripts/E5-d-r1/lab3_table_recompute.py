# Independent check of every row of the Lab 3 table (scratch; numpy polyfit trend, not the lab's formula)
import random, math
import numpy as np
rng = random.Random(2026)
gdp=[20000.0]
for _ in range(23): gdp.append(gdp[-1]*(1+0.004+0.012*(rng.random()-0.5)))
price=[100.0]
for _ in range(23): price.append(price[-1]*(1+0.005+0.004*(rng.random()-0.5)))
un=[4.2]
for _ in range(23): un.append(min(7.0,max(3.5,un[-1]+0.4*(rng.random()-0.5))))
pol=[1.0]
for _ in range(23): pol.append(max(0.0,pol[-1]+0.5*(rng.random()-0.5)))
def lab(q):
    lbl={0:'2020 Q4'}
    m=9+3*q; return f"{2020+m//12} Q{(m%12)//3+1}"
for t in range(20,24):
    g=100*((gdp[t]/gdp[t-1])**4-1)
    pi=100*(price[t]/price[t-4]-1)
    sl,ic=np.polyfit(np.arange(20), np.log(np.array(gdp[t-19:t+1])),1)
    gap=100*(math.log(gdp[t])-(ic+sl*19))
    tay=2+pi+0.5*(pi-2)+0.5*gap
    print(lab(t), *[f"{x:.2f}" for x in (g,pi,gap,un[t],pol[t],tay,pol[t]-tay)])
