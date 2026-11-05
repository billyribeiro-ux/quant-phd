"""Round-10 verifier D: sample 20 fresh seeds (not 0-49) and check each make_instance output is valid under project.html
(2 or 3 positive whole-cent positions, 100,000 to 5,000,000 cents; symmetric positive-definite covariance with positive pivots;
nu in 3..8; draw count not a multiple of 100 and at most 20,000), and that the reference's Gaussian 99% loss differs across the
sampled seeds (the answers change, not only the labels). Also prints the number of distinct nu and n_assets values over seeds 0-199."""

import math
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD10-M4-d")
sys.path.insert(0, str(ROOT / "course/modules/M/M4/grader"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import instance  # noqa: E402
import cross_term_d10 as ct  # noqa: E402

SEEDS = [3, 17, 29, 41, 58, 73, 88, 101, 150, 222, 333, 404, 512, 640, 777, 818, 901, 1000, 1234, 1500]
ref = ct.load(ct.REF, "ref")
rows = []
for s in SEEDS:
    inst = instance.make_instance(s)
    pos, cov, nu, n = inst["positions_cents"], inst["cov"], inst["nu"], inst["n_draws"]
    ok_pos = all(type(w) is int and 100_000 <= w <= 5_000_000 for w in pos) and len(pos) in (2, 3)
    ok_cov = all(cov[i][j] == cov[j][i] for i in range(len(cov)) for j in range(len(cov)))
    # Cholesky pivots, computed independently here (float, row by row)
    m = len(cov)
    L = [[0.0] * m for _ in range(m)]
    pivots_ok = True
    for i in range(m):
        for j in range(i + 1):
            acc = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                piv = cov[i][i] - acc
                pivots_ok &= piv > 0
                L[i][i] = math.sqrt(piv) if piv > 0 else 0.0
            else:
                L[i][j] = (cov[i][j] - acc) / L[j][j]
    ok_nu = 3 <= nu <= 8
    ok_n = n % 100 != 0 and n <= 20_000 and n in (6003, 8001, 9997, 12011, 15013, 19987)
    losses = ref.simulate_losses(pos, cov, 2000, s, "gaussian", None)
    q = ref.quantile_99(losses)
    rows.append((s, len(pos), nu, n, ok_pos and ok_cov and pivots_ok and ok_nu and ok_n, q))
    print(f"seed {s}: positions {len(pos)} nu {nu} draws {n} valid {ok_pos and ok_cov and pivots_ok and ok_nu and ok_n} "
          f"cov_symmetric {ok_cov} pivots_positive {pivots_ok} gaussian 99% loss (2000 draws) {q} cents")
print("all valid:", all(r[4] for r in rows), "| distinct gaussian 99% losses among 20 seeds:", len({r[5] for r in rows}))
distinct = {(instance.make_instance(s)["n_assets"], instance.make_instance(s)["nu"]) for s in range(200)}
print("distinct (n_assets, nu) pairs over seeds 0-199:", len(distinct), "| n_assets values:", sorted({a for a, _ in distinct}), "| nu values:", sorted({b for _, b in distinct}))
sys.stdout.flush()
