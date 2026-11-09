import sys
sys.path.insert(0, "/Users/billyribeiro/dev/quant-phd/ledgers/E3/scripts/E3-d-r15")
from sim_participants_r15 import sim
import reference as ref
# Targeted HIGH probe: low-noise participants (large kappa), gamma truth near 1, several seeds.
import itertools
res = {"converged": 0, "raised": 0, "max_gh_converged": 0.0, "max_gh_nondegenerate": 0.0, "above_0999_nondeg": 0}
for g, l, k, n, seed in itertools.product([0.95, 0.99, 0.999], [0.5, 1.0, 2.0, 3.0], [1.0, 5.0, 20.0, 100.0], [12, 26], range(1, 6)):
    recs = sim(seed, g, l, k, n)
    try:
        r = ref.estimate(recs)
    except Exception:
        res["raised"] += 1
        continue
    res["converged"] += 1
    gh = r["gamma_hat"]
    res["max_gh_converged"] = max(res["max_gh_converged"], gh)
    nondeg = r["kappa_hat"] < 1e4 and r["lambda_hat"] < 1e4
    if nondeg:
        res["max_gh_nondegenerate"] = max(res["max_gh_nondegenerate"], gh)
        if gh > 0.999:
            res["above_0999_nondeg"] += 1
print(res)
