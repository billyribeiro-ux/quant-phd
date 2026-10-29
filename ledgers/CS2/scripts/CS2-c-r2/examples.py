import math
from fractions import Fraction
def R(xs, v): return sum(1 for x in xs if x <= v)
def Rm(xs, v): return sum(1 for x in xs if x < v)
def ok(xs, q, v, eps):
    n = len(xs); return Rm(xs, v) <= q*n + eps*n and R(xs, v) >= q*n - eps*n
vals = list(range(1, 1001)); q = Fraction(1, 2); e = Fraction(1, 20)
print("L11 S3 ex: 500", ok(vals, q, 500, e), "501 eps0", Rm(vals,501)<=500 and R(vals,501)>=500, "450", ok(vals,q,450,e), Rm(vals,450), R(vals,450))
mix = [0]*500 + [1000]*500
print("L11 misc2: 1000 ok", ok(mix, q, 1000, e), "R-(1000)", Rm(mix,1000), "R(1000)", R(mix,1000))
print("L11 misc2 eps0 all v in [0,1000] pass:", all(Rm(mix,v)<=500 and R(mix,v)>=500 for v in range(0,1001)))
# L10 examples: deque-based
def deque_run(series, w, is_min=True):
    dq=[]; ops=0; rem_by=[]
    for i,x in enumerate(series):
        r=0
        while dq and ((series[dq[-1]]>=x) if is_min else (series[dq[-1]]<=x)): dq.pop(); r+=1
        dq.append(i)
        while dq[0] <= i-w: dq.pop(0); r+=1
        ops += 1+r; rem_by.append(r)
    return ops, rem_by
print("L10 E2 (1..5,0,w=5) removals:", deque_run([1,2,3,4,5,0],5)[1])
print("L10 R2 (4,1,4,w=2) fronts check: ", deque_run([4,1,4],2)[1])
print("L10 M2 ops (3,1,4,1,5 w=3):", deque_run([3,1,4,1,5],3))
print("L10 E1 w=1 ops n=200:", deque_run([0]*200,1)[0], "(series of constants)")
print("L10 R3 n=10 w=3 increasing ops:", deque_run(list(range(10)),3)[1], "sum", sum(deque_run(list(range(10)),3)[1]))
# L11 M3/E1: sketch with eps=1/10 on n values
def sketch(xs, eps):
    levels=[]
    def cap(h): return 2*math.ceil(Fraction((h+1)*(h+2),2)/eps)
    def push(h,x):
        while len(levels)<=h: levels.append([])
        b=levels[h]; b.append(x)
        if len(b)==cap(h):
            b.sort(); kept=b[1::2]; levels[h]=[]
            for y in kept: push(h+1,y)
    for x in xs: push(0,x)
    return levels
for n in (39,40):
    lv = sketch(list(range(n)), Fraction(1,10))
    print("L11 n=",n,"stored", sum(len(b) for b in lv), "weight", sum(len(b)*2**h for h,b in enumerate(lv)), "level sizes", [len(b) for b in lv])
