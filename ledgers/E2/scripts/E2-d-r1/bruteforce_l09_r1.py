# Independent brute force for L09 Part B/C counts, R1 per-w counts (c120), and Part A efficiency (c119, c135).
import itertools
from collections import Counter
def ranking(b): return sorted(range(len(b)), key=lambda i: (-b[i], i))
def rev(fmt, b, k):
    o = ranking(b); clr = b[o[k]]
    return sum(clr for _ in o[:k]) if fmt == "u" else sum(b[i] for i in o[:k])
cnt = Counter(); per_w = Counter(); k1 = 0
for b in itertools.product(range(4), repeat=4):
    d, u = rev("d", b, 2), rev("u", b, 2)
    cnt["gt" if d > u else "eq" if d == u else "lt"] += 1
    if d == u and len(set(b)) >= 1:
        s = sorted(b, reverse=True)
        if s[0] == s[1] == s[2]:
            per_w[s[0]] += 1
    if rev("u", b, 1) == sorted(b, reverse=True)[1] and rev("d", b, 1) == sorted(b, reverse=True)[0]:
        k1 += 1
print("Part B-style counts over 256 profiles (k=2):", dict(cnt), "total", sum(cnt.values()))
print("equal-revenue profiles by common top-three bid w:", dict(sorted(per_w.items())), "sum", sum(per_w.values()))
print("k=1 uniform=second-highest and discriminatory=highest over 256:", k1)
V = [9000, 5000, 6000, 7000]; B = [8000, 9500, 6500, 7000]
o = ranking(B); w = o[:2]
win_val = sum(V[i] for i in w); top2 = sum(sorted(V, reverse=True)[:2])
print("Part A winners", w, "value", win_val, "top2", top2, "eff", win_val/top2, "u", rev("u", B, 2), "d", rev("d", B, 2), "gap%", (rev("d",B,2)-rev("u",B,2))/rev("u",B,2)*100)
