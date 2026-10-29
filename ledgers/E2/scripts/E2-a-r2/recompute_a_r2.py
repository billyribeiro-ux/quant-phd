"""Independent recomputation for E2 slice a, round 2 (does not import the lab twins)."""
from fractions import Fraction as F
import itertools

# L01 Cournot grid, independent of lab code: profit in cents
def prof(q, r):
    price = max(0, 100 - q - r)
    return q * (price - 10)
grid = range(91)
tie = [(a, b) for a in grid for b in grid
       if all(prof(k, b) <= prof(a, b) for k in grid) and all(prof(k, a) <= prof(b, a) for k in grid)]
strict = [(a, b) for a in grid for b in grid
          if all(prof(k, b) < prof(a, b) for k in grid if k != a) and all(prof(k, a) < prof(b, a) for k in grid if k != b)]
print("L01 tie-allowed", tie)
print("L01 strict", strict)
print("L01 profits", [(prof(a,b), prof(b,a)) for a,b in tie])
print("L01 example 4.1 check q1=1/2,q2=30:", F(1,2)*(max(0, 100-F(1,2)-30)-10), "=119/4 ?", F(1,2)*(max(0, 100-F(1,2)-30)-10)==F(119,4))
print("L01 3x4 comparisons alt-only:", 12*(2+3), " incl-played:", 12*(3+4))
# L01 M1 game
u1={('A','A'):2,('A','B'):0,('B','A'):0,('B','B'):1}
u2={('A','A'):1,('A','B'):0,('B','A'):0,('B','B'):2}
eq=[]
for a in 'AB':
    for b in 'AB':
        if all(u1[(a,b)]>=u1[(x,b)] for x in 'AB') and all(u2[(a,b)]>=u2[(a,x)] for x in 'AB'):
            eq.append((a,b))
print("L01 M1 eq", eq)

# L02: n-bidder first-price symmetric equilibrium, independent recompute
def W(b, beta, n):
    return F(1) if b >= beta else (b/beta)**(n-1)
for n in range(2,6):
    beta = F(n-1,n)
    ok=0
    for k in range(21):
        v=F(k,20)
        cf=(v-beta*v)*W(beta*v,beta,n)
        best=max((v-F(j,1200))*W(F(j,1200),beta,n) for j in range(1201))
        ok += cf>=best
    # revenue and second-highest mean via numeric midpoint integration in floats
    N=200000
    rev=sum(beta*((i+0.5)/N)*n*((i+0.5)/N)**(n-1) for i in range(N))/N
    sec=sum(((i+0.5)/N)*n*(n-1)*((i+0.5)/N)**(n-2)*(1-(i+0.5)/N) for i in range(N))/N
    print("L02 n",n,"closed-form best on grid",ok,"of 21; rev float",round(rev,6),"(n-1)/(n+1)",round((n-1)/(n+1),6),"second mean float",round(sec,6))
# M3 five bidders
print("L02 M3", F(4,5)*F(1,2), (F(2,5)/F(4,5))**4)
print("L02 R-check 0.8^2/2", F(4,5)**2/2)
# L02 Remark 2.4 symbolic: v^n/n at n=2,v=0.8
print("L02 n=3 v=0.6 payoff", (F(3,5)-F(2,5))*F(36,100), F(6,10)**3/3)

# L03 consistent prices, independent recompute with floats avoided
VH,VL,CH,CL=12000,6000,10000,4000
def consistent(alpha):
    res=[]
    for p in range(0,15001):
        mH = alpha if CH<=p else F(0)
        mL = (1-alpha) if CL<=p else F(0)
        M=mH+mL
        if M>0 and F(mH*VH+mL*VL)/M == p:
            res.append((p, M))
    return res
for k in range(11):
    a=F(k,10)
    r=consistent(a)
    print("L03 alpha",a,[p for p,_ in r],[str(m) for _,m in r],"lost",[int(2000-2000*m) for _,m in r])
print("L03 threshold", F(CH-VL, VH-VL))
print("L03 alpha=1/2 avg", F(VH+VL,2))
