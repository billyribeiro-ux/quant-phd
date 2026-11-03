import json, sys, re
sys.path.insert(0, sys.argv[1])
import constrained_allocator as ref
from instance import make_instance
# count iterations of the active-set loop by wrapping _kkt_step
count = {"n": 0, "max": 0}
orig = ref._kkt_step
cur = {"k": 0}
def wrapped(h, g, a):
    return orig(h, g, a)
rows = []
stats = []
for s in range(50):
    case = json.loads(make_instance(s)["payload"])
    problem = ref._parse(case)
    rws = ref._inequalities(problem)
    # replicate _active_set loop with a counter by monkey-patching range is awkward; re-run the search and count KKT steps
    calls = {"k": 0}
    def counting(h, g, a, _o=orig, _c=calls):
        _c["k"] += 1
        return _o(h, g, a)
    ref._kkt_step = counting
    try:
        x, mult, budget_mult = ref._active_set(problem, rws)
    finally:
        ref._kkt_step = orig
    active_ineq = len(mult)
    nonzero = sum(1 for v in mult.values() if v != 0)
    stats.append((s, problem.n, calls["k"], nonzero, active_ineq))
print("seed n kkt_steps nonzero_inequality_multipliers working_set_size")
for row in stats:
    print(*row)
print("max kkt steps over seeds 0-49:", max(r[2] for r in stats))
print("n values:", sorted({r[1] for r in stats}))
print("seeds with a nonzero upper multiplier etc. (count of distinct nonzero-multiplier patterns):", len({r[3] for r in stats}))
