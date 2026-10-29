"""Random check of L10 Theorem 2.2 (invariant), Theorem 2.3, Theorem 2.4 (<=2n), R1 looser rule, P3 max version."""
import random
from collections import deque

def run(series, w, strict_pop=False, is_min=True):
    dq = deque(); ops = 0; cmps = 0; states = []
    for i, x in enumerate(series):
        while dq:
            b = series[dq[-1]]
            cmps += 1
            if is_min:
                cond = (b > x) if strict_pop else (b >= x)
            else:
                cond = (b < x) if strict_pop else (b <= x)
            if not cond:
                break
            dq.pop(); ops += 1
        dq.append(i); ops += 1
        while dq[0] <= i - w:
            dq.popleft(); ops += 1
        states.append(list(dq))
    return states, ops, cmps

bad = dict(inv=0, front=0, bound=0, cmpbound=0, looser=0, maxver=0)
for t in range(3000):
    r = random.Random(t)
    n = r.randint(1, 25); w = r.randint(1, 8)
    s = [r.randint(0, 5) for _ in range(n)]
    st, ops, cmps = run(s, w)
    for i in range(n):
        W = range(max(0, i - w + 1), i + 1)
        S = [j for j in W if all(s[j] < s[l] for l in range(j + 1, i + 1))]
        if st[i] != S:
            bad["inv"] += 1
        if st[i]:
            if s[st[i][0]] != min(s[j] for j in W):
                bad["front"] += 1
            # latest attaining min
            m = min(s[j] for j in W)
            p = max(j for j in W if s[j] == m)
            if st[i][0] != p:
                bad["front"] += 1
    if ops > 2 * n:
        bad["bound"] += 1
    if cmps > 2 * n:
        bad["cmpbound"] += 1
    # R1 looser rule (strict pop) keeps the min at the front
    st2, _, _ = run(s, w, strict_pop=True)
    for i in range(n):
        W = range(max(0, i - w + 1), i + 1)
        m = min(s[j] for j in W)
        if s[st2[i][0]] != m:
            bad["looser"] += 1
    # max version: front is window max
    st3, _, _ = run(s, w, is_min=False)
    for i in range(n):
        W = range(max(0, i - w + 1), i + 1)
        if s[st3[i][0]] != max(s[j] for j in W):
            bad["maxver"] += 1
print("mismatch counts over 3000 random cases:", bad)
# E2-style: increasing 1..5 then 0 with w=5 min deque: one push removes 5
st, ops, cmps = run([1, 2, 3, 4, 5, 0], 5)
print("E2 final state", st[-1], "ops", ops)
# R1 claim: looser rule can hold equal values
st4, _, _ = run([2, 2, 2], 5, strict_pop=True)
print("looser rule with [2,2,2] deque:", st4[-1])
