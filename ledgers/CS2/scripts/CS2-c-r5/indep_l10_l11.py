import random, math
from fractions import Fraction
# L10 independent: list-based monotonic deque, counting appends+removals
def run_window(series, w, is_min):
    dq=[]; ops=0; maxrem=0; maxsize=0; ok=True
    for i,x in enumerate(series):
        rem=0
        while dq and ((dq[-1][1] >= x) if is_min else (dq[-1][1] <= x)):
            dq.pop(); rem+=1
        dq.append((i,x))
        while dq[0][0] <= i-w:
            dq.pop(0); rem+=1
        ops += 1+rem; maxrem=max(maxrem,rem); maxsize=max(maxsize,len(dq))
        seg=series[max(0,i-w+1):i+1]
        want = min(seg) if is_min else max(seg)
        if dq[0][1]!=want: ok=False
    return ops,maxrem,maxsize,ok
rng=random.Random(1010)
s=[rng.randint(0,999) for _ in range(200)]
for w in (1,2,5,13,30):
    a=run_window(s,w,True); b=run_window(s,w,False)
    print(w, 'min ops',a[0],'max ops',b[0],'maxrem',max(a[1],b[1]),'maxsize',max(a[2],b[2]),'ok',a[3] and b[3])
# L11 independent: exact counts via plain sorted list and count, sketch via explicit lists
def sketch_run(xs, eps):
    levels=[]
    def cap(h): return 2*math.ceil(Fraction((h+1)*(h+2),1)/(2*eps))
    compactions=0
    def push(h,x):
        nonlocal compactions
        while len(levels)<=h: levels.append([])
        levels[h].append(x)
        if len(levels[h])==cap(h):
            buf=sorted(levels[h]); levels[h]=[]; compactions+=1
            keep=[buf[j] for j in range(len(buf)) if (j+1)%2==0]
            for y in keep: push(h+1,y)
    for x in xs: push(0,x)
    stored=[(v,2**h) for h,b in enumerate(levels) for v in b]
    return stored, compactions, [cap(0),cap(1),cap(2)]
N=5000
rng=random.Random(2026); xs=[rng.random() for _ in range(N)]
srt=sorted(xs)
probes=[Fraction(0),Fraction(1,100),Fraction(1,10),Fraction(1,4),Fraction(1,2),Fraction(3,4),Fraction(9,10),Fraction(99,100),Fraction(1)]
for eps in (Fraction(1,20),Fraction(1,10)):
    stored,comp,caps=sketch_run(xs,eps)
    tw=sum(w for _,w in stored)
    stored_sorted=sorted(stored)
    exc=Fraction(0); dfc=Fraction(0); allok=True
    for q in probes:
        target=q*N; cum=0; v=None
        for val,wt in stored_sorted:
            cum+=wt
            if cum>=target: v=val; break
        below=sum(1 for x in xs if x<v); le=sum(1 for x in xs if x<=v)
        if not (below<=q*N+eps*N and le>=q*N-eps*N): allok=False
        exc=max(exc, below-q*N); dfc=max(dfc,q*N-le)
    print('eps',eps,'caps',caps,'stored',len(stored),'comp',comp,'weight',tw,'pass',allok,'excess/N %.6f'%float(exc/N),'deficit/N %.6f'%float(dfc/N))
