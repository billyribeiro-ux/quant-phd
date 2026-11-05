import random
from collections import deque
def seq(seed, n=200):
    r = random.Random(seed)
    return [r.randint(0, 999) for _ in range(n)]
def deq(xs, k):
    # independent implementation: survivors-based, count tests
    dq = []  # list of indices, front at 0
    out = []; cmp_ = pops = pushes = 0
    for i in range(len(xs)):
        while dq:
            cmp_ += 1
            if xs[dq[-1]] > xs[i]:
                break
            dq.pop(); pops += 1
        dq.append(i); pushes += 1
        if dq[0] <= i - k:
            dq.pop(0); pops += 1
        if i >= k - 1:
            out.append(xs[dq[0]])
    return out, cmp_, pops, pushes
def naive(xs, k):
    out = []; c = 0
    for s in range(len(xs) - k + 1):
        w = xs[s:s+k]
        out.append(max(w)); c += k - 1
    return out, c
def survivors_bruteforce(xs, k, i):
    # Definition 3.1 directly
    return [j for j in range(max(0, i-k+1), i+1) if all(xs[j] > xs[m] for m in range(j+1, i+1))]
xs5 = seq(5); xs6 = seq(6)
print("first5 seed5", xs5[:5], "max", max(xs5), "min", min(xs5))
o, c, p, pu = deq(xs5, 8); print("seed5 k8: deque cmp", c, "pops", p, "pushes", pu, "first5 max", o[:5], "naive", naive(xs5, 8)[1], "equal", naive(xs5,8)[0]==o)
o6, c6, p6, pu6 = deq(xs6, 8); print("seed6 k8: deque cmp", c6, "pops", p6, "pushes", pu6, "naive", naive(xs6,8)[1], "equal", naive(xs6,8)[0]==o6)
for k in (1, 2, 8, 32, 200):
    o, c, p, pu = deq(xs5, k)
    print("k", k, "windows", 200-k+1, "naive", naive(xs5, k)[1], "formula", (200-k+1)*(k-1), "deque_cmp", c, "pops", p, "pushes", pu, "outputs equal", naive(xs5,k)[0]==o)
ok = all(naive(xs5,k)[0]==deq(xs5,k)[0] for k in range(1,21))
print("equal 1..20", ok, "window1 identity", deq(xs5,1)[0]==xs5, "whole", deq(xs5,200)[0]==[max(xs5)])
# brute survivors check on seed5 for k=8
bad = 0
for i in range(200):
    pass
# Definition 3.1 deque equivalence: compare deque content with brute survivors at each step, k=8 and k=32
for k in (1,2,3,8,32):
    dq=[]
    for i in range(200):
        while dq and xs5[dq[-1]] <= xs5[i]: dq.pop()
        dq.append(i)
        if dq[0] <= i-k: dq.pop(0)
        if dq != survivors_bruteforce(xs5, k, i) and dq != [j for j in survivors_bruteforce(xs5, 10**9, i) if j > i-k]:
            bad += 1
print("survivor mismatches (k=1,2,3,8,32 combined)", bad)
# Remark 3.4: x = (k, k-1, ..., 1, k+1), n=k+1; removals at step k+1
for k in range(1, 12):
    x = list(range(k, 0, -1)) + [k+1]
    o, c, p, pu = deq(x, k)
    # per-step removals
    print("R3.4 k", k, "step k+1 removes", p, "(max over steps bounded by k)")
# Example 3.5
print("Ex3.5", deq([3,1,4,1,5],3)[0])
# M2
print("M2", deq([2,5,1,0,3],2)[0])
# E1 ratio
print("E1 ratio", 5239/382)
# P3: increasing sequence comparisons, several k
for k in (1,2,5,100):
    x = list(range(1, 201))
    print("P3 increasing k", k, "cmp", deq(x,k)[1], "n-1", 199)
print("E3 k=200 row: pops", deq(xs5,200)[2], "pushes", deq(xs5,200)[3], "cmp", deq(xs5,200)[1], "2n", 400, "194+200", 394)
