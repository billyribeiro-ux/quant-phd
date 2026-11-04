# Independent exact recomputation of the L04 numeric claims (not using the twin code).
from fractions import Fraction as F
import math
pairs = [(v, u) for v in range(-4, 5) for u in range(-6, 7)]  # V forecast draw, U realised draw
print("pairs", len(pairs))
for b in range(0, 5):
    c = sum(1 for v, u in pairs if abs(1 + v - u) <= b)
    print("band", b, "hit count", c, "prob", F(c, 117), float(F(c, 117)))
def var_unif(n): return F(n*n - 1, 12)
vV, vU = var_unif(9), var_unif(13)
vE = vV + vU
print("Var V", vV, "Var U", vU, "Var e", vE)
se = math.sqrt(float(vE / 24)); print("se", se, "sq62/72", math.sqrt(62/72))
gap = F(41, 12) - 1; print("gap", gap, float(gap), "z", float(gap) / se)
# Part A path recomputed from the stated seed
import random
rng = random.Random(20261103)
path = []
for t in range(1, 25):
    u = rng.randint(-6, 6); v = rng.randint(-4, 4)
    path.append((t, 101 + v, 100 + u))
errs = [f - r for _, f, r in path]
hits = [1 if abs(e) <= 2 else 0 for e in errs]
print("hits", sum(hits), "hit rate", F(sum(hits), 24), "sum", sum(errs), "bias", F(sum(errs), 24))
print("first12 hit", F(sum(hits[:12]), 12), "bias", F(sum(errs[:12]), 12), "last12 hit", F(sum(hits[12:]), 12), "bias", F(sum(errs[12:]), 12))
print("E2 first12 errors", errs[:12], sum(errs[:12]))
print("E1 hits periods 13-24", [t for t, h in zip(range(1, 25), hits) if h and t >= 13])
print("MAE", F(sum(abs(e) for e in errs), 24))
print("mean-err check Ptheory", sum(1 + v - u for v, u in pairs) / len(pairs))
