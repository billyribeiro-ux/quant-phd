"""Recomputes the seed-49 standard errors quoted in the grader docstring (test_project.py:876-887), round-5 verifier.

Imports the suite's own oracle helpers from a scratch workspace holding test_project.py, instance.py and elicit.py
(the reference, copied), with QF_SEED=49. Run from that workspace: QF_SEED=49 python -I <this file>.
"""
import math
import sys
import os
sys.path.insert(0, os.path.abspath("."))
import test_project as t  # noqa: E402

gamma, lam, kappa = t.est()["gamma_hat"], t.est()["lambda_hat"], t.est()["kappa_hat"]
theta = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
for h in (1e-5, 1e-6):
    cov = t._invert3(t._observed_information(theta, h))
    se_g = gamma * (1 - gamma) * math.sqrt(cov[0][0])
    se_l = lam * math.sqrt(cov[1][1])
    print("step", h, "se_gamma", f"{se_g:.5f}", "se_lambda", f"{se_l:.2f}", "se_kappa", f"{kappa * math.sqrt(cov[2][2]):.4f}")

# reverse order of the likelihood terms (the docstring's reverse-order figures)
t.PARSED[:] = t.PARSED[::-1]
for h in (1e-5, 1e-6):
    cov = t._invert3(t._observed_information(theta, h))
    print("reverse order step", h, "se_lambda", f"{lam * math.sqrt(cov[1][1]):.2f}")
print("pct lambda 1e-5 forward->reverse:", f"{(136.78/135.05-1)*100:.2f}", "(from docstring values)")
