"""Round-4 independent re-derivation of the numbers quoted on cards (exact fractions; no lesson code reused).

Usage: python3 -I ledgers/BK4/scripts/BK4-d-r4/rederive_r4.py
Inputs are the payment and trade lists transcribed from the printed lesson output (L01 section A, L02 section A),
and the printed L03 Part B scenario path is regenerated from the seed with random.Random (stdlib).
"""
import random
from fractions import Fraction as F
from math import floor, ceil

out = []
def say(label, value, expect):
    ok = value == expect
    out.append(ok)
    print(f"{'OK  ' if ok else 'DIFF'} {label}: got {value}, card/lesson says {expect}")

# ---- L01: payments in sending order (cents), from the printed Section A of the lab
pay = [("B","C",101800),("B","A",324400),("B","C",318300),("B","C",278600),("B","C",218000),("C","A",149400),
       ("A","C",269700),("B","A",173600),("A","C",91800),("A","B",398400),("B","C",25300),("B","A",492300)]
banks = ["A","B","C"]
def running(bank):
    s, sums = 0, [0]
    for snd, rcv, amt in pay:
        if snd == bank: s -= amt
        if rcv == bank: s += amt
        sums.append(s)
    return sums
def need(bank):
    return max(0, -min(running(bank)))
def net(bank):
    return sum(a for s,r,a in pay if r==bank) - sum(a for s,r,a in pay if s==bank)
for b in banks:
    print(b, "need", need(b), "net", net(b), "debit", max(0,-net(b)), "running", running(b))
say("L01 Bank B need", need("B"), 1533900)
say("L01 Bank B debit", max(0,-net("B")), 1533900)
say("L01 Bank A need", need("A"), 112500)
say("L01 Bank A debit", max(0,-net("A")), 0)
say("L01 Bank A net", net("A"), 379800)
say("L01 Bank A running sum after payment 10", running("A")[10], -112500)
say("L01 Bank C need", need("C"), 0)
say("L01 Bank C net", net("C"), 1154100)
gross = sum(a for *_, a in pay)
moved = sum(max(0,-net(b)) for b in banks)
say("L01 gross", gross, 2841600)
say("L01 DNS moved", moved, 1533900)
say("L01 share 0.5398 to four places", round(F(moved, gross), 4), F("0.5398"))
print("L01 share float", moved/gross)
# Example 2.6 and Remark 2.7 (hand example; cents -> dollars)
ex = [("A","B",100),("B","C",80),("C","A",50)]
def run_ex(seq, bank):
    s, sums = 0, [0]
    for snd, rcv, amt in seq:
        if snd == bank: s -= amt
        if rcv == bank: s += amt
        sums.append(s)
    return sums
say("Ex 2.6 running A", run_ex(ex,"A"), [0,-100,-100,-50])
say("Ex 2.6 need A", max(0,-min(run_ex(ex,"A"))), 100)
rem = [ex[2], ex[0], ex[1]]
say("Rem 2.7 running A", run_ex(rem,"A"), [0,50,-50,-50])
say("Rem 2.7 need A", max(0,-min(run_ex(rem,"A"))), 50)

# ---- L02 trades (cents) from the printed Section A
tr = [(1,2,1696600),(1,4,1873700),(4,3,1845000),(4,3,1495300),(2,1,314500),(1,2,371200)]
def rec(m): return sum(a for p,r,a in tr if r==m)
def pay_(m): return sum(a for p,r,a in tr if p==m)
G = sum(a for *_, a in tr)
n = {m: rec(m)-pay_(m) for m in range(1,5)}
A = sum(max(0,v) for v in n.values())
say("L02 gross", G, 7596300)
say("L02 sum receivables", sum(rec(m) for m in range(1,5)), 7596300)
say("L02 net obligations sum", sum(n.values()), 0)
say("L02 netted A", A, 5093600)
say("L02 reduction", G-A, 2502700)
say("L02 bps floor", (10000*(G-A))//G, 3294)
ex24 = {1: -50, 2: 20, 3: 30}
say("Ex 2.4 A", sum(max(0,v) for v in ex24.values()), 50)
say("Ex 2.4 bps", (10000*180)//230, 7826)
say("Ex 2.4 bps float", 10000*180/230, 7826.08)
say("M1 chain bps", (10000*130)//180, 7222)
say("R1 example: reduction when G=230,A=50", (10000*(230-50))//230, 7826)
say("c099/P3: cycle k=3 reduction bps", (10000*(3-0))//3, 10000)

# ---- L03
def waterfall(loss, im, df, cap, defaulter, surv):
    a1 = min(loss, im[defaulter]); a2 = min(loss-a1, df[defaulter]); a3 = min(loss-a1-a2, cap)
    Z = loss-a1-a2-a3
    D = sum(df[i] for i in surv)
    if Z >= D:
        pay = {i: df[i] for i in surv}; u = Z-D
    else:
        pay = {i: Z*df[i]//D for i in surv}
        left = Z - sum(pay.values())
        for i in surv:
            if left == 0: break
            if df[i] > 0: pay[i] += 1; left -= 1
        u = 0
    return a1, a2, a3, Z, pay, u
fx_im = {1:0,2:0,3:100}; fx_df = {1:40,2:60,3:50}
w = waterfall(200, fx_im, fx_df, 30, 3, [1,2])
say("Ex 1.5 L=200 pays", (w[4][1], w[4][2], w[5], w[3]), (8, 12, 0, 20))
w = waterfall(181, fx_im, fx_df, 30, 3, [1,2])
say("Ex 1.5 L=181 member1 leftover", w[4], {1:1, 2:0})
w = waterfall(300, fx_im, fx_df, 30, 3, [1,2])
say("Ex 1.5 L=300 uncovered", w[5], 20)
w = waterfall(2, {4:0,1:0,2:0,3:0}, {1:1,2:1,3:1,4:0}, 0, 4, [1,2,3])
say("Ex 1.6 Z=2 pays", w[4], {1:1, 2:1, 3:0})
# Lab 1 Part B: seeded scenario losses (SIMULATED), regenerated with the seed printed in the lab
rng = random.Random(2026)
im = {i: rng.randint(1000,5000) for i in (1,2,3,4)}
df = {i: rng.randint(100,900) for i in (1,2,3,4)}
cap = rng.randint(500,2000)
losses = [rng.randint(0,3000) for _ in range(200)]
say("Lab L03 IM/DF/cap regenerated", (im[3], df[3], cap), (3058, 205, 1730))
def ksize(t, S): return -((-t*S)//10000)
for t, exp in ((9900, 2961), (9975, 2992)):
    k = ksize(t, 200)
    srt = sorted(losses)
    say(f"Lab L03 sized margin t={t}", srt[k-1], exp)
    cov = lambda M: 10000*sum(1 for x in losses if x <= M)//200
    say(f"Lab L03 brute min t={t}", min(M for M in range(0, 3001) if cov(M) >= t), exp)
say("Ex 2.5 k for 9900 of 200", ksize(9900,200), 198)
say("Ex 2.5 k for 9975 of 200", ksize(9975,200), 200)
# Survivor example in lab Part A3 (E2): residual 857 and shares
say("L03 E2 residual", 5850-3058-205-1730, 857)
say("L03 E2 shares sum", 312+381+164, 857)
say("L03 E2 df sum", 624+762+328, 1714)
say("L03 E1 default fund pays", 3160-3058, 102)
# cover 9900 at k=198 of 200 and the 'two above' claim
say("L03 cover at c=198", 10000*198//200, 9900)
say("L03 cover at c=197", 10000*197//200, 9850)

# ---- L04
def cov(rho, x): return (rho-x)/(1-x)
say("L04 Prop 2.2 example 19/20, 1/2", cov(F(19,20),F(1,2)), F(9,10))
say("L04 21/20, 1/2", cov(F(21,20),F(1,2)), F(11,10))
say("L04 19/20, 1/7 coverage", cov(F(19,20),F(1,7)), F(113,120))
say("L04 bps of 113/120", floor(10000*F(113,120)), 9416)
say("L04 threshold 1/(1-h), h=1/20", F(1)/(1-F(1,20)), F(20,19))
say("L04 haircut 2*rho-1 at 19/20", 2*F(19,20)-1, F(9,10))
say("L04 measured at rho=1, h=1/20", cov(1*(1-F(1,20)), F(0)), F(19,20))
say("L04 coverage 1/2 halving (19/40)", F(19,20)/2, F(19,40))
say("L04 theta-rho sign rho=21/20", cov(F(21,20),F(1,2))-F(21,20), F(21,20)*0 + (F(21,20)*0 + (F(1,2)*(F(21,20)-1))/(1-F(1,2))))
say("L04 coverage at 21/25 bps", floor(10000*cov(F(19,20),F(21,25))), 6875)

# ---- L05
p = F(1,8); kap = 2500; ell = (1,2,4)
mean_closed = p*kap*sum(ell)
say("L05 closed mean", mean_closed, F(4375,2))
say("L05 rounded half up", floor(mean_closed + F(1,2)), 2188)
pats = [(x0,x1,x2) for x0 in (0,1) for x1 in (0,1) for x2 in (0,1)]
def P(x):
    r = F(1)
    for xi in x: r *= p if xi else 1-p
    return r
def C(x): return kap*sum(ell[i]*x[i] for i in range(3))
say("L05 enumerated mean", sum(P(x)*C(x) for x in pats), F(4375,2))
say("L05 P(no fail) indep", P((0,0,0)), F(343,512))
say("L05 P(>=1 fail) indep", 1-P((0,0,0)), F(169,512))
say("L05 3p", 3*p, F(3,8))
say("L05 comonotone P(no cost)", 1-p, F(7,8))
say("L05 p(>=1) under A4", p, F(1,8))
def var(outs):
    m = sum(pr*c for pr,c in outs); return sum(pr*c*c for pr,c in outs) - m*m
ind = [(P(x), C(x)) for x in pats]
com = [(1-p, 0), (p, kap*sum(ell))]
say("L05 variance independent", var(ind), F(57421875,4))
say("L05 variance comonotone", var(com), F(133984375,4))
say("L05 difference = 2k^2p(1-p) sum_{i<j}", var(com)-var(ind), 2*kap*kap*p*(1-p)*(ell[0]*ell[1]+ell[0]*ell[2]+ell[1]*ell[2]))
say("L05 equal delays 2 enumeration", sum(P(x)*kap*2*sum(x) for x in pats), 1875)
say("L05 Prop 2.6 P(C=0) indep", (1-p)**3, F(343,512))
say("L05 Ex 2.7 3p-(1-(1-p)^3)", 3*p-(1-(1-p)**3), F(1,8)**2*(3-F(1,8)))
say("L05 p=1/4 mean M1 (delays 2,3,1, kappa 1000)", F(1,4)*1000*(2+3+1), 1500)
say("L05 R2 bounds 5/8", 1-F(3,8), F(5,8))
say("L05 Q5 one trade expected cost 1/4*1000*3", F(1,4)*1000*3, 750)
say("L05 Prop 2.5 at p=1/8 vs Ex 2.7 lab", 1-(F(7,8))**3, F(169,512))
print("ALL OK" if all(out) else "SOME DIFFS")
