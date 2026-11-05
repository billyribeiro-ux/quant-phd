"""Round-11 verifier d: validity and variety of grader/instance.py over 20 sampled seeds (0-19) plus 20 others, and the
answers the reference gives (the Gaussian 99% loss at each seed's draws, 2000 draws, for the 'answers change' check)."""

import importlib.util
import math
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("instance", ROOT / "course/modules/M/M4/grader/instance.py")
inst = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inst)
ref_spec = importlib.util.spec_from_file_location("ref", ROOT / "course/modules/M/M4/grader/reference.py")
ref = importlib.util.module_from_spec(ref_spec)
ref_spec.loader.exec_module(ref)
SEEDS = list(range(20)) + [1093, 777, 2026, 2027, 314159, 271828, 99991, 424242, 1000003, 65537,
                           7, 13, 42, 100, 500, 999, 1500, 1999, 12345, 54321]
DRAWS = {6_003, 8_001, 9_997, 12_011, 15_013, 19_987}
sigs = set()
bad = []
answers = []
for s in SEEDS:
    i = inst.make_instance(s)
    n = i["n_assets"]
    pos, cov = i["positions_cents"], i["cov"]
    ok = (n in (2, 3) and len(pos) == n and all(type(w) is int and 100_000 <= w <= 5_000_000 for w in pos)
          and all(cov[a][b] == cov[b][a] for a in range(n) for b in range(n))
          and 3 <= i["nu"] <= 8 and i["n_draws"] in DRAWS and i["n_draws"] % 100 != 0 and i["label"] == "SIMULATED")
    try:
        ref._cholesky(cov, n)
    except ValueError:
        ok = False
    if not ok:
        bad.append(s)
    sigs.add((n, tuple(pos), i["nu"], i["n_draws"]))
    losses = ref.simulate_losses(pos, cov, 2000, 2026, "gaussian", None)
    answers.append(ref.quantile_99(losses))
print("seeds checked:", len(SEEDS), "invalid:", bad)
print("distinct (n, positions, nu, draws) tuples:", len(sigs))
print("distinct 99% losses over the seeds (2000 draws each, seed 2026):", len(set(answers)))
print("distinct (n_assets, nu, n_draws) combinations over seeds 0-199:",
      len({(inst.make_instance(s)["n_assets"], inst.make_instance(s)["nu"], inst.make_instance(s)["n_draws"]) for s in range(200)}))
