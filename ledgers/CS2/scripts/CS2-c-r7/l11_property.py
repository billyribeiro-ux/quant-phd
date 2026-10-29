"""Round 7 verifier: property test of Theorems 2.4 and 2.5 on random streams (stdlib only)."""
import bisect
import math
import random
from fractions import Fraction
import importlib.util, sys

spec = importlib.util.spec_from_file_location("l11c", "/Users/billyribeiro/.fanout/wt/verifyB7-CS2-c/ledgers/CS2/scripts/CS2-c-r7/l11_claims.py")
# reuse the Sk class without running its prints: copy the class source instead
src = open("/Users/billyribeiro/.fanout/wt/verifyB7-CS2-c/ledgers/CS2/scripts/CS2-c-r7/l11_claims.py").read()
cls_src = src.split("def ranks")[0]
ns = {}
exec(cls_src, ns)
Sk = ns["Sk"]
cap = ns["cap"]

rng = random.Random(7)
cases = 0
worst_E_ratio = 0.0
fails = 0
for trial in range(300):
    eps = Fraction(rng.choice([1, 2, 3, 5, 7, 10, 20, 50]), rng.choice([2, 3, 5, 7, 10, 20, 50, 100]))
    if not (0 < eps < 1):
        continue
    n = rng.randint(1, 1500)
    kind = rng.choice(["uniform", "ints", "dup", "sorted", "rev"])
    if kind == "uniform":
        xs = [rng.random() for _ in range(n)]
    elif kind == "ints":
        xs = [rng.randint(0, 20) for _ in range(n)]
    elif kind == "dup":
        xs = [float(rng.choice([0, 1000])) for _ in range(n)]
    elif kind == "sorted":
        xs = [float(i) for i in range(n)]
    else:
        xs = [float(n - i) for i in range(n)]
    sk = Sk(eps)
    for x in xs:
        sk.add(x)
    assert sk.weight() == n, ("weight", trial)
    E = sum(c * 2 ** h for h, c in sk.comp_by_level.items())
    if E > eps * n:
        fails += 1
        print("E > eps n", trial, E, float(eps * n))
    worst_E_ratio = max(worst_E_ratio, E / float(eps * n) if n else 0)
    srt = sorted(xs)
    for qi in range(0, 21):
        q = Fraction(qi, 20)
        v = sk.query(q)
        R = bisect.bisect_right(srt, v)
        Rm = bisect.bisect_left(srt, v)
        cases += 1
        if not (Rm <= q * n + eps * n and R >= q * n - eps * n):
            fails += 1
            print("quantile fails", trial, kind, n, eps, q, v, Rm, R)
    # Theorem 2.4 bounds on Rhat vs R for probes
    for probe in srt[:: max(1, n // 7)] + [srt[-1] + 1.0, srt[0] - 1.0]:
        Rhat = sum(2 ** h for h, b in enumerate(sk.levels) for x in b if x <= probe)
        Rhat_m = sum(2 ** h for h, b in enumerate(sk.levels) for x in b if x < probe)
        R = bisect.bisect_right(srt, probe)
        Rm = bisect.bisect_left(srt, probe)
        if not (-E <= Rhat - R <= 0 and -E <= Rhat_m - Rm <= 0):
            fails += 1
            print("Thm 2.4 fails", trial, kind, n, probe)
print("cases", cases, "fails", fails, "worst E/(eps n) ratio", round(worst_E_ratio, 4))
