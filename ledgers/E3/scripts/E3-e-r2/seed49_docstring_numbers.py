"""Recompute the seed-49 standard errors quoted in test_standard_errors_match_the_delta_method_oracle (verifier E3-e r2).

Run from a scratch directory that holds elicit.py (= grader/reference.py), test_project.py and instance.py:
    QF_SEED=49 python -I seed49_docstring_numbers.py
Prints se_lambda and se_gamma from the observed information at steps 1e-5 and 1e-6, the relative changes, and the
change in se_lambda when the log-likelihood terms are summed in reverse order.
"""

import math

import test_project as t

est = t.est()
gamma, lam, kappa = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
theta = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]


def ses(parsed: list) -> dict[str, float]:
    def ll(th: list[float]) -> float:
        return t.oracle_loglik(parsed, 1.0 / (1.0 + math.exp(-th[0])), math.exp(th[1]), math.exp(th[2]))

    out: dict[str, float] = {}
    for h in (1e-5, 1e-6):
        cov = t._invert3(t._observed_information(theta, h))
        out[f"se_gamma@{h:g}"] = gamma * (1.0 - gamma) * math.sqrt(cov[0][0])
        out[f"se_lambda@{h:g}"] = lam * math.sqrt(cov[1][1])
    return out


base = ses(t.PARSED)
print("estimate gamma, lambda, kappa:", f"{gamma:.6f} {lam:.6f} {kappa:.6f}")
for k, v in base.items():
    print(k, f"{v:.5f}")
g5, g6 = base["se_gamma@1e-05"], base["se_gamma@1e-06"]
l5, l6 = base["se_lambda@1e-05"], base["se_lambda@1e-06"]
print("relative change se_lambda (1e-6 vs 1e-5):", f"{(l6 - l5) / l5 * 100:.2f}%")
print("relative change se_gamma (1e-6 vs 1e-5):", f"{(g6 - g5) / g5 * 100:.2f}%")
rev = ses(list(reversed(t.PARSED)))
print("reverse-order se_lambda@1e-05:", f"{rev['se_lambda@1e-05']:.5f}",
      "change:", f"{(rev['se_lambda@1e-05'] - l5) / l5 * 100:.2f}%")
print("reverse-order se_lambda@1e-06:", f"{rev['se_lambda@1e-06']:.5f}",
      "change:", f"{(rev['se_lambda@1e-06'] - l6) / l6 * 100:.2f}%")
