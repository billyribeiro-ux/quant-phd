import sys, json, math, random
from fractions import Fraction
sys.path.insert(0, '/Users/billyribeiro/.fanout/wt/verifyD3-CS2-d/course/modules/CS/CS2/grader')
import importlib.util
spec = importlib.util.spec_from_file_location('instance', '/Users/billyribeiro/.fanout/wt/verifyD3-CS2-d/course/modules/CS/CS2/grader/instance.py')
inst = importlib.util.module_from_spec(spec); spec.loader.exec_module(inst)
def close(a, b, rel=1e-9, absolute=1e-9):
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= max(absolute, rel * max(abs(a), abs(b)))
groups = {}
fails = {}
for seed in range(50):
    ins = inst.make_instance(seed)
    p = json.loads(ins['payload'])
    vals = [float(x) for x in p['values']]
    offset = min(vals, key=lambda v: 0)  # placeholder
    # offset: the drawn offset, recover from rng the same way make_instance does
    rng = random.Random(seed); rng.randint(20, 400); off = rng.choice(inst.OFFSETS)
    s = 0.0; ss = 0.0
    for x in vals:
        s += x; ss += x * x
    n = len(vals); mean = s / n
    naive = (ss - n * mean * mean) / (n - 1)
    fr = [Fraction(x) for x in vals]; fm = sum(fr) / n
    exact = sum((x - fm) ** 2 for x in fr) / (n - 1)
    ok = close(naive, float(exact))
    groups.setdefault(off, []).append(seed)
    if not ok: fails.setdefault(off, []).append(seed)
for off in sorted(groups):
    print(f"offset {off:>12}: seeds {len(groups[off])}, naive fails {len(fails.get(off, []))}, passing seeds {sorted(set(groups[off]) - set(fails.get(off, [])))}")
