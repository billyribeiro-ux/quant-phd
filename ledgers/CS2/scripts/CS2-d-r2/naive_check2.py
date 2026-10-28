# Same as naive_check.py but with running float sums (the mutant's order: s += x, ss += x*x), sample divisor.
import sys, json
from fractions import Fraction
sys.path.insert(0, "/tmp/verifyB2-CS2-d/course/modules/CS/CS2/grader")
from instance import make_instance
def exact(vals):
    fr = [Fraction(x) for x in vals]; n = len(fr); m = sum(fr)/n
    return sum((x-m)**2 for x in fr)/(n-1)
def naive_run(vals):
    n = len(vals); s = 0.0; ss = 0.0
    for x in vals: s += x; ss += x*x
    mean = s/n
    return (ss - n*mean*mean)/(n-1)
def close(a, b):
    return abs(a-b) <= max(1e-9, 1e-9*max(abs(a), abs(b)))
by = {}
for seed in range(50):
    p = json.loads(make_instance(seed)["payload"])
    vals = [float(x) for x in p["values"]]
    m = sum(vals)/len(vals)
    off = 0 if abs(m) < 5000 else (10000 if abs(m) < 500000 else 1000000)
    ex = float(exact(vals))
    by.setdefault(off, []).append((seed, not close(naive_run(vals), ex)))
for off in sorted(by):
    rows = by[off]
    print("offset", off, "seeds", len(rows), "fails", sum(f for _, f in rows), "passing seeds", [s for s, f in rows if not f])
