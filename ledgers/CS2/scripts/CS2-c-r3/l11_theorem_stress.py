"""Randomised and structured stress of Theorems 2.2, 2.4, 2.5 on many streams (CS2-c r3). Supports, does not prove."""
import sys, random, bisect
from fractions import Fraction as F
exec(open(sys.argv[1], encoding="utf-8").read().split('print("capacities')[0])
checked = 0; worst = {}
streams = []
rng = random.Random(7)
for trial in range(300):
    n = rng.randint(1, 400)
    kind = trial % 4
    if kind == 0: xs = [rng.random() for _ in range(n)]
    elif kind == 1: xs = sorted(rng.random() for _ in range(n))
    elif kind == 2: xs = sorted((rng.random() for _ in range(n)), reverse=True)
    else: xs = [rng.randint(0, 3) for _ in range(n)]
    streams.append(xs)
for eps in (F(1, 20), F(1, 10), F(1, 3), F(9, 10)):
    for xs in streams:
        sk = Sk(eps)
        ordered_prefix = []
        for x in xs:
            sk.add(x)
        n = len(xs)
        assert sk.weight() == n
        E = sum(c * 2 ** h for h, c in sk.C.items())
        assert E <= eps * n, (eps, n, E)
        ordered = sorted(xs)
        for qn in range(0, 21):
            q = F(qn, 20)
            v = sk.query(q)
            R = bisect.bisect_right(ordered, v); Rm = bisect.bisect_left(ordered, v)
            Rhat = sum(w for (val, w) in sk.items() if val <= v)
            Rhatm = sum(w for (val, w) in sk.items() if val < v)
            assert -E <= Rhat - R <= 0 and -E <= Rhatm - Rm <= 0
            assert R >= q * n - eps * n and Rm <= q * n + eps * n, (eps, n, q, v)
            assert R >= q * n - E and Rm <= q * n + E
            checked += 1
print("streams", len(streams), "eps values 4, quantile probes checked", checked, "all assertions held")
