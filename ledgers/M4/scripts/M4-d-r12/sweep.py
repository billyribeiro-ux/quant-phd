# Recomputes the grader-comment numbers (test_project.py lines 31-48) from reference.py and instance.py.
import sys, math, random, json
sys.path.insert(0, "/tmp/M4-d-r12-scratch/ws")
import importlib
sol = importlib.import_module("tail_risk")  # copy of reference.py
from instance import make_instance

def fsum_var(xs):
    m = math.fsum(xs) / len(xs)
    return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)

def sim_mode(pos, cov, n, seed, nu, mode):
    """mode: 'ref' = matched factor; 'nomatch' = sqrt(nu/W) (matched factor missing)."""
    n_a = len(pos)
    factor = sol._cholesky(cov, n_a)
    rng = random.Random(seed)
    matched = (nu - 2) / nu
    out = []
    for _ in range(n):
        z = [rng.gauss(0.0, 1.0) for _ in range(n_a)]
        chi = rng.gammavariate(nu / 2, 2.0)
        scale = math.sqrt(matched * nu / chi) if mode == "ref" else math.sqrt(nu / chi)
        total = 0.0
        for i in range(n_a):
            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))
            total += pos[i] * ret
        out.append(round(-total))
    return out

res = {"nu_counts": {}, "max_rel": {}, "seeds_fail_nomatch": {}, "seeds_total": {}, "seed1093": None}
rel_max = {}
fail_nm = {}
tot = {}
for seed in range(2000):
    inst = make_instance(seed)
    nu = inst["nu"]
    res["nu_counts"][nu] = res["nu_counts"].get(nu, 0) + 1
    if nu < 5:
        if seed == 1093:
            pos, cov, n = inst["positions_cents"], inst["cov"], inst["n_draws"]
            target = math.fsum(pos[i] * pos[j] * cov[i][j] for i in range(len(pos)) for j in range(len(pos)))
            v = fsum_var(sim_mode(pos, cov, n, seed, nu, "ref"))
            res["seed1093"] = {"nu": nu, "rel_err_matched": abs(v / target - 1), "n": n}
        continue
    pos, cov, n = inst["positions_cents"], inst["cov"], inst["n_draws"]
    target = math.fsum(pos[i] * pos[j] * cov[i][j] for i in range(len(pos)) for j in range(len(pos)))
    lr = sim_mode(pos, cov, n, seed, nu, "ref")
    rel = abs(fsum_var(lr) / target - 1)
    rel_max[nu] = max(rel_max.get(nu, 0.0), rel)
    tot[nu] = tot.get(nu, 0) + 1
    ln = sim_mode(pos, cov, n, seed, nu, "nomatch")
    rel_nm = abs(fsum_var(ln) / target - 1)
    fail_nm[nu] = fail_nm.get(nu, 0) + (1 if rel_nm > 0.30 else 0)
    if seed == 1093:
        pass
    if seed % 500 == 0:
        print("progress", seed, flush=True)
res["max_rel"] = {k: rel_max[k] for k in sorted(rel_max)}
res["seeds_fail_nomatch"] = {k: fail_nm[k] for k in sorted(fail_nm)}
res["seeds_total"] = {k: tot[k] for k in sorted(tot)}
print(json.dumps(res, indent=1))
