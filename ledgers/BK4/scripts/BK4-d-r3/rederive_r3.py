# Independent re-derivation of the numbers on the BK4 cards (round 3). Stdlib only; written from the card text
# and from the printed lab output in the lesson, not from the twins' functions.
import random
from fractions import Fraction as F
from math import floor, ceil
ok = []
def chk(name, got, want):
    ok.append(got == want)
    print(("OK  " if got == want else "BAD ") + name + f": got {got}, want {want}")

# ---- L01: printed day (lesson lines 223-234), payer -> receiver, cents
pay = [("B","C",101800),("B","A",324400),("B","C",318300),("B","C",278600),("B","C",218000),("C","A",149400),
       ("A","C",269700),("B","A",173600),("A","C",91800),("A","B",398400),("B","C",25300),("B","A",492300)]
def run(seq, bank):
    s=0; mn=0; out=[]
    for snd,rcv,a in seq:
        if snd==bank: s-=a
        if rcv==bank: s+=a
        out.append(s); mn=min(mn,s)
    return out, -mn, s   # running sums, need (least opening balance), net position
for b in "ABC":
    sums, need, net = run(pay, b)
    debit = max(0,-net)
    print(b, "need", need, "net", net, "debit", debit)
A_sums,_,_ = run(pay,"A")
chk("c011 A running sum after payment 10", A_sums[9], -112500)
chk("c011 A need", run(pay,"A")[1], 112500)
chk("c011 A debit", max(0,-run(pay,"A")[2]), 0)
chk("c010 B need == debit 1533900", (run(pay,"B")[1], max(0,-run(pay,"B")[2])), (1533900,1533900))
chk("c014 A net", run(pay,"A")[2], 379800)
gross = sum(a for *_,a in pay); moved = max(0,-run(pay,"B")[2])
chk("c012 gross", gross, 2841600)
chk("c012 moved", moved, 1533900)
chk("c012 share rounded to 4 places", round(F(moved,gross),4), F(5398,10000))
# ---- L01 Example 2.6 and Remark 2.7 (dollars)
ex = [("A","B",100),("B","C",80),("C","A",50)]
chk("c008 Need_A", run(ex,"A")[1], 100); chk("c008 Debit_A", max(0,-run(ex,"A")[2]), 50)
chk("c008 A sums", run(ex,"A")[0], [-100,-100,-50])
ex2 = [("C","A",50),("A","B",100),("B","C",80)]
chk("c009 Need_A reordered", run(ex2,"A")[1], 50); chk("c009 sums", run(ex2,"A")[0], [50,-50,-50])
chk("c009 Debit unchanged", max(0,-run(ex2,"A")[2]), 50)
chk("c015 the peak need can change with order", run(ex2,"A")[1] != run(ex,"A")[1], True)
# c004 example from the card: receipt 300 then pay 500
chk("M1 need", run([("X","D",300),("D","X",500)],"D")[1], 200)  # M1 uses bank D with receipt first
# ---- L02 printed trades (lesson lines 219-224), member -> member, cents
tr = [(1,2,1696600),(1,4,1873700),(4,3,1845000),(4,3,1495300),(2,1,314500),(1,2,371200)]
G = sum(a for *_,a in tr)
rec = {m: sum(a for p,r,a in tr if r==m) for m in range(1,5)}
pay_ = {m: sum(a for p,r,a in tr if p==m) for m in range(1,5)}
n = {m: rec[m]-pay_[m] for m in range(1,5)}
A = sum(max(0,n[m]) for m in n)
chk("c031 netted A", A, 5093600); chk("c092 gross", G, 7596300)
chk("c092 sum receivables", sum(rec.values()), 7596300)
chk("sum of net obligations zero", sum(n.values()), 0)
chk("reduction bps", (10000*(G-A))//G, 3294)
chk("reduction cents", G-A, 2502700)
chk("E3 member 3 largest n", max(n, key=n.get), 3)
# Example 2.4
e24 = {1:(50,100),2:(100,80),3:(80,50)}
n24 = {m:r-p for m,(r,p) in e24.items()}
chk("c027 n", (n24[1],n24[2],n24[3]), (-50,20,30))
chk("c027 A", sum(max(0,x) for x in n24.values()), 50)
chk("c028 floor 10000*180/230", (10000*180)//230, 7826)
# M1 chain in L02 (dollars): n = -10,-20,50,-20; A=50; G=180; bps 7222
e = {1:(40,50),2:(50,70),3:(70,20),4:(20,40)}
nn = {m:r-p for m,(r,p) in e.items()}
chk("L02 M1 nets", (nn[1],nn[2],nn[3],nn[4]), (-10,-20,50,-20))
chk("L02 M1 bps", (10000*130)//180, 7222)
# P3 cycle k=3 check of zero nets (card c030 claim): every net zero
# ---- L03 Example 1.5 and 1.6, Lab fixture
def waterfall(L, im, df, K, dflt, survivors):
    a1=min(L,im[dflt]); a2=min(L-a1,df[dflt]); a3=min(L-a1-a2,K); Z=L-a1-a2-a3
    D=sum(df[i] for i in survivors)
    if Z>=D: return (a1,a2,a3,{i:df[i] for i in survivors}, Z-D)
    x={i: (Z*df[i])//D for i in survivors}
    left=Z-sum(x.values())
    for i in sorted(survivors):
        if left==0: break
        if df[i]>0: x[i]+=1; left-=1
    assert left==0
    return (a1,a2,a3,x,0)
im={3:100}; im.update({1:0,2:0}); df={1:40,2:60,3:50}
w=waterfall(200,im,df,30,3,[1,2])
chk("c043 member 1 pays 8", w[3][1], 8); chk("c043 member 2 pays 12", w[3][2], 12)
chk("c043 residual 20", 200-w[0]-w[1]-w[2], 20)
w181=waterfall(181,im,df,30,3,[1,2]); chk("L03 loss 181 leftover to member 1", w181[3][1], 1)
dfx={1:1,2:1,3:1}; w2=waterfall(2,{4:0,1:0,2:0,3:0},{1:1,2:1,3:1,4:0},0,4,[1,2,3])
chk("c044 members 1,2 pay one cent each", (w2[3][1],w2[3][2],w2[3][3]), (1,1,0))
# ---- L03 Part B: independent re-generation of the seeded losses (own code, same draw order as printed lab)
rng=random.Random(2026)
imS={i: rng.randint(1000,5000) for i in (1,2,3,4)}
dfS={i: rng.randint(100,900) for i in (1,2,3,4)}
capS=rng.randint(500,2000)
losses=[rng.randint(0,3000) for _ in range(200)]
def cover(M): return 10000*sum(1 for L in losses if L<=M)//200
def minimal(t):
    for M in range(0,3001):
        if cover(M)>=t: return M
s=sorted(losses)
for t in (9900,9975):
    k=ceil(t*200/10000)
    print("target",t,"k",k,"L(k)",s[k-1],"brute",minimal(t),"cover at L(k)",cover(s[k-1]),"cover one below",cover(s[k-1]-1))
chk("c048 k for 9900 of 200", ceil(9900*200/10000), 198)
chk("c049 sized margin 9900", s[197], 2961); chk("c049 brute", minimal(9900), 2961)
chk("c049 cover at 2961", cover(2961), 9900); chk("c049 cover at 2960", cover(2960), 9850)
chk("c050 sized margin 9975", s[199], 2992); chk("c050 brute", minimal(9975), 2992)
chk("c050 cover at 2992", cover(2992), 10000); chk("c050 cover at 2991", cover(2991), 9950)
chk("L03 Part A3 surviving scenario Z", 5850-3058-205-1730, 857)
chk("L03 E2 half of DF", (312*2,381*2,164*2), (624,762,328))
# ---- L04 coverage numbers
chk("c072 cov 19/20 at 1/2", (F(19,20)-F(1,2))/(1-F(1,2)), F(9,10))
chk("c072 bps", floor(10000*(F(19,20)-F(1,2))/(1-F(1,2))), 9000)
chk("c072 cov 21/20 at 1/2", (F(21,20)-F(1,2))/(1-F(1,2)), F(11,10))
chk("c072 bps 21/20", floor(10000*(F(21,20)-F(1,2))/(1-F(1,2))), 11000)
chk("c073 threshold", 1/(1-F(1,20)), F(20,19))
chk("c075 rho/2 for 19/20", F(19,40), F(19,20)/2)
chk("c075 counterexample rho=2/3, x=1/2 equals rho/2", (F(2,3)-F(1,2))/(1-F(1,2)), F(2,3)/2)
chk("c076 theta-rho identity", (F(3,5)-F(2,5))/(1-F(2,5)) - F(3,5), F(2,5)*(F(3,5)-1)/(1-F(2,5)))
chk("c012-like: L04 Remark2.8 x=1/7 bps", floor(10000*(F(19,20)-F(1,7))/(1-F(1,7))), 9416)
# ---- L05 cost model (exact fractions, own code)
p=F(1,8); kap=2500; ell=(1,2,4)
import itertools
tot=F(0); mean=F(0); ssq=F(0); pno=F(0)
for pat in itertools.product((0,1),repeat=3):
    pr=F(1)
    for x in pat: pr*= p if x else 1-p
    cst=sum(kap*l*x for l,x in zip(ell,pat))
    tot+=pr; mean+=pr*cst; ssq+=pr*cst*cst
    if sum(pat)==0: pno=pr
chk("c081 probs sum", tot, 1)
chk("c086 mean", mean, F(4375,2)); chk("c094 rounded half up", floor(mean+F(1,2)), 2188)
chk("c089 P(one fails) indep", 1-pno, F(169,512)); chk("c084 no-cost indep", pno, F(343,512))
chk("c089 3p", 3*p, F(192,512))
chk("c087 var indep", ssq-mean*mean, F(57421875,4))
# comonotone
Lsum=sum(ell)
pno4=1-p; mean4=p*kap*Lsum; var4=(kap*Lsum)**2*p*(1-p)
chk("c087 var comonotone", var4, F(133984375,4))
chk("c084 no-cost A4", pno4, F(7,8))
chk("c083 difference", var4-(ssq-mean*mean), 19140625)
chk("c083 closed form", 2*kap**2*p*(1-p)*sum(ell[i]*ell[j] for i in range(3) for j in range(i+1,3)), 19140625)
chk("c090 closed form equal delays", p*kap*(2+2+2), 1875)
chk("c088 means equal", mean4, mean)
chk("c080 mean closed form", mean, p*kap*Lsum)
chk("c089 A4 at least one fails", p, F(1,8))
print("ALL OK" if all(ok) else "SOME FAILED", len(ok), sum(ok))
