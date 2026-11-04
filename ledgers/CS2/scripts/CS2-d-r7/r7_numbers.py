"""Re-derive the numeric claims of project.html, instance.py and the rank witnesses (CS2 slice d, round 7)."""
import math
import random
import sys
from collections import Counter
from fractions import Fraction

ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/course/modules/CS/CS2/grader")
from instance import make_instance, OFFSETS  # noqa: E402

# Lab 3 numbers
STREAM = ["10003.2", "10001.7", "10007.5", "10000.4", "10004.9", "10002.1", "10009.6", "10001.0", "10006.3", "10003.8", "10005.5"]
exact = [Fraction(s) for s in STREAM]
total = sum(exact)
mean = total / len(exact)
var = sum((x - mean) ** 2 for x in exact) / (len(exact) - 1)
print("lab3 sum", float(total), "exact mean", float(mean), "exact sample var", float(var))
print("lab3 q*n - eps*n", Fraction(1, 2) * 11 - Fraction("0.1") * 11, "ceil", math.ceil(Fraction(1, 2) * 11 - Fraction("0.1") * 11))
print("lab3 sorted 5th", sorted(exact)[4])

# Lab 1 numbers: random.Random(12) draws
rng = random.Random(12)
series = [rng.randint(0, 99) for _ in range(12)]
print("lab1 series", series)

# Rank witness: q=0.1, n=20, eps=0.05 exact vs float
print("witness exact ceil", math.ceil(Fraction(0.1) * 20 - Fraction(0.05) * 20), "float ceil", math.ceil(0.1 * 20 - 0.05 * 20))
print("witness exact diff", float(Fraction(0.1) * 20 - Fraction(0.05) * 20) - 1, "> 0:", Fraction(0.1) * 20 - Fraction(0.05) * 20 > 1)
# 0.2500004 witness
print("seven-decimal qn", float(Fraction(0.2500004) * 20), "ceil(qn-eps n)", math.ceil(Fraction(0.2500004) * 20 - Fraction(0.05) * 20), "q=0.25 target", math.ceil(Fraction(0.25) * 20 - Fraction(0.05) * 20), "float 0.25 expr", math.ceil(0.25 * 20 - 0.05 * 20))
# Exemplar: wide eps witness
print("wide eps: qn - eps n", 2 - 0.3 * 2, "exact", Fraction(2) - Fraction(0.3) * 2)

# Instance docstring counts: naive formula s += x, ss += x*x, mean = s/n, var = (ss - n*mean*mean)/(n-1)
def naive_var(values):
    s = 0.0
    ss = 0.0
    for x in values:
        s += x
        ss += x * x
    n = len(values)
    mean = s / n
    return (ss - n * mean * mean) / (n - 1)

def exact_var(values):
    fr = [Fraction(x) for x in values]
    n = len(fr)
    m = sum(fr) / n
    return sum((x - m) ** 2 for x in fr) / (n - 1)

def close(a, b):
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= max(1e-9, 1e-9 * max(abs(a), abs(b)))

by_off = Counter()
fails = Counter()
passes_seed = []
dup_check = set()
for seed in range(50):
    inst = make_instance(seed)
    import json
    p = json.loads(inst["payload"])
    vals = p["values"]
    off = min(OFFSETS, key=lambda o: abs(o - round(sum(vals) / len(vals))))
    # grouped by the offset make_instance draws: recompute draw
    rng2 = random.Random(seed)
    rng2.randint(20, 400)
    off_drawn = rng2.choice(OFFSETS)
    by_off[off_drawn] += 1
    nv = naive_var(vals)
    ev = float(exact_var(vals))
    if not close(nv, ev):
        fails[off_drawn] += 1
    else:
        passes_seed.append(seed)
print("seeds per offset", dict(by_off))
print("naive fails per offset", dict(fails))
print("naive passing seeds", passes_seed)
print("docstring claim: 0 of 16 at 0; 22 of 23 at 10000 (seed 41 passes); all 11 at 1e6")
