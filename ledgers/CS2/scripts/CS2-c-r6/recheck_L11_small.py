import random
from fractions import Fraction
src = open("/Users/billyribeiro/.fanout/wt/verifyB6-CS2-c/tests/labs/CS2/lab-CS2-L11-1.py", encoding="utf-8").read()
src = src.rsplit("\nmain()", 1)[0]
ns = {"__name__": "twin_noexec"}
exec(compile(src, "twin", "exec"), ns)
QS = ns["QuantileSketch"]
def run(n, eps, seed=2026):
    s = QS(eps)
    r = random.Random(seed)
    for _ in range(n):
        s.add(r.random())
    return s
s = run(39, Fraction(1, 10))
print("39 values eps=1/10: stored", s.stored(), "weight", s.total_weight(), "compactions", s.compactions, "levels", [len(l) for l in s.levels])
s = run(40, Fraction(1, 10))
print("40 values eps=1/10: stored", s.stored(), "weight", s.total_weight(), "levels", [len(l) for l in s.levels])
print("capacities eps=1/10 h=0..2:", [s.capacity(h) for h in range(3)], "eps=1/20:", [QS(Fraction(1,20)).capacity(h) for h in range(5)])
# M2 style check on a 7-weight state (1,w1),(2,w2),(5,w4)
s = QS(Fraction(1, 10)); s.n = 7; s.levels = [[1], [2], [5]]
print("M2 quantile(1/2) on pairs (1,1),(2,2),(5,4):", s.quantile(Fraction(1, 2)))
# stored count stream-independence for other N near 5000
for seed in (1, 2, 3):
    print("seed", seed, "stored eps1/20:", run(5000, Fraction(1, 20), seed).stored())
