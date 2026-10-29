"""Re-derive the grader's tolerance-comment sweep (seeds 0-1999) with the reference and an unmatched variant.

Unmatched variant: simulate_losses(pos, cov * nu/(nu-2), ...) reproduces a draw with no matched factor, because
sqrt((nu-2)/nu) * sqrt(nu/(nu-2)) = 1. Run with the scratch directory holding reference.py as tail_risk.py.
"""
import sys
sys.path.insert(0, "/tmp/M4-d-r6-scratch")
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyB6-M4-d/course/modules/M/M4/grader")
import math, time
import tail_risk as sol
from instance import make_instance

TOL = 0.30
def sample_variance(xs):
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)

def rel(losses, target):
    return abs(sample_variance(losses) / target - 1.0)

start = time.time()
seeds = range(int(sys.argv[1]), int(sys.argv[2]))
maxrel = {}
count = {}
unmatched_fail = {}
unmatched_total = {}
seed1093 = None
for seed in seeds:
    inst = make_instance(seed)
    pos, cov, nu, n = inst["positions_cents"], inst["cov"], inst["nu"], inst["n_draws"]
    target = math.fsum(pos[i] * pos[j] * cov[i][j] for i in range(len(pos)) for j in range(len(pos)))
    matched = sol.simulate_losses(pos, cov, n, seed, "student_t", nu)
    r = rel(matched, target)
    count[nu] = count.get(nu, 0) + 1
    maxrel[nu] = max(maxrel.get(nu, 0.0), r)
    if nu == 3 and seed == 1093:
        seed1093 = r
    if nu >= 5:
        f = nu / (nu - 2)
        cov_u = [[c * f for c in row] for row in cov]
        unm = sol.simulate_losses(pos, cov_u, n, seed, "student_t", nu)
        unmatched_total[nu] = unmatched_total.get(nu, 0) + 1
        if rel(unm, target) > TOL:
            unmatched_fail[nu] = unmatched_fail.get(nu, 0) + 1
print("seeds", seeds, "elapsed %.1f s" % (time.time() - start))
for nu in sorted(count):
    print("nu", nu, "seeds", count[nu], "max matched rel err %.4f" % maxrel[nu])
print("seed 1093 nu 3 matched rel err: %.4f (tolerance %.2f)" % (seed1093, TOL) if seed1093 is not None else "seed 1093 nu!=3")
for nu in sorted(unmatched_total):
    print("nu", nu, "unmatched fails", unmatched_fail.get(nu, 0), "of", unmatched_total[nu])
