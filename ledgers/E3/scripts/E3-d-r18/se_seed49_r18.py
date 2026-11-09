"""Verifier probe (round 18): the oracle standard errors of seed 49 at steps 1e-5 and 1e-6 (test_project's own functions),
for the docstring numbers 135.05, 97.67, 0.09474, 0.07983. Usage (repo root): .venv/bin/python -I <this> <repo-root>"""

import math
import os
import shutil
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
work = Path(tempfile.mkdtemp(prefix="e3d-r18-se-"))
for f in ("test_project.py", "instance.py"):
    shutil.copy(root / "course/modules/E/E3/grader" / f, work)
shutil.copy(root / "course/modules/E/E3/grader/reference.py", work / "elicit.py")
sys.path.insert(0, str(work))
os.environ["QF_SEED"] = "49"
import test_project as tp  # noqa: E402

est = tp.est()
gamma, lam, kappa = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
theta = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
print(f"estimate gamma {gamma:.6f} lambda {lam:.4f} kappa {kappa:.4f}; reported se_gamma {est['se_gamma']:.5f} se_lambda {est['se_lambda']:.4f} se_kappa {est['se_kappa']:.4f}")
for h in (1e-5, 1e-6):
    cov = tp._invert3(tp._observed_information(theta, h))
    se_g = gamma * (1.0 - gamma) * math.sqrt(cov[0][0])
    se_l = lam * math.sqrt(cov[1][1])
    se_k = kappa * math.sqrt(cov[2][2])
    print(f"step {h:g}: oracle se_gamma {se_g:.5f} se_lambda {se_l:.4f} se_kappa {se_k:.4f}")
shutil.rmtree(work, ignore_errors=True)
