import random
rng = random.Random(2604)
Q = []
for _ in range(8):
    cs = rng.randint(50_000_00, 120_000_00)
    cr = rng.randint(20_000_00, 60_000_00)
    pp = rng.randint(40_000_00, 90_000_00) if rng.random() < 1/3 else 0
    ox = rng.randint(30_000_00, 70_000_00)
    it = rng.randint(2_000_00, 5_000_00)
    Q.append((cs, cr, pp, ox, it))
exp = [0]*8
for s,(cs,cr,pp,ox,it) in enumerate(Q):
    base = pp//4
    sh = [base,base,base,pp-3*base]
    for o in range(4):
        if s+o < 8: exp[s+o] += sh[o]
import itertools
cum_pp = list(itertools.accumulate(q[2] for q in Q))
cum_e = list(itertools.accumulate(exp))
bal = [a-b for a,b in zip(cum_pp,cum_e)]
print("prepaid_paid", [q[2] for q in Q])
print("bal", bal)
ni_a=[]; ni_b=[]
rev=[q[0]+q[1] for q in Q]
for t,(cs,cr,pp,ox,it) in enumerate(Q):
    ni_a.append(rev[t]-ox-it-pp); ni_b.append(rev[t]-ox-it-exp[t])
print("ni_a", ni_a); print("ni_b", ni_b)
d=[a-b for a,b in zip(ni_a,ni_b)]
dbal=[bal[0]]+[bal[t]-bal[t-1] for t in range(1,8)]
print("NI_A-NI_B per q", d)
print("-(delta bal) per q", [-x for x in dbal], "match", d==[-x for x in dbal])
print("cum diff", sum(d), "minus end bal", -bal[-1])
print("6632381//4", 6632381//4, 6632381-6632381//4)
print("ratio 3319293/27832482", 3319293/27832482, round(3319293/27832482,4))
print("ratio 3319293/24513189", 3319293/24513189, round(3319293/24513189,4))
print("interest total", sum(q[4] for q in Q))
cfo1=sum(q[0]+ (0) for q in Q)  # placeholder
cash=[]
rcpt=[Q[t][0]+(Q[t-1][1] if t>0 else 0) for t in range(8)]
paid=[q[2]+q[3]+q[4] for q in Q]
cc=[a-b for a,b in zip(rcpt,paid)]
print("cash end", sum(cc), "cfo2", sum(cc)+sum(q[4] for q in Q), "diff", sum(q[4] for q in Q))
print("cumNI_a", sum(ni_a), "cumNI_b", sum(ni_b))
