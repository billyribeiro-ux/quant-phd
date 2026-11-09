"""Seed-49 (LARGE_LAMBDA) standard errors by the test's oracle at steps 1e-5 and 1e-6, forward and reverse summation."""
import ast
import json
import math
import sys
from pathlib import Path

GRADER = Path("/Users/billyribeiro/dev/quant-phd/course/modules/E/E3/grader")
sys.path.insert(0, str(GRADER))
import reference as sol  # noqa: E402
from instance import make_instance  # noqa: E402

resp = json.loads(str(make_instance(49)["responses_json"]))
fit = sol.estimate(resp)
gamma, lam, kappa = fit["gamma_hat"], fit["lambda_hat"], fit["kappa_hat"]
print("estimate", gamma, lam, kappa)


def parse(r):
    from fractions import Fraction
    return ([int(x) for x in r["prizes_a"]], [Fraction(str(s)) for s in r["probs_a"]],
            [int(x) for x in r["prizes_b"]], [Fraction(str(s)) for s in r["probs_b"]], str(r["choice"]))


def oracle_prospect(prizes, probs, g, l):
    def val(x):
        return math.pow(float(x), 1.0 - g) if x >= 0 else -l * math.pow(float(-x), 1.0 - g)
    total = sum(float(p) * val(x) for x, p in zip(prizes, probs, strict=True))
    if total >= 0.0:
        return math.pow(total, 1.0 / (1.0 - g))
    return -math.pow(-total / l, 1.0 / (1.0 - g))


def loglik(parsed, g, l, k, order):
    total = 0.0
    seq = parsed if order == "fwd" else list(reversed(parsed))
    for pa, qa, pb, qb, ch in seq:
        z = k * (oracle_prospect(pa, qa, g, l) - oracle_prospect(pb, qb, g, l)) / 10_000.0
        total += -math.log1p(math.exp(-z)) if ch == "A" else -math.log1p(math.exp(z))
    return total


def info(theta, h, parsed, order):
    def at(*moves):
        y = list(theta)
        for idx, amt in moves:
            y[idx] += amt
        return loglik(parsed, 1.0 / (1.0 + math.exp(-y[0])), math.exp(y[1]), math.exp(y[2]), order)
    f0 = at()
    m = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        m[i][i] = -(at((i, h)) - 2 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4 * h * h)
            m[i][j] = m[j][i] = v
    return m


def invert3(m):
    import numpy as np
    return np.linalg.inv(np.array(m)).tolist()


parsed = [parse(r) for r in resp]
theta = [math.log(gamma / (1 - gamma)), math.log(lam), math.log(kappa)]
for order in ("fwd", "rev"):
    for h in (1e-5, 1e-6):
        cov = invert3(info(theta, h, parsed, order))
        se_g = gamma * (1 - gamma) * math.sqrt(cov[0][0])
        se_l = lam * math.sqrt(cov[1][1])
        se_k = kappa * math.sqrt(cov[2][2])
        print(order, "h", h, "se_gamma %.5f se_lambda %.4f se_kappa %.5f" % (se_g, se_l, se_k))
print("reference se", {k: round(fit[k], 5) for k in ("se_gamma", "se_lambda", "se_kappa")})
