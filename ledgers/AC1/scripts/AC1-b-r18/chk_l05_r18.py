import random
rng = random.Random(2605)
count = rng.randint(2, 4)
obs = []
for i in range(count):
    ot = rng.random() < 0.5
    d = rng.randint(1, 12)
    sa = rng.randint(50_000_00, 400_000_00)
    obs.append((ot, d, sa))
disc = rng.randint(8000, 9500)
price = sum(o[2] for o in obs) * disc // 10000
W = sum(o[2] for o in obs)
fl = [price*o[2]//W for o in obs]
rem = [price*o[2]-f*W for o,f in zip(obs,fl)]
L = price - sum(fl)
order = sorted(range(len(obs)), key=lambda i:(-rem[i], i))
al = fl[:]
for i in order[:L]: al[i]+=1
print("price", price, "alloc", al, "sum ok", sum(al)==price, "L", L, "rem", rem)
print("shares", [round(a/price,4) for a in al], sum(round(a/price,4) for a in al))
ota = [a for a,o in zip(al,obs) if o[0]]
def sched(a):
    b=a//12; return [b]*11+[a-11*b]
rev1=[0]*12; rev2=[0]*12
for o,a in zip(obs,al):
    if o[0]:
        for m,s in enumerate(sched(a)): rev1[m]+=s
        rev2[11]+=a
    else:
        rev1[o[1]-1]+=a; rev2[o[1]-1]+=a
import itertools
c1=list(itertools.accumulate(rev1)); c2=list(itertools.accumulate(rev2))
print("rev total", c1[-1], "m6 c1", c1[5], round(c1[5]/price,6), round(c1[5]/price,4))
print("m6 c2", c2[5], "diff", c1[5]-c2[5])
print("peak/price 32792272", 32792272/price, "23333398/price", 23333398/price, round(23333398/price,4))
print("E2 32792272/price", round(32792272/price,6))
print("sample ota months1-6", [ (a//12, a-11*(a//12), a//12*6 ) for a in ota])
for a in ota: print("a",a,"floor",a//12,"rem12",a-11*(a//12),"six",6*(a//12))
# billing
def alloc(total, weights):
    ws=sum(weights); fl=[total*w//ws for w in weights]; rm=[total*w-f*ws for w,f in zip(weights,fl)]
    l=total-sum(fl); od=sorted(range(len(weights)),key=lambda i:(-rm[i],i))
    for i in od[:l]: fl[i]+=1
    return fl
for up in (40,0):
    upf=price*up//100
    inst=alloc(price-upf,[1]*12)
    bill=[upf]+inst
    bc=list(itertools.accumulate(bill))
    rc=[0]+c1
    bal=[b-r for b,r in zip(bc,rc)]
    print("up",up,"end",bal[-1],"max",max(bal),"min",min(bal),"asset months",sum(1 for b in bal if b<0))
