import random, math, bisect
from collections import deque
from fractions import Fraction
# L10 Theorem 2.2 / 2.3 randomized check (min deque), with ties
bad=0
for trial in range(3000):
    rng=random.Random(trial); w=rng.randint(1,6); n=rng.randint(1,30)
    s=[rng.randint(0,4) for _ in range(n)]
    dq=deque()
    for i,x in enumerate(s):
        while dq and s[dq[-1]]>=x: dq.pop()
        dq.append(i)
        while dq[0]<=i-w: dq.popleft()
        W=range(max(0,i-w+1),i+1)
        S=[j for j in W if all(s[j]<s[l] for l in range(j+1,i+1))]
        if list(dq)!=S: bad+=1
        if s[dq[0]]!=min(s[j] for j in W): bad+=1
        if dq[0]!=max(j for j in W if s[j]==min(s[k] for k in W)): bad+=1
print("L10 Thm2.2/2.3 violations:", bad)
# L11 Theorem 2.4 randomized: -E <= hatR - R <= 0 and hatR^- - R^- similarly, E <= eps n; Theorem 2.5 check
class Sk:
    def __init__(s_,eps): s_.eps=eps; s_.levels=[]; s_.comp=[]; s_.n=0
    def cap(s_,h): return 2*math.ceil(Fraction((h+1)*(h+2),2)/s_.eps)
    def add(s_,x): s_.n+=1; s_._push(0,x)
    def _push(s_,h,x):
        while len(s_.levels)<=h: s_.levels.append([]); s_.comp.append(0)
        b=s_.levels[h]; b.append(x)
        if len(b)==s_.cap(h):
            b.sort(); kept=b[1::2]; s_.levels[h]=[]; s_.comp[h]+=1
            for y in kept: s_._push(h+1,y)
    def items(s_): return [(x,2**h) for h,b in enumerate(s_.levels) for x in b]
viol=0; checked=0
for trial in range(60):
    rng=random.Random(100+trial); eps=Fraction(rng.choice([1,2,3,5,10,20]),rng.choice([20,30,50]))
    if not (0<eps<1): continue
    n=rng.randint(1,600); xs=[rng.randint(0,50) for _ in range(n)]
    sk=Sk(eps)
    for x in xs: sk.add(x)
    E=sum(c*2**h for h,c in enumerate(sk.comp))
    if E> eps*n: viol+=1
    srt=sorted(xs)
    items=sk.items()
    for v in sorted(set(xs))+[-1,51]:
        R=bisect.bisect_right(srt,v); Rm=bisect.bisect_left(srt,v)
        hR=sum(w for x,w in items if x<=v); hRm=sum(w for x,w in items if x<v)
        if not (-E<=hR-R<=0 and -E<=hRm-Rm<=0): viol+=1
        checked+=1
    tot=sum(w for _,w in items)
    if tot!=n: viol+=1
    # Theorem 2.5 for q grid
    for q in [Fraction(k,20) for k in range(21)]:
        target=q*n; cum=0; ans=None
        for x,w in sorted(items):
            cum+=w
            if cum>=target: ans=x; break
        if ans is None: viol+=1; continue
        R=bisect.bisect_right(srt,ans); Rm=bisect.bisect_left(srt,ans)
        if not (R>=q*n-eps*n and Rm<=q*n+eps*n): viol+=1
print("L11 Thm2.2(a)/2.4/2.5 randomized violations:", viol, "points checked:", checked)
