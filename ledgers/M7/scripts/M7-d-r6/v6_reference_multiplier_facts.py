"""Round 6 (M7-d): facts about the reference's multipliers on seeds 0-49 and the hand cases, used for the equivalence
argument on the two candidate mutants v6_01 (floor removed) and v6_02 (turnover multipliers left out of the dual).

Prints, per case: the minimum inequality multiplier (exact), whether lower_i and upper_i are both non-zero for some i,
and whether any turnover multiplier is negative. Stdlib + the reference module, run with -I."""

import sys
from fractions import Fraction as F

sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402
import json  # noqa: E402

def facts(case, label):
    p = ref._parse(case)
    sol = ref._solve(p)
    ineq = [*sol["lower"], *sol["upper"], *sol["sector"], *sol["plus"], *sol["minus"], sol["kappa"]]
    both = any(sol["lower"][i] != 0 and sol["upper"][i] != 0 for i in range(p.n))
    neg_turn = any(v < 0 for v in [*sol["plus"], *sol["minus"], sol["kappa"]])
    return min(ineq), both, neg_turn

minima = {}
both_any = False
neg_any = False
for seed in range(50):
    case = json.loads(make_instance(seed)["payload"])
    m, both, neg = facts(case, seed)
    minima[str(m)] = minima.get(str(m), 0) + 1
    both_any |= both
    neg_any |= neg
print("seeds 0-49: minimum inequality multiplier values (count):", minima)
print("seeds 0-49: some asset with lower and upper multipliers both nonzero:", both_any)
print("seeds 0-49: some turnover multiplier negative:", neg_any)
