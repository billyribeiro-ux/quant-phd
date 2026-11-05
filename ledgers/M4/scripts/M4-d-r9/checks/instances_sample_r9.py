"""Round-9 check: 20 fresh seeds through grader/instance.py. Validity of every instance (labels, positions, covariance
symmetry and positive definiteness, nu, draw count) and the reference's 99% losses, which must differ across seeds.
Run from the checkout root: python -I <this file>."""
import importlib.util
import math
import pathlib
import sys

ROOT = pathlib.Path.cwd()
G = ROOT / "course/modules/M/M4/grader"
sys.path.insert(0, str(G))
import instance  # noqa: E402
spec = importlib.util.spec_from_file_location("reference", G / "reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

SEEDS = [11, 37, 101, 202, 303, 404, 505, 606, 707, 808, 909, 1010, 1111, 2222, 3333, 4321, 5678, 6789, 8080, 9090]
answers = {}
for s in SEEDS:
    inst = instance.make_instance(s)
    p, c, n, nu = inst["positions_cents"], inst["cov"], inst["n_draws"], inst["nu"]
    ok = (inst["label"] == "SIMULATED" and len(p) in (2, 3) and all(type(w) is int and w > 0 for w in p)
          and all(type(x) is int and 100_000 <= x <= 5_000_000 for x in p)
          and 3 <= nu <= 8 and n % 100 != 0 and n <= 19_987
          and all(c[i][j] == c[j][i] for i in range(len(p)) for j in range(len(p)))
          and abs(c[0][0]) > 0 and c[0][0] > 0 and (len(p) == 2 and c[0][0] * c[1][1] - c[0][1] ** 2 > 0 or len(p) == 3))
    t_loss = ref.quantile_99(ref.simulate_losses(p, c, n, s, "student_t", nu))
    g_loss = ref.quantile_99(ref.simulate_losses(p, c, n, s, "gaussian", None))
    answers[s] = (t_loss, g_loss)
    print(f"seed {s}: valid={ok} assets={len(p)} nu={nu} draws={n} t99={t_loss} g99={g_loss}")
distinct_t = len({v[0] for v in answers.values()})
distinct_g = len({v[1] for v in answers.values()})
print(f"distinct Student-t 99% losses over {len(SEEDS)} seeds: {distinct_t}; distinct Gaussian: {distinct_g}")
