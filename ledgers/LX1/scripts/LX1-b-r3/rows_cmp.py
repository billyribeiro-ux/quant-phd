import math, sys
from fractions import Fraction as F
D0, N0 = F(1000000), F(4000000); delta = F(1,50)
def rhu(x,p): s=math.floor(x*10**p+F(1,2)); w,fr=divmod(s,10**p); return f"{w}.{fr:0{p}d}"
def rint(x): return math.floor(x+F(1,2))
P=lambda m,t:(1-delta)**min(t,m); V=lambda m,t:D0/P(m,t)
L=lambda v:v/(N0-(v-D0)); L0=L(D0)
out=[]
for m,label in ((12,"X"),(4,"Y")):
    for t in range(13):
        p=P(m,t); v=V(m,t); lev=L(v); ps=(lev-L0); fl=ps
        out.append(f"  t = {t:2d}: index {rhu(p,4)}; real debt {rint(v)} cents; leverage {rhu(lev,4)}; premium {rhu(ps,4)}; output fall {rhu(100*fl,2)} percent")
exp=open(sys.argv[1]).read().splitlines()
rows=[l for l in exp if l.startswith("  t =")]
print("computed rows", len(out), "twin rows", len(rows), "all equal:", out==rows)
print("M3 check: 1084166/3915834 =", rhu(F(1084166,3915834),4), "; exact L4 rounds", rhu(F(1084165)+F(7847339397,10**10)-F(1084165), 4) if False else "")
