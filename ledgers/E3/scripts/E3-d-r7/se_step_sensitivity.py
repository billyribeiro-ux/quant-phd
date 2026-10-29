"""Standard-error step sensitivity for seeds 0-49: oracle observed information at steps 1e-4, 1e-5, 1e-6, and the reference SE.

Run with: python3 -I se_step_sensitivity.py WORKDIR  (WORKDIR holds instance.py, test_project.py-equivalent oracles, elicit.py)
"""
import math
import sys

sys.path.insert(0, sys.argv[1])
from fractions import Fraction  # noqa: E402

import elicit as sol  # noqa: E402
from instance import make_instance  # noqa: E402
import json  # noqa: E402


def oracle_value(x, gamma, lam):
    if x >= 0:
        return math.pow(float(x), 1.0 - gamma)
    return -lam * math.pow(float(-x), 1.0 - gamma)


def oracle_prospect(prizes, probs, gamma, lam):
    total = sum(float(p) * oracle_value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))
    if total >= 0.0:
        return math.pow(total, 1.0 / (1.0 - gamma))
    return -math.pow(-total / lam, 1.0 / (1.0 - gamma))


def parse(r):
    return ([int(x) for x in r["prizes_a"]], [Fraction(str(s)) for s in r["probs_a"]],
            [int(x) for x in r["prizes_b"]], [Fraction(str(s)) for s in r["probs_b"]], str(r["choice"]))


def oracle_loglik(parsed, gamma, lam, kappa):
    total = 0.0
    for pa, qa, pb, qb, choice in parsed:
        z = kappa * (oracle_prospect(pa, qa, gamma, lam) - oracle_prospect(pb, qb, gamma, lam)) / 10_000.0
        total += -math.log1p(math.exp(-z)) if choice == "A" else -math.log1p(math.exp(z))
    return total


def info(parsed, theta, h):
    def at(*moves):
        y = list(theta)
        for idx, amt in moves:
            y[idx] += amt
        g = 1.0 / (1.0 + math.exp(-y[0]))
        return oracle_loglik(parsed, g, math.exp(y[1]), math.exp(y[2]))
    f0 = at()
    m = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        m[i][i] = -(at((i, h)) - 2 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4 * h * h)
            m[i][j] = m[j][i] = v
    return m


def invert3(m):
    aug = [list(r) + [1.0 if i == j else 0.0 for j in range(3)] for i, r in enumerate(m)]
    for col in range(3):
        piv = max(range(col, 3), key=lambda r: abs(aug[r][col]))
        aug[col], aug[piv] = aug[piv], aug[col]
        d = aug[col][col]
        aug[col] = [x / d for x in aug[col]]
        for r in range(3):
            if r != col:
                f = aug[r][col]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[col], strict=True)]
    return [row[3:] for row in aug]


worst = {"se_gamma": 0.0, "se_lambda": 0.0, "se_kappa": 0.0}
rows = []
for seed in range(50):
    inst = make_instance(seed)
    resp = json.loads(inst["responses_json"])
    parsed = [parse(r) for r in resp]
    est = sol.estimate(resp)
    g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
    theta = [math.log(g / (1 - g)), math.log(l), math.log(k)]
    se = {}
    for h in (1e-4, 1e-5, 1e-6):
        cov = invert3(info(parsed, theta, h))
        se[h] = {
            "se_gamma": g * (1 - g) * math.sqrt(cov[0][0]),
            "se_lambda": l * math.sqrt(cov[1][1]),
            "se_kappa": k * math.sqrt(cov[2][2]),
        }
    for key in worst:
        ref = est[key]
        for h in (1e-4, 1e-6):
            rel = abs(se[h][key] - se[1e-5][key]) / se[1e-5][key]
            if rel > worst[key]:
                worst[key] = rel
    rel16 = {key: abs(se[1e-6][key] - se[1e-5][key]) / se[1e-5][key] for key in worst}
    rel_ref = {key: abs(est[key] - se[1e-5][key]) / se[1e-5][key] for key in worst}
    rows.append((seed, rel16, rel_ref, est["se_lambda"]))
for seed, r16, rref, sel in rows:
    if seed in (0, 49) or max(r16.values()) > 0.05:
        print(f"seed {seed}: |se(1e-6)-se(1e-5)|/se(1e-5) = " + ", ".join(f"{k}={v:.4f}" for k, v in r16.items())
              + " | |ref-oracle(1e-5)|/oracle = " + ", ".join(f"{k}={v:.2e}" for k, v in rref.items()))
print("max over seeds 0-49 of step-1e-6 vs step-1e-5 relative SE difference:", {k: round(max(r[1][k] for r in rows), 4) for k in worst})
print("seeds with a 10% or larger step difference in any SE:", [r[0] for r in rows if max(r[1].values()) >= 0.10])
print("max reference-vs-oracle relative SE difference:", {k: f"{max(r[2][k] for r in rows):.2e}" for k in worst})
