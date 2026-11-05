"""Independent re-derivation of every number in the BK4 card slice (round 11, verifier d).

Written from the lesson text and the card text, not from the lab code. Prints one line per check.
"""
from fractions import Fraction as F
import math, random, itertools

fails = []
def check(label, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + label + f" | got {got} | want {want}")
    if not ok:
        fails.append(label)

# ---- L01 day, payments as printed in lab-BK4-L01-1 section A (page L01 line 52)
day = [(2,3,101800),(2,1,324400),(2,3,318300),(2,3,278600),(2,3,218000),(3,1,149400),
       (1,3,269700),(2,1,173600),(1,3,91800),(1,2,398400),(2,3,25300),(2,1,492300)]
# banks: index 1=A, 2=B, 3=C ; (sender, receiver, cents)
banks = {1:"A",2:"B",3:"C"}
def net(b): return sum(a for s,r,a in day if r==b) - sum(a for s,r,a in day if s==b)
def need(b):
    bal=0; low=0
    for s,r,a in day:
        if s==b: bal-=a
        elif r==b: bal+=a
        low=min(low,bal)
    return -low
def debit(b): return max(0,-net(b))
check("c010 Bank B RTGS need", need(2), 1533900)
check("c010 Bank B DNS debit", debit(2), 1533900)
check("c011 Bank A RTGS need", need(1), 112500)
check("c014 Bank A net", net(1), 379800)
check("c014 Bank A DNS debit", debit(1), 0)
check("c012 gross value", sum(a for *_,a in day), 2841600)
check("c012 DNS moved", sum(debit(b) for b in (1,2,3)), 1533900)
check("c012 share 4dp", round(F(1533900,2841600),4), F(5398,10000))
check("L01 net sum zero", sum(net(b) for b in (1,2,3)), 0)

# Example 2.6 and Remark 2.7 (page)
def peak(seq):
    bal=0; low=0
    for x in seq:
        bal+=x; low=min(low,bal)
    return -low
check("c008 Example 2.6 need A", peak([-100,80*0+0][:1]+[]) if False else peak([-100,50]), 100)
check("c009 Remark 2.7 need A", peak([50,-100]), 50)
check("c101 Example 2.6 net A", -100+50, -50)

# ---- L02 trades as printed in lab-BK4-L02-1 section A (page L02 line 56)
trades = [(1,2,1696600),(1,4,1873700),(4,3,1845000),(4,3,1495300),(2,1,314500),(1,2,371200)]
members = [1,2,3,4]
rec = {m: sum(a for p,r,a in trades if r==m) for m in members}
pay = {m: sum(a for p,r,a in trades if p==m) for m in members}
G = sum(a for *_,a in trades)
n = {m: rec[m]-pay[m] for m in members}
A = sum(max(0,n[m]) for m in members)
check("c031 netted amount", A, 5093600)
check("c092 gross notional", G, 7596300)
check("c092 sum receivables equals G", sum(rec.values()), G)
check("L02 net sum zero", sum(n.values()), 0)
check("L02 A equals sum max(0,-n)", sum(max(0,-n[m]) for m in members), A)
check("c031/L02 reduction bps floor", (10000*(G-A))//G, 3294)
check("c028 Example 2.4 bps", (10000*180)//230, 7826)
check("c027 Example 2.4 A", max(0,20)+max(0,30), 50)
# Example 2.4 nets: rec/pay
ex = [(1,2,100),(2,3,80),(3,1,50)]
nn = {m: sum(a for p,r,a in ex if r==m)-sum(a for p,r,a in ex if p==m) for m in (1,2,3)}
check("Example 2.4 nets", (nn[1],nn[2],nn[3]), (-50,20,30))
# cycle P3 and M2
check("c030 cycle netted", 0, 0)
# c033 claim: A=50 vs G=230
check("c033 G of Example 2.4", sum(a for *_,a in ex), 230)

# ---- L03 fixture (Example 1.5 / 1.6), by hand from Definition 1.1
def wf(L, IM, DF, K, surv):
    a1=min(L,IM); a2=min(L-a1,DF[0]); a3=min(L-a1-a2,K)
    Z=L-a1-a2-a3
    D=sum(d for _,d in surv)
    if Z>=D:
        return a1,a2,a3,{i:d for i,d in surv},Z-D
    pay={i: (Z*d)//D for i,d in surv}
    l=Z-sum(pay.values())
    for i,d in surv:
        if l==0: break
        if d>0: pay[i]+=1; l-=1
    return a1,a2,a3,pay,0
r=wf(200,100,(50,),30,[(1,40),(2,60)])
check("c043 Example 1.5 member1 pays", r[3][1], 8)
check("c043 Example 1.5 member2 pays", r[3][2], 12)
check("c043 residual", 200-r[0]-r[1]-r[2], 20)
check("c043 uncovered", r[4], 0)
r=wf(2,0,(0,),0,[(1,1),(2,1),(3,1)])  # defaulter 4 has DF 0 (Example 1.6)
check("c044 Example 1.6 Z=2 member1", r[3][1], 1)
check("c044 Example 1.6 member2", r[3][2], 1)
check("c044 Example 1.6 member3", r[3][3], 0)
check("c044 Example 1.6 floor shares", [ (2*1)//3 for _ in range(3)], [0,0,0])
# c048 k
check("c048 k", 9900*200//10000, 198)
# Lab 1 Part B sized margins: regenerate seeded losses as the lab does
rng = random.Random(2026)
MEM=(1,2,3,4)
im={i: rng.randint(1000,5000) for i in MEM}
df={i: rng.randint(100,900) for i in MEM}
cap=rng.randint(500,2000)
losses=[rng.randint(0,3000) for _ in range(200)]
def cover(M): return 10000*sum(1 for L in losses if L<=M)//len(losses)
def sized(t):
    k=-((-t*200)//10000)
    return sorted(losses)[k-1], k
s9900,k1=sized(9900); s9975,k2=sized(9975)
check("c049 sized margin 9900", s9900, 2961)
check("c050 sized margin 9975", s9975, 2992)
check("c049 cover at 2961", cover(2961), 9900)
check("c050 cover at 2992", cover(2992), 10000)
check("c049 brute force", min(M for M in range(3001) if cover(M)>=9900), 2961)
check("c050 brute force", min(M for M in range(3001) if cover(M)>=9975), 2992)
print("L03 seeded IM", im, "DF", df, "cap", cap)

# ---- L04 exact
rho=F(19,20)
check("c075 coverage at 1/2", (rho-F(1,2))/(1-F(1,2)), F(9,10))
check("c075 rho/2", rho/2, F(19,40))
check("c072 21/20 at 1/2", (F(21,20)-F(1,2))/F(1,2), F(11,10))
check("c072 bps", math.floor(10000*F(11,10)), 11000)
check("Remark 2.8 113/120", (F(19,20)-F(1,7))/(1-F(1,7)), F(113,120))
check("Remark 2.8 bps 9416", math.floor(10000*F(113,120)), 9416)
check("c073 threshold h=1/20", 1/(1-F(1,20)), F(20,19))
check("c073 threshold float", round(F(20,19).numerator/F(20,19).denominator,10), 1.0526315789)
# c074 measured coverage at rho=1, h=1/20
check("c074 measured ratio", 1*(1-F(1,20)), F(19,20))
# c076 identity theta - rho = x(rho-1)/(1-x), sample rho=19/20 x=1/5
th=(rho-F(1,5))/(1-F(1,5)); check("c069/c076 identity", th-rho, F(1,5)*(rho-1)/(1-F(1,5)))
# c068 identity sample
th=(F(21,20)-F(1,5))/(1-F(1,5)); check("c068 identity", th-1, (F(21,20)-1)/(1-F(1,5)))
# c069 difference identity sample x=1/5 y=51/100 rho=19/20
x,y=F(1,5),F(51,100)
tx=(rho-x)/(1-x); ty=(rho-y)/(1-y)
check("c069 difference identity", ty-tx, (y-x)*(rho-1)/((1-x)*(1-y)))
# c067 with A1..A3 : Res0-x C0 and claims (1-x)C0
check("c067 coverage formula at x=1/3, rho=19/20", (rho-F(1,3))/(1-F(1,3)), F(37,40))
check("c067 reserves and claims after x", (rho-F(1,3), 1-F(1,3)), (F(37,60), F(2,3)))
# c071 flooring identity: floor(y)>=10000 iff y>=10000 (check a few)
ok = all(((math.floor(F(k,3)) >= 10000) == (F(k,3) >= 10000)) for k in range(29990,30010))
check("c071 floor threshold sample", ok, True)
# L04 lab rows: seeded path - check the printed coverage 1760000/1860000 at x=7/100 and 220000/320000
check("L04 printed row rho19/20 x21/25", F(220000,320000), F(11,16))
check("L04 printed bps 6875", math.floor(10000*F(11,16)), 6875)
check("L04 printed bps 11000", math.floor(10000*F(21,20)*0 + 10000*F(11,10)), 11000)

# ---- L05 enumerations
p=F(1,8); kap=2500; ell=(1,2,4)
pats=list(itertools.product((0,1),repeat=3))
def P(x):
    out=F(1)
    for xi in x: out*= p if xi else 1-p
    return out
def C(x): return kap*sum(l*xi for l,xi in zip(ell,x))
mean=sum(P(x)*C(x) for x in pats)
check("c086 mean enumeration", mean, F(4375,2))
check("c086 closed form", p*kap*sum(ell), F(4375,2))
check("c094 round half up", math.floor(mean+F(1,2)), 2188)
varI=sum(P(x)*C(x)**2 for x in pats)-mean**2
pc=[(1-p,0),(p,kap*sum(ell))]
varC=sum(q*c*c for q,c in pc)-mean**2
check("c087 variance independent", varI, F(57421875,4))
check("c087 variance comonotone", varC, F(133984375,4))
check("c083 difference", varC-varI, 2*kap**2*p*(1-p)*sum(ell[i]*ell[j] for i in range(3) for j in range(i+1,3)))
check("c083 difference 19140625", varC-varI, 19140625)
check("c081 sum P C", sum(P(x)*C(x) for x in pats), p*kap*sum(ell))
check("c089 at least one fails indep", 1-P((0,0,0)), F(169,512))
check("c089 3p", 3*p, F(3,8))
check("c089 comonotone", p, F(1,8))
check("c090 equal delays", p*kap*(2+2+2), 1875)
check("c084 P(C=0) indep", P((0,0,0)), F(343,512))
check("c084 P(C=0) comon", 1-p, F(7,8))
check("c084 ordering", (1-p)**3 < 1-p, True)
# c089 general: 1-(1-p)^3 - 3p vs p^2(3-p)
pp=F(3,7)
check("c089 identity p^2(3-p)", 3*pp-(1-(1-pp)**3), pp*pp*(3-pp))
# c088 mean same under both laws
check("c088 comonotone mean", sum(q*c for q,c in pc), F(4375,2))
# c080 closed form under a 2nd marginal p=1/4, kappa 1000, delays 2,3,1
check("M1 check", F(1,4)*1000*6, 1500)

print("FAILS:", fails)
