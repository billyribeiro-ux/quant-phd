"""Searches low-noise simulated participants (gamma truth 0.99 to 0.999) for converged, non-degenerate fits with
gamma_hat in (0.99, 0.999), using the pinned reference. Usage: high_side_check.py (run from the checkout root)."""
import itertools, sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "course/modules/E/E3/grader"))
sys.path.insert(0, os.path.join(os.getcwd(), "ledgers/E3/scripts/E3-d-r15/verifier"))
from sim_pinned import sim
import reference as ref
hits, conv, raised = [], 0, 0
for g, l, k, n, seed in itertools.product([0.99, 0.999], [0.5, 1.0, 2.0], [1.0, 5.0, 20.0, 100.0], [12, 26], range(1, 4)):
    try:
        r = ref.estimate(sim(seed, g, l, k, n))
    except Exception:
        raised += 1
        continue
    conv += 1
    if 0.99 < r["gamma_hat"] < 0.999 and r["kappa_hat"] < 1e4 and r["lambda_hat"] < 1e4:
        hits.append((round(r["gamma_hat"], 6), g, l, k, n, seed, round(r["lambda_hat"], 3), round(r["kappa_hat"], 3)))
print("converged", conv, "raised", raised, "nondegenerate fits with 0.99 < gamma_hat < 0.999:", len(hits))
for h in hits[:6]:
    print(h)
