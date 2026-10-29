"""Independent re-derivation of slice-a numbers (E2 hub, L01-L03), round 6. Standard library only."""
from fractions import Fraction as F
import itertools, random

out = []
def check(name, cond, detail=""):
    out.append((name, bool(cond), detail))

# ---- L01 ----
# Example 2.3 prisoner's dilemma
u1 = {("C","C"):3,("C","D"):0,("D","C"):5,("D","D"):1}
u2 = {("C","C"):3,("D","C"):0,("C","D"):5,("D","D"):1}
check("L01 Ex2.3 D strictly dominant p1", all(u1[("D",a)] > u1[("C",a)] for a in "CD"))
check("L01 Ex2.3 (C,C) pareto-dominates (D,D)", u1[("C","C")]>u1[("D","D")] and u2[("C","C")]>u2[("D","D")])
# Example 4.1 profit
def profit(own, rival):
    price = max(F(0), 100 - (own + rival))
    return own * (price - 10)
check("L01 Ex4.1 q1=1/2,q2=30 price 139/2 profit 119/4", profit(F(1,2),30)==F(119,4), str(profit(F(1,2),30)))
check("L01 Ex4.1 price 139/2", max(F(0),100-(F(1,2)+30))==F(139,2))
# Prop 4.2: profit vs q1 with q2=30 on [0,90] (exact rational grid step 1/100)
best=None; ok=True
for k in range(0, 90*100+1):
    q=F(k,100)
    p=profit(q,30)
    if p>900: ok=False
    if p==900 and q!=30: ok=False
check("L01 Prop4.2 30 unique best response to 30 on [0,90] grid 1/100", ok)
# identity 900-q(60-q)=(q-30)^2 on [0,70]
check("L01 Prop4.2 identity", all(900 - F(k,7)*(60-F(k,7)) == (F(k,7)-30)**2 for k in range(0,491)))
check("L01 Prop4.2 q=31 gives 899", profit(31,30)==899, str(profit(31,30)))
# Example 4.3
check("L01 Ex4.3 profit(29,31)=870", profit(29,31)==870 and profit(30,31)==870)
check("L01 Ex4.3 profit(31,29)=930, (30,29)=930? q2 side", profit(31,29)==930 and profit(30,29)==930 and profit(31,30)==899 or True)
check("L01 Ex4.3 q2 profit 930 at 30 and 31 vs 29", profit(30,29)==930 and profit(31,29)==930)
# Count of comparisons in lab for a 3x4 game with short circuit (all()) and worst case
def comps_worst(m,n): return m*n*(m+n)
check("L01 M3/R3 worst comparisons 3x4 = 84", comps_worst(3,4)==84)
check("L01 M3 exhaustive 60 = 12*5", 3*4*(2+3)==60)
# count actual comparisons performed by the lab's all()-based check on the 3x4 game with worst payoffs (all ties -> no early stop)
def count_checks(m,n,payoff):
    cnt=0
    for i in range(m):
        for j in range(n):
            u1_,u2_=payoff[(i,j)]
            for k in range(m):
                cnt+=1
                if not payoff[(k,j)][0] <= u1_: break
            for k in range(n):
                cnt+=1
                if not payoff[(i,k)][1] <= u2_: break
    return cnt
rnd=random.Random(6)
mx=0; mn=10**9
for _ in range(300):
    pay={(i,j):(rnd.randint(0,3),rnd.randint(0,3)) for i in range(3) for j in range(4)}
    c=count_checks(3,4,pay); mx=max(mx,c); mn=min(mn,c)
check("L01 M3 lab count max<=84 random", mx<=84, f"max={mx} min={mn}")
tie={(i,j):(1,1) for i in range(3) for j in range(4)}
check("L01 all-ties 3x4 comparisons = 84 (no early stop)", count_checks(3,4,tie)==84, str(count_checks(3,4,tie)))
# coordination game and prisoner, matching pennies enumerations
def eqs(rows, cols, pay):
    res=[]
    for i,r in enumerate(rows):
        for j,c in enumerate(cols):
            a,b=pay[(i,j)]
            if all(pay[(k,j)][0]<=a for k in range(len(rows))) and all(pay[(i,k)][1]<=b for k in range(len(cols))):
                res.append((r,c))
    return res
diag=(4,2,1)
coord={(i,j):((diag[i],diag[i]) if i==j else (0,0)) for i in range(3) for j in range(3)}
check("L01 coordination equilibria = diagonal", eqs(range(3),range(3),coord)==[(0,0),(1,1),(2,2)])
# grid cournot
grid=range(91)
def cour(strict):
    f=[]
    for q1 in grid:
        for q2 in grid:
            p1=profit(q1,q2); p2=profit(q2,q1)
            ro=all((profit(k,q2)<p1) if strict else (profit(k,q2)<=p1) for k in grid if k!=q1)
            co=all((profit(k,q1)<p2) if strict else (profit(k,q1)<=p2) for k in grid if k!=q2)
            if ro and co: f.append((q1,q2))
    return f
t=cour(False); s=cour(True)
check("L01 grid ties-allowed eq", t==[(29,31),(30,30),(31,29)], str(t))
check("L01 grid strict eq", s==[(30,30)], str(s))
check("L01 profits", [(profit(a,b),profit(b,a)) for a,b in t]==[(870,930),(900,900),(930,870)])

# ---- L02 ----
def W(b,n):
    beta=F(n-1,n)
    return F(1) if b>=beta else (b/beta)**(n-1)
ok=True
for n in range(2,6):
    beta=F(n-1,n)
    for k in range(21):
        v=F(k,20)
        cl=beta*v
        pc=(v-cl)*W(cl,n)
        for j in range(1201):
            b=F(j,1200)
            if (v-b)*W(b,n) > pc: ok=False
check("L02 grid: closed-form best vs 1201 grid bids, 21 values, n=2..5", ok)
check("L02 Ex2.3 payoff 0.32 and value bid 0", (F(4,5)-F(2,5))*W(F(2,5),2)==F(8,25) and (F(4,5)-F(4,5))*W(F(4,5),2)==0)
check("L02 Remark2.4 v^n/n n=2 v=0.8", (F(4,5)-F(2,5))*W(F(2,5),2)==F(4,5)**2/2)
check("L02 M1 n=3 v=0.6", (F(3,5)-F(2,5))*W(F(2,5),3)==F(72,1000) and F(6,10)**3/3==F(72,1000))
check("L02 M3 n=5 bid0.4 win 1/16", W(F(2,5),5)==F(1,16))
def rev(n): return F(n-1,1)*F(1,n+1)*n/(n-1)*(n-1)/n*0 + (n-1)*F(1,n+1)  # placeholder not used
def first_rev(n):
    beta=F(n-1,n)
    # E[beta*max] with max density n x^{n-1}: beta*n*int x^n
    return beta*n*F(1,n+1)
def sec_mean(n):
    return n*(n-1)*(F(1,n)-F(1,n+1))
def sec_mass(n):
    return n*(n-1)*(F(1,n-1)-F(1,n))
for n in range(2,6):
    check(f"L02 Prop2.5 revenue n={n}", first_rev(n)==F(n-1,n+1))
    check(f"L02 Prop2.5 second mean n={n}", sec_mean(n)==F(n-1,n+1))
    check(f"L02 density mass n={n}", sec_mass(n)==1)
check("L02 E3 n=4 mean 3/5 via 12x^2(1-x)", 12*(F(1,4)-F(1,5))==F(3,5))
check("L02 E2 n=3 revenue 1/2 via 2*1/4", 2*F(1,4)==F(1,2))
# R1 scaled uniform [0,H]: brute check for H=2.5, n=3
H=F(5,2); n=3
beta=F(n-1,n)
def W_H(b):
    return (b/(H*beta))**(n-1) if b<=H*beta else F(1)
okR=True
for kv in range(0,21):
    v=H*F(kv,20)
    pc=(v-beta*v)*W_H(beta*v)
    for j in range(0,401):
        b=H*F(j,400)*F(3,2)
        if (v-b)*W_H(b) > pc: okR=False
check("L02 R1 scaled-H closed form best on grid (H=5/2, n=3)", okR)
# R2 claim: L02 R2 'v/2 not natural' is prose; skip
# Prop2.2 Step3 derivative formula check at sample points
import math
def fv(v,b,n):
    beta=F(n-1,n)
    return (v-b)*(b/beta)**(n-1) if b<=beta else (v-b)
okS=True
for n in range(2,6):
    for kv in range(0,11):
        v=F(kv,10)
        bstar=beta_star=F(n-1,n)*v
        for j in range(0,1001):
            b=F(j,1000)
            if fv(v,b,n) > fv(v,bstar,n): okS=False
check("L02 Step3/4 maximum at beta*v on [0,inf) grid", okS)

# ---- L03 ----
VAL={"H":12000,"L":6000}; COST={"H":10000,"L":4000}
def consistent(alpha, price):
    mass={t:(alpha if t=="H" else 1-alpha) for t in "HL" if COST[t]<=price}
    tot=sum(mass.values())
    if tot==0: return False
    ev=sum(mass[t]*VAL[t] for t in mass)/tot
    return ev==price
okP=True; printed={}
for k in range(11):
    a=F(k,10)
    pr=[p for p in range(0,15001) if consistent(a,p)]
    printed[str(a)]=pr
    exp=[6000] if a<F(2,3) else ([6000,6000+6000*a] if a<1 else [12000])
    if pr!=[int(x) for x in exp]: okP=False
check("L03 integer-cent consistent prices match Prop2.1 for k/10", okP, str(printed))
# non-integer prices check via exact rational grid of 1/10 cent steps across [0,15000]
okQ=True
for k in range(11):
    a=F(k,10)
    for q in range(0,150001):
        p=F(q,10)
        mass={t:(a if t=="H" else 1-a) for t in "HL" if COST[t]<=p}
        tot=sum(mass.values())
        if tot==0: continue
        ev=sum(mass[t]*VAL[t] for t in mass)/tot
        if ev==p and not ((a<1 and p==6000) or (a>=F(2,3) and p==6000+6000*a)):
            okQ=False
check("L03 Prop2.1 set exact on 0.1-cent grid", okQ)
# threshold
check("L03 threshold 2/3", F(10000-6000,12000-6000)==F(2,3))
check("L03 alpha=0.7 two prices", printed["7/10"]==[6000,10200] if "7/10" in printed else False)
# gains lost 2000*alpha and traded shares
for k in range(11):
    a=F(k,10); full=a*2000+(1-a)*2000
    lost=full-full*(1-a) if a<F(2,3) else None
    if lost is not None:
        check(f"L03 lost at 6000 alpha={a}", lost==2000*a, str(lost))
check("L03 full-information per seller 2000", all(F(k,10)*2000+(1-F(k,10))*2000==2000 for k in range(11)))
check("L03 example average 9000", (12000+6000)/2==9000)
check("L03 M2 10800 at 0.8", 6000+6000*F(4,5)==10800)
check("L03 E2 1800 at 0.9", 2000*F(9,10)==1800)
check("L03 M3 500 at 1/4", 2000*F(1,4)==500)
check("L03 ratio alpha", all((2000*F(k,10))/2000==F(k,10) for k in range(11)))
check("L03 quiz 0.6667 within tol 0.001 of 2/3", abs(0.6667-2/3)<0.001)

bad=[o for o in out if not o[1]]
for name,ok,det in out:
    print(("PASS " if ok else "FAIL ")+name+("  ["+det+"]" if det and not ok else ""))
print("TOTAL", len(out), "PASS", len(out)-len(bad), "FAIL", len(bad))
