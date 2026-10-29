from fractions import Fraction as F
import itertools
# L01
d=F(1000); rho=F(1,10)
S=[sum(d*(1-rho)**t for t in range(n+1)) for n in range(11)]
print("S1",S[1],"S2",S[2],"S10",float(S[10]), "cents", int(S[10]*100+F(1,2)))
print("rounded 4dp multiplier*1000", F(round(float(S[10]/d),4))*1000)
print("half limit", d/(1-F(1,2)*(1-rho)), float(d/(1-F(1,2)*(1-rho))/10000*100))
print("E2 ratio", (d/(1-F(1,2)*(1-rho)))/(d/rho), "=2/11?", (d/(1-F(1,2)*(1-rho)))/(d/rho)==F(2,11))
q=F(1,2)
print("S10 half share", sum(d*(F(9,20))**t for t in range(11)))
print("M2", F(800)*(1-(F(3,4))**3)/F(1,4), "M3 eq", 300-320)
# L03 Example 2.5 and R2, M2
def pay(sig,q,p): return sig*q*p
h=2
C=-9998*100+9992*100; print("Ex2.5 C",C,"hV",2*h*200,"mid",(-1)*100*(10000-9990))
C2=-9988*100+10002*100; print("R2 C",C2,"mid",(-1)*100*(9990-10000)+0)
print("M2 cash", 10006*80-10008*80)
# Prop 2.3 general identity check random small instances with constant h
import random
rng=random.Random(1)
bad=0
for _ in range(2000):
    n=rng.randint(1,6); h=rng.randint(1,5)
    trades=[(rng.choice([1,-1]), rng.randint(1,9), rng.randint(900,1100)) for _ in range(n)]
    mn=trades[-1][2]
    C=sum(s*q*(m+s*h) for s,q,m in trades); I=-sum(s*q for s,q,m in trades); V=sum(q for s,q,m in trades)
    P=C+I*mn
    rhs=h*V+sum(s*q*(m-mn) for s,q,m in trades)
    if P!=rhs: bad+=1
print("constant-h identity failures", bad)
# varying-h counterexample: same mid, half-spread 1 then 3
m=10000
C=(m+1)-(m-3); print("varying-h cash (buy at ask m+1, sell at bid m-3, 1 share each)", C, "spread capture with h=1:", 2, "h=3:", 6)
# Prop 3.2 brute force on wider grid with Q=1000,c=100
def prof(d,o,c,Q):
    if d<o: return (d-c)*Q
    if d==o: return (d-c)*Q/2
    return 0
c=100;Q=1000
eq=[]
asks=range(c,c+60)
for a,b in itertools.product(asks,asks):
    ok=all(prof(x,b,c,Q)<=prof(a,b,c,Q) for x in asks) and all(prof(x,a,c,Q)<=prof(b,a,c,Q) for x in asks)
    if ok: eq.append((a,b))
print("wide-grid equilibria", eq)
# three dealers R1 check symmetric
def prof3(d,others,c,Q):
    lo=min(others)
    if d<lo: return (d-c)*Q
    if d==lo:
        k=sum(1 for o in others if o==lo)+1
        return (d-c)*Q/k
    return 0

# three dealers R1 symmetric profiles, Q multiple of 3
Q3=300
def pay3(i,asks,c,Q):
    a=asks[i]; lo=min(asks)
    if a>lo: return 0
    k=sum(1 for x in asks if x==lo)
    return (a-c)*Q/k if a==lo else 0
def eq3(asks,c,Q):
    for i in range(3):
        base=pay3(i,asks,c,Q)
        for dv in range(c,c+60):
            alt=list(asks); alt[i]=dv
            if pay3(i,alt,c,Q)>base: return False
    return True
for k in range(0,4):
    print("3-dealer symmetric k",k, eq3([100+k]*3,100,Q3))
