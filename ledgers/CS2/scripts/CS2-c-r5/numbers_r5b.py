# CS2-c round 5: independent checks of L10 worked examples and L11 sketch claims (stdlib only).
import random, math, bisect
from fractions import Fraction
from collections import deque

def brute_min_deque_trace(series, w, is_min=True):
    dq=deque(); trace=[]; ops=0; removals_by_push=[]
    for i,x in enumerate(series):
        rem=0
        while dq:
            b=series[dq[-1]]
            dom = (b>=x) if is_min else (b<=x)
            if not dom: break
            dq.pop(); rem+=1
        dq.append(i)
        while dq[0] <= i-w:
            dq.popleft(); rem+=1
        ops += 1+rem
        removals_by_push.append(rem)
        trace.append([(j,series[j]) for j in dq])
    return trace, ops, removals_by_push

print("L10 M2 trace:", brute_min_deque_trace([3,1,4,1,5],3)[0])
print("L10 M2 ops (M3 expects 8):", brute_min_deque_trace([3,1,4,1,5],3)[1])
print("L10 M1 rolling min:", [min([3,1,4,1,5][max(0,i-2):i+1]) for i in range(5)])
t,ops,rem=brute_min_deque_trace([4,1,4],2); print("L10 R2 trace:", t)
t,ops,rem=brute_min_deque_trace([1,2,3,4,5,0],5); print("L10 E2 removals per push:", rem, "max", max(rem))
for n in (6,10,25):
    t,ops,rem=brute_min_deque_trace(list(range(n)),3); print("L10 R3 increasing n=%d w=3 total removals step3 (expect n-w=%d):"%(n,n-3), sum(rem)-(n-1)+0 if False else None)
# E1: window 1, any series: ops = 2n-1 ; E3 strictly decreasing: 2n-1
for seed in range(20):
    rng=random.Random(seed); s=[rng.randint(0,9) for _ in range(30)]
    assert brute_min_deque_trace(s,1)[1]==2*30-1
    assert brute_min_deque_trace(s,1,False)[1]==2*30-1
dec=[100-i for i in range(10)]
for w in (1,2,3,7,10,20):
    assert brute_min_deque_trace(dec,w)[1]==19, w
print("L10 E1/E3 ops checks pass (2n-1 for w=1 random; 19 for decreasing n=10 all w)")
# L10 ops for window 1 on seeded series N=200 (lab prints 399)
rng=random.Random(1010); series=[rng.randint(0,999) for _ in range(200)]
print("L10 lab series window1 ops:", brute_min_deque_trace(series,1)[1], brute_min_deque_trace(series,1,False)[1])

# L11 sketch
class Sk:
    def __init__(self, eps, count_only=False):
        self.eps=eps; self.levels=[]; self.n=0; self.comp=[]
    def cap(self,h): return 2*math.ceil(Fraction((h+1)*(h+2),2)/self.eps)
    def add(self,x):
        self.n+=1; self._push(0,x)
    def _push(self,h,x):
        while len(self.levels)<=h: self.levels.append([]); self.comp.append(0)
        b=self.levels[h]; b.append(x)
        if len(b)==self.cap(h):
            b.sort(); kept=b[1::2]; self.levels[h]=[]; self.comp[h]+=1
            for y in kept: self._push(h+1,y)
    def stored(self): return sum(len(b) for b in self.levels)
    def tw(self): return sum(len(b)*2**h for h,b in enumerate(self.levels))

for eps in (Fraction(1,20),Fraction(1,10)):
    results=[]
    for label,xs in [("uniform seed2026",[random.Random(2026).random() for _ in range(5000)]),
                     ("sorted",[i/5000 for i in range(5000)]),
                     ("reversed",[1-i/5000 for i in range(5000)]),
                     ("seed7",[random.Random(7).random() for _ in range(5000)])]:
        sk=Sk(eps)
        for x in xs: sk.add(x)
        results.append((label, sk.stored(), sum(sk.comp), sk.tw(), sk.comp[:4]))
    print("L11 eps=",eps, "caps k0..k2=", [Sk(eps).cap(h) for h in range(3)])
    for r in results: print("   ", r)

# per-level compaction bound vs actual for eps=1/20
sk=Sk(Fraction(1,20))
for x in [random.Random(2026).random() for _ in range(5000)]: sk.add(x)
bounds=[5000//(sk.cap(h)*2**h) for h in range(5)]
print("L11 E2: actual per-level compactions", sk.comp, "level bounds floor(5000/(k_h 2^h))", bounds, "sums", sum(sk.comp), sum(bounds))
print("L11 E2 k_h for h=0..4:", [sk.cap(h) for h in range(5)])

# Corollary 2.6 numbers
L=int(math.floor(math.log2(10**9))); print("L for 1e9 =", L, " (L+1)(L+2)(L+3)/(3eps)+(L+1) at eps=1/20:", (L+1)*(L+2)*(L+3)/(3/20)+(L+1))
L5=int(math.floor(math.log2(5000))); print("L for 5000 =", L5, " closed form:", (L5+1)*(L5+2)*(L5+3)/(3/20)+(L5+1), " exact sum k_h-1:", sum(Sk(Fraction(1,20)).cap(h)-1 for h in range(L5+1)))
print("R3 exact sum of (k_h-1), L=12:", sum(20*(h+1)*(h+2)-1 for h in range(13)))
print("M1 eps=1/10 k0..k2:", [Sk(Fraction(1,10)).cap(h) for h in range(3)])

# M3: 40 adds eps=1/10
sk=Sk(Fraction(1,10))
for i in range(40): sk.add(float(i))
print("L11 M3 40 adds eps=1/10: levels sizes", [len(b) for b in sk.levels], "total weight", sk.tw(), "comp", sk.comp)
# E1: 39 adds
sk=Sk(Fraction(1,10))
for i in range(39): sk.add(float(i))
print("L11 E1 39 adds eps=1/10: stored", sk.stored(), "total weight", sk.tw(), "comp", sk.comp)
# misc 2: 500 zeros and 500 thousands, eps=1/20 q=1/2
xs=[0.0]*500+[1000.0]*500
N=1000; q=Fraction(1,2); e=Fraction(1,20)
def R(v): return sum(1 for x in xs if x<=v)
def Rm(v): return sum(1 for x in xs if x<v)
print("misc2: v=1000 R-=",Rm(1000)," R=",R(1000)," allowed:", Rm(1000)<=q*N+e*N and R(1000)>=q*N-e*N)
print("misc2 all v in [0,1000] (eps=0) on grid? check v=0,1,500,999,1000:", [ (Rm(v)<=500 and R(v)>=500) for v in (0,1,500,999,1000)])
# canon bullet: values 1..1000 q=1/2
vals=list(range(1,1001)); N=1000
def RR(v): return sum(1 for x in vals if x<=v)
def RRm(v): return sum(1 for x in vals if x<v)
for v in (450,500,501):
    print("canon v=",v," R-=",RRm(v)," R=",RR(v), " eps=1/20 ok:", RRm(v)<=500+50 and RR(v)>=500-50, " eps0 ok:", RRm(v)<=500 and RR(v)>=500)
