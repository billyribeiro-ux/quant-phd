"""Round-11: the fixed participants named on project.html:213 and test_project.py:36-37 (seeds 30 and 49), and the seed-0 and 7919 instances.
Prints the reference estimate, the generator's true values and the number of responses."""
import json
import sys
from pathlib import Path

work = Path(sys.argv[1])
sys.path.insert(0, str(work))
import elicit  # noqa: E402
from instance import make_instance  # noqa: E402

for seed in (0, 7919, 30, 49):
    inst = make_instance(seed)
    resp = json.loads(str(inst["responses_json"]))
    est = elicit.estimate(resp)
    print(f"seed {seed}: n={len(resp)} true gamma={float(inst['gamma']):.4f} lambda={float(inst['lambda']):.4f} kappa={float(inst['kappa']):.4f}"
          f" | reference gamma_hat={est['gamma_hat']:.4f} lambda_hat={est['lambda_hat']:.4f} kappa_hat={est['kappa_hat']:.4f}")
