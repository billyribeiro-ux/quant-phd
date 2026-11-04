"""Re-derive the seed-49 standard errors quoted in the docstring of test_standard_errors_match_the_coordinate_change_oracle
(grader/test_project.py, round 5), using the suite's own oracle functions with QF_SEED=49 and the reference solution.

Run from a scratch directory that holds elicit.py (= grader/reference.py), instance.py and test_project.py copies:
    QF_SEED=49 python -I seed49_se_r5.py
"""

import math
import os
import sys

sys.path.insert(0, os.getcwd())
import test_project as tp  # noqa: E402

est = tp.est()
gamma, lam, kappa = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
theta = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
print("seed", os.environ["QF_SEED"], "gamma", round(gamma, 6), "lambda", round(lam, 6), "kappa", round(kappa, 6))
for h in (1e-5, 1e-6):
    cov = tp._invert3(tp._observed_information(theta, h))
    se_g = gamma * (1 - gamma) * math.sqrt(cov[0][0])
    se_l = lam * math.sqrt(cov[1][1])
    se_k = kappa * math.sqrt(cov[2][2])
    print(f"step {h:g}: se_gamma {se_g:.5f} se_lambda {se_l:.2f} se_kappa {se_k:.4f}")
