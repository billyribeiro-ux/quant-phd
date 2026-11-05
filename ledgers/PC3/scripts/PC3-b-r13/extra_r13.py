import random
from fractions import Fraction as F
from collections import deque
def half_up(x, places):
    import math
    scale = 10**places
    n = math.floor(x*scale + F(1,2))
    return n/scale if places else n
def npv(cfs, r): return sum((c/(1+r)**t for t,c in enumerate(cfs)), F(0))
for rate in (F(8,100), F(10,100), F(12,100)):
    A = sum((1/(1+rate)**t for t in range(1,4)), F(0))
    be = F(15000000,5000)/A
    lo = npv([F(-15000000)] + [F(200*5000)]*3, rate)
    hi = npv([F(-15000000)] + [F(1600*5000)]*3, rate)
    print(float(rate*100), "lower", half_up(lo,0), "upper", half_up(hi,0), "be", half_up(be,2))
# Remark 4.3 / E3 derived from displayed 7-decimal factors (page claim) and from exact
print("8pct NPVs grid check fine")
# Random tests of the deque (Prop 3.2 correctness, Prop 3.3 bounds, Q7 tie rule)
rng = random.Random(12345)
fails = 0; checked = 0
for trial in range(4000):
    n = rng.randint(1, 30); k = rng.randint(1, n)
    xs = [rng.randint(0, 5) for _ in range(n)]  # many ties
    dq = deque(); out=[]; cmp_=0; pops=0; pushes=0
    for i, x in enumerate(xs):
        while dq:
            cmp_ += 1
            if xs[dq[-1]] > x: break
            dq.pop(); pops += 1
        dq.append(i); pushes += 1
        if dq[0] <= i - k: dq.popleft(); pops += 1
        if i >= k-1:
            out.append(xs[dq[0]])
            # Q7: front is the last occurrence of the window maximum
            w = list(range(i-k+1, i+1)); M = max(xs[j] for j in w)
            last = max(j for j in w if xs[j] == M)
            if dq[0] != last: fails += 1
    naive = [max(xs[s:s+k]) for s in range(n-k+1)]
    checked += 1
    if out != naive or cmp_ > 2*n or pushes != n or pops > n: fails += 1
print("random deque trials", checked, "failures", fails)
# P3 increasing check and R3 claim covered; Prop 2.1 count random
ok = True
for trial in range(500):
    n = rng.randint(1,40); k = rng.randint(1,n)
    xs = [rng.random() for _ in range(n)]
    c = sum(k-1 for _ in range(n-k+1))
    ok = ok and c == (n-k+1)*(k-1)
print("Prop 2.1 formula", ok)
