"""Independent re-derivation of L05 numbers: own deque and naive implementations written from the page's pseudocode.

Usage: python -I recompute_L05.py. Stdlib only. Does not import the twin.
"""
import random

def seq(seed, n=200):
    r = random.Random(seed)
    return [r.randint(0, 999) for _ in range(n)]

def naive(xs, k):
    out = []; comps = 0
    for s in range(len(xs) - k + 1):
        w = xs[s:s+k]; best = w[0]
        for v in w[1:]:
            comps += 1
            best = max(best, v)
        out.append(best)
    return out, comps

def dq(xs, k):
    # page pseudocode, 1-indexed semantics mapped to 0-indexed positions
    d = []; out = []; comps = 0; pushes = 0; pops = 0
    for i, x in enumerate(xs):
        while d:
            comps += 1
            if xs[d[-1]] > x:
                break
            d.pop(); pops += 1
        d.append(i); pushes += 1
        if d[0] <= i - k:
            d.pop(0); pops += 1
        if i >= k - 1:
            out.append(xs[d[0]])
    return out, comps, pushes, pops

xs = seq(5)
print("seed5 k=8 windows", len(xs)-8+1)
n5, c5 = naive(xs, 8); o5, dc, dp, dpo = dq(xs, 8)
print("naive", c5, "deque comps", dc, "pushes", dp, "pops", dpo, "equal", n5 == o5)
print("formula", (200-8+1)*7)
print("part3 rows:")
for k in (1, 2, 8, 32, 200):
    _, nc = naive(xs, k); _, c, p, q = dq(xs, k)
    print(f"  k={k} windows={200-k+1} naive={nc} formula={(200-k+1)*(k-1)} deque_comps={c} pops={q} pushes={p}")
print("part2 all k 1..20 equal:", all(naive(xs,k)[0]==dq(xs,k)[0] for k in range(1,21)))
print("window1 equals seq:", dq(xs,1)[0]==xs, " whole max:", dq(xs,200)[0]==[max(xs)], " longer:", dq(xs,201)[0]==[])
print("first five values", xs[:5])
x6 = seq(6)
n6, c6 = naive(x6, 8); o6, dc6, dp6, dpo6 = dq(x6, 8)
print("seed6 k=8 outputs equal:", n6 == o6, "naive", c6, "deque comps", dc6, "pushes", dp6, "pops", dpo6)
print("E1 seed5 k=32 ratio", 5239/382)
for k in (2,3,5,7):
    x = list(range(k, 1, -1)) + [k+1]
    _, c, p, q = dq(x, k)
    print("R3.4 k", k, "len", len(x), "pops", q, "comps", c, "outputs", dq(x,k)[0])
print("Example 3.5:", dq([3,1,4,1,5],3)[0])
print("M2:", dq([2,5,1,0,3],2)[0])
ok = all(dq(list(range(1,21)), k)[1] == 19 for k in range(1,21))
print("increasing n=20 comparisons n-1 for every k:", ok)
best = max(range(1,201), key=lambda k: (200-k+1)*(k-1))
print("R2 argmax k", best, (200-best+1)*(best-1))
bad = 0
for s in range(200):
    r = random.Random(1000+s)
    xs2 = [r.randint(0,20) for _ in range(30)]
    for k in range(1,31):
        o, c, p, q = dq(xs2, k)
        if c > 2*30 or p != 30 or q > 30 or o != naive(xs2,k)[0]: bad += 1
print("prop 3.2/3.3 random violations:", bad)
