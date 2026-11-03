"""Round-3 verifier D: sample 20 seeds of grader/instance.py (seeds 0..19 and 1000..1019): every instance valid, instances differ."""
import math, sys
sys.path.insert(0, sys.argv[1] + "/course/modules/M/M4/grader")
import instance
seeds = list(range(20)) + list(range(1000, 1020))
ok = 0
answers = set()
for s in seeds:
    i = instance.make_instance(s)
    pos, cov, nd, nu = i["positions_cents"], i["cov"], i["n_draws"], i["nu"]
    valid = (2 <= len(pos) <= 3 and all(type(w) is int and w > 0 for w in pos) and 3 <= nu <= 8
             and nd <= 20000 and nd % 100 != 0 and i["label"] == "SIMULATED"
             and all(abs(cov[a][b] - cov[b][a]) == 0 for a in range(len(cov)) for b in range(len(cov))))
    # positive definite: leading pivots positive (Cholesky)
    n = len(cov)
    L = [[0.0] * n for _ in range(n)]
    pd = True
    for a in range(n):
        for b in range(a + 1):
            inner = sum(L[a][k] * L[b][k] for k in range(b))
            if a == b:
                piv = cov[a][a] - inner
                if piv <= 0:
                    pd = False
                L[a][a] = math.sqrt(piv) if piv > 0 else 0.0
            else:
                L[a][b] = (cov[a][b] - inner) / L[b][b] if L[b][b] else 0.0
    valid = valid and pd
    ok += valid
    answers.add((tuple(pos), nu, nd))
print(f"valid instances: {ok}/{len(seeds)}; distinct (positions, nu, n_draws) triples: {len(answers)}")
