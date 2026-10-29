import random
from fractions import Fraction as F
def gen(seed,n=8):
    rng=random.Random(seed); out=[]
    for i in range(n):
        C=rng.randrange(20000,200001,1000); oi=5*rng.randint(C//125,C//31)
        out.append((f"SIM-{chr(65+i)}",C,oi))
    return out
r=F(900,10000)
def disc(ds,ties_ignored=True):
    cnt=0; tied=0; pairs=0
    for i,a in enumerate(ds):
        for b in ds[i+1:]:
            pairs+=1
            ri=(a[2]-r*a[1])-(b[2]-r*b[1]); ra=F(a[2],a[1])-F(b[2],b[1])
            if ri==0 or ra==0: tied+=1
            if (ri>0)!=(ra>0) and ri!=0 and ra!=0: cnt+=1
    return cnt,pairs,tied
ds=gen(20261027)
print('seed', disc(ds))
print('C values distinct:', len({d[1] for d in ds}))
print('seeds 1-40 with 4 discordant:', [s for s in range(1,41) if disc(gen(s))[0]==4])
print('seed20261027 ties:', disc(ds))
print('counts over seeds 1-40 in tie-check:', [disc(gen(s))[2] for s in range(1,41) if disc(gen(s))[2]])
# check: does ignoring ties (m04) change count for any seed 1..40?
def disc_noties(ds):
    cnt=0
    for i,a in enumerate(ds):
        for b in ds[i+1:]:
            ri=(a[2]-r*a[1])-(b[2]-r*b[1]); ra=F(a[2],a[1])-F(b[2],b[1])
            if (ri>0)!=(ra>0): cnt+=1
    return cnt
print('m04 diff on seeds 1-40 and 20261027:', [s for s in list(range(1,41))+[20261027] if disc_noties(gen(s))!=disc(gen(s))[0]])
# RI/EVA check of SIM-A capitalized
print('sign identity holds all seeds 20261027:', all(((a[2]-r*a[1])>=0)==(F(a[2],a[1])>=r) for a in ds))
