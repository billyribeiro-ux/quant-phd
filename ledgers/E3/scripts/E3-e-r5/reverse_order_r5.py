"""Reverse-order summation check for the seed-49 standard errors quoted in the grader docstring."""
import math
import os
import sys

sys.path.insert(0, os.getcwd())
import test_project as tp  # noqa: E402

est = tp.est()
gamma, lam, kappa = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
theta = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
forward = list(tp.PARSED)
tp.PARSED[:] = list(reversed(forward))
for h in (1e-5, 1e-6):
    cov = tp._invert3(tp._observed_information(theta, h))
    se_l = lam * math.sqrt(cov[1][1])
    print(f"reverse order, step {h:g}: se_lambda {se_l:.2f}")
tp.PARSED[:] = forward
