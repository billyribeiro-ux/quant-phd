"""Round-6 verifier (slice d): sample seeds 0..19 of grader/instance.py; check validity and that answers differ.

Validity: positions are whole cents in [100000, 5000000] and all positive; cov is square, symmetric, with positive
Cholesky pivots; nu in 3..8; n_draws <= 20000 and not a multiple of 100. Materiality: the Gaussian 99% loss from the
reference at each seed (reference.simulate_losses, quantile_99) and the seed's first position differ across seeds.
"""
import sys
from pathlib import Path

GRADER = Path(__file__).resolve().parents[4] / "course" / "modules" / "M" / "M4" / "grader"
sys.path.insert(0, str(GRADER))
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

rows = []
for seed in range(20):
    inst = make_instance(seed)
    pos, cov, nu, n = inst["positions_cents"], inst["cov"], inst["nu"], inst["n_draws"]
    assert all(type(p) is int and 100_000 <= p <= 5_000_000 for p in pos), seed
    k = len(pos)
    assert all(len(r) == k for r in cov) and all(cov[i][j] == cov[j][i] for i in range(k) for j in range(k)), seed
    ref._cholesky(cov, k)  # raises if not positive definite
    assert 3 <= nu <= 8 and n <= 20000 and n % 100 != 0, seed
    q = ref.quantile_99(ref.simulate_losses(pos, cov, n, seed, "gaussian", None))
    rows.append((seed, k, nu, n, pos[0], q))
    print(f"seed {seed:2d} assets {k} nu {nu} n_draws {n:6d} pos0 {pos[0]:8d} gaussian_99_loss_cents {q}")
print("distinct gaussian 99% losses over seeds 0..19:", len({r[5] for r in rows}), "of 20")
print("distinct first positions:", len({r[4] for r in rows}), "of 20")
print("all 20 instances valid: True")
