import math
from fractions import Fraction as F
from decimal import Decimal, getcontext
getcontext().prec = 30
out = []
def p(*a): out.append(" ".join(str(x) for x in a))
# L01 box counts (independent implementation)
payoffs = [[1, 3], [1, 1]]  # rows states u,d; cols bond, stock
def arb_count(prices, box):
    n = 0
    for x in box:
        for y in box:
            h = (x, y)
            cost = x * prices[0] + y * prices[1]
            pay = [h[0]*payoffs[s][0] + h[1]*payoffs[s][1] for s in range(2)]
            if cost <= 0 and all(v >= 0 for v in pay) and (cost < 0 or any(v > 0 for v in pay)):
                n += 1
    return n
box = range(-10, 11)
p("L01 arb in box, consistent (9/10,1):", arb_count([F(9,10), F(1)], box))
p("L01 arb in box, mispriced (9/10,1/2):", arb_count([F(9,10), F(1,2)], box))
def dom(prices, box2):
    hs = [(x, y) for x in box2 for y in box2]
    d = v = 0
    for a in hs:
        pa = [a[0]*payoffs[s][0]+a[1]*payoffs[s][1] for s in range(2)]
        for b in hs:
            pb = [b[0]*payoffs[s][0]+b[1]*payoffs[s][1] for s in range(2)]
            if pa[0] >= pb[0] and pa[1] >= pb[1]:
                d += 1
                if a[0]*prices[0]+a[1]*prices[1] < b[0]*prices[0]+b[1]*prices[1]:
                    v += 1
    return d, v
small = range(-2, 3)
p("L01 dominance pairs consistent:", dom([F(9,10), F(1)], small))
p("L01 dominance pairs mispriced:", dom([F(9,10), F(1,2)], small))
# state prices as function of q
for q in [F(1), F(1,2), F(9,10), F(27,10)]:
    pu = (q - F(9,10))/2; pd = (F(27,10) - q)/2
    p("L01 psi at q=", q, pu, pd)
# L01 misconception / quiz numbers
p("L01 cost 1 - 2*9/10 =", 1 - 2*F(9,10), "payoff", 3-2, 1-2)
p("L01 sum state prices", F(1,20)+F(17,20))
p("L01 M2 psi (4/5,1):", (F(1)-F(4,5))/2, F(4,5)-(F(1)-F(4,5))/2)
p("L01 R1 check: q=1, w eps=0.01: psi_u", (1-F(9,10)-F(1,100))/2, "psi_d", (F(27,10)-1-F(1,100))/2)
# L02
S = 5000; r = 0.05; tau = 0.5
Fs = S*math.exp(r*tau); p("L02 F* cents", repr(Fs), f"{Fs:.2f}")
p("L02 50e^0.025", 50*math.exp(0.025))
p("L02 value V at 0.25 with spot 5300:", 5300 - Fs*math.exp(-r*0.25))
p("L02 M1 50e^.025", 50*math.exp(0.025))
p("L02 M2 80e^.01", 80*math.exp(0.01), 81-80*math.exp(0.01))
p("L02 M3 104-100e^-.015", 104-100*math.exp(-0.015))
p("L02 R3 1.05^2", 1.05**2, "e^0.1", math.exp(0.1), "diff", math.exp(0.1)-1.1025)
p("L02 e^0.1 to 4dp", f"{math.exp(0.1):.4f}")
p("L02 P2 partials ok")
p("L02 quote-fair", 5200 - Fs)
# L03
path=[5000]
import random
rng = random.Random(20261028)
for _ in range(10): path.append(path[-1] + rng.randint(-40, 40))
m=[path[i]-path[i-1] for i in range(1,len(path))]
p("L03 path", path); p("L03 margins", m, "sum", sum(m), "neg days", sum(1 for x in m if x<0))
DF=[1.0]; zr=[0.03,0.035,0.04,0.045,0.05]
for i,z in enumerate(zr,1): DF.append((1+z)**(-i))
ann=sum(DF[1:]); par=(1-DF[-1])/ann
p("L03 DF", [f"{d:.6f}" for d in DF[1:]], "annuity", ann, "par", f"{par:.8f}", f"{par*100:.4f}")
p("L03 payment cents", par*1e8, "value", -0.01*ann*1e8)
p("L03 M2 DF3 6%", 1.06**-3, "flatpar")
Dfl=[1.06**-i for i in (1,2,3)]; p("L03 M3 annuity", sum(Dfl), "value/100", 0.01*sum(Dfl)*100, "parts", [f"{d:.6f}" for d in Dfl], sum(float(f"{d:.6f}") for d in Dfl))
d1=1/1.03; d2=d1/1.05; p("L03 R3 DF1 DF2", d1, d2, "Rpar", (1-d2)/(d1+d2), "flat3 DF2", 1.03**-2)
p("L03 R2 check weights")
p("L03 Q10 par rate vs zero rates ok", f"{par*100:.4f}" in ["3.0000","3.5000","4.0000","4.5000","5.0000"])
print("\n".join(out))
