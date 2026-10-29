import sys, random, json, math
from fractions import Fraction
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyB15-CS2-d/course/modules/CS/CS2/grader")
import instance
def close(a, b, rel=1e-9, absolute=1e-9):
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= max(absolute, rel * max(abs(a), abs(b)))
def exact_sample(vals):
    fr = [Fraction(x) for x in vals]; n = len(fr)
    mean = sum(fr, Fraction(0)) / n
    return sum(((x - mean) ** 2 for x in fr), Fraction(0)) / (n - 1)
fails = {0.0: [], 10000.0: [], 1000000.0: []}
passes = {0.0: [], 10000.0: [], 1000000.0: []}
for seed in range(50):
    rng = random.Random(seed)
    rng.randint(20, 400)
    off = rng.choice(instance.OFFSETS)
    inst = instance.make_instance(seed)
    vals = [float(x) for x in json.loads(inst["payload"])["values"]]
    n = len(vals); s = 0.0; ss = 0.0
    for x in vals:
        s += x; ss += x * x
    mean = s / n
    naive = (ss - n * mean * mean) / (n - 1)
    ok = close(naive, float(exact_sample(vals)))
    (passes if ok else fails)[off].append(seed)
for off in fails:
    print("offset", off, "naive fails", len(fails[off]), "passes", len(passes[off]), "fail seeds", fails[off][:30], "pass seeds", passes[off])
