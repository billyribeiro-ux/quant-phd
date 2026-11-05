"""Verifier round 8: the seed-6 numbers quoted in L05 Empirical problem E2 (not printed by the lab), and P3 check."""
import random, sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE8-PC3-b/ledgers/PC3/scripts/PC3-b-r8")
from l05_independent import naive, deque_alg, seq

xs6 = seq(6, 200)
nv, nc = naive(xs6, 8)
dv, c, po, pu = deque_alg(xs6, 8)
print("seed6 k=8: outputs equal", nv == dv, "naive", nc, "deque comparisons", c, "pops", po, "pushes", pu)
# lab-twin functions, run on seed 6 by importing the twin module source with main() suppressed
import importlib.util, io, contextlib
src = open("/Users/billyribeiro/.fanout/wt/verifyE8-PC3-b/tests/labs/PC3/lab-PC3-L05-1.py").read().replace("\nmain()", "\n")
ns: dict = {}
exec(compile(src, "twin", "exec"), ns)
ops = ns["deque_maxima"](xs6, 8)[1]
print("twin deque_maxima on seed 6, k=8: comparisons", ops.comparisons, "pops", ops.pops, "pushes", ops.pushes)
# P3 increasing sequence: comparisons n-1 for every k (n=7..12)
ok = True
for n in range(1, 13):
    for k in range(1, n + 1):
        xs = list(range(n))
        _, o = ns["deque_maxima"](xs, k)
        if o.comparisons != n - 1:
            ok = False
print("P3 increasing sequences: comparisons == n-1 for all n<=12, k<=n:", ok)
