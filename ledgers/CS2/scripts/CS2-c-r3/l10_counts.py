"""Recount L10 deque: appends, removals, step-(1) value comparisons, step-(3) index comparisons; random and worst-case tests."""
import random

def run(series, w, is_min=True):
    items = []
    ops = c1 = c3 = 0
    maxsz = 0
    for i, x in enumerate(series):
        rem = 0
        while items:
            back = items[-1][1]
            dom = back >= x if is_min else back <= x
            c1 += 1
            if not dom:
                break
            items.pop(); rem += 1
        items.append((i, x))
        while items:
            c3 += 1
            if items[0][0] <= i - w:
                items.pop(0); rem += 1
            else:
                break
        ops += 1 + rem
        maxsz = max(maxsz, len(items))
    return ops, c1, c3, maxsz

worst_total = 0; worst_c1 = 0; worst_all = 0
rng = random.Random(7)
for trial in range(20000):
    n = rng.randint(1, 30); w = rng.randint(1, 12)
    s = [rng.randint(0, 5) for _ in range(n)]
    ops, c1, c3, _ = run(s, w)
    assert ops <= 2 * n and c1 <= 2 * n, (s, w)
    worst_c1 = max(worst_c1, c1 - 2 * n)
    worst_all = max(worst_all, (c1 + c3) - 2 * n)
print("max over random trials of (step1 comparisons - 2n):", worst_c1)
print("max over random trials of (all comparisons - 2n):", worst_all)
# witness: all comparisons exceed 2n?
for s, w in [([1,2,3,4,5,0],5), ([0,1,2,3],1), ([3,1,4,1,5],3)]:
    print("series", s, "w", w, "ops, step1 cmp, step3 cmp, n:", run(s, w), len(s))
print("lab series min/max counts:")
rng2 = random.Random(1010)
series = [rng2.randint(0, 999) for _ in range(200)]
for w in (1, 2, 5, 13, 30):
    print(w, run(series, w, True), run(series, w, False))
