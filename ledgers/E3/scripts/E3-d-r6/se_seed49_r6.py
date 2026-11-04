"""Recompute the seed-49 standard-error step sensitivity and the seed-30 kappa quoted in test_project.py's docstrings.

Run with: python -I se_seed49_r6.py <scratch dir holding elicit.py (reference) and instance.py (copies)>
"""
import json
import math
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1])
import elicit as sol  # noqa: E402  (reference implementation copy)
from instance import make_instance  # noqa: E402


def parse(r):
    return ([int(x) for x in r["prizes_a"]], [Fraction(s) for s in r["probs_a"]],
            [int(x) for x in r["prizes_b"]], [Fraction(s) for s in r["probs_b"]], r["choice"])


def value(x, g, lam):
    return math.pow(float(x), 1.0 - g) if x >= 0 else -lam * math.pow(float(-x), 1.0 - g)


def ce(prizes, probs, g, lam):
    tot = sum(float(p) * value(x, g, lam) for x, p in zip(prizes, probs, strict=True))
    return math.pow(tot, 1.0 / (1.0 - g)) if tot >= 0 else -math.pow(-tot / lam, 1.0 / (1.0 - g))


def loglik(parsed, g, lam, kappa, reverse=False):
    total = 0.0
    seq = list(reversed(parsed)) if reverse else parsed
    for pa, qa, pb, qb, choice in seq:
        z = kappa * (ce(pa, qa, g, lam) - ce(pb, qb, g, lam)) / 10000.0
        total += -math.log1p(math.exp(-z)) if choice == "A" else -math.log1p(math.exp(z))
    return total


def inv3(m):
    aug = [list(r) + [1.0 if i == j else 0.0 for j in range(3)] for i, r in enumerate(m)]
    for c in range(3):
        p = max(range(c, 3), key=lambda r: abs(aug[r][c]))
        aug[c], aug[p] = aug[p], aug[c]
        d = aug[c][c]
        aug[c] = [x / d for x in aug[c]]
        for r in range(3):
            if r != c:
                f = aug[r][c]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[c], strict=True)]
    return [row[3:] for row in aug]


def info(parsed, theta, h, reverse):
    def at(*moves):
        y = list(theta)
        for i, a in moves:
            y[i] += a
        return loglik(parsed, 1.0 / (1.0 + math.exp(-y[0])), math.exp(y[1]), math.exp(y[2]), reverse)
    f0 = at()
    m = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        m[i][i] = -(at((i, h)) - 2.0 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4.0 * h * h)
            m[i][j] = m[j][i] = v
    return m


inst = make_instance(49)
resp = json.loads(inst["responses_json"])
parsed = [parse(r) for r in resp]
est = sol.estimate(resp)
g, lam, kap = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
theta = [math.log(g / (1 - g)), math.log(lam), math.log(kap)]
print("seed 49 reference estimate:", {k: round(v, 6) for k, v in est.items()})
for reverse in (False, True):
    for h in (1e-5, 1e-6):
        cov = inv3(info(parsed, theta, h, reverse))
        se_g = g * (1 - g) * math.sqrt(cov[0][0])
        se_l = lam * math.sqrt(cov[1][1])
        se_k = kap * math.sqrt(cov[2][2])
        print(f"reverse={reverse} h={h:g}: se_gamma={se_g:.5f} se_lambda={se_l:.4f} se_kappa={se_k:.4f}")
print("seed 30 (LOW_KAPPA) kappa:", make_instance(30)["kappa"], "gamma:", make_instance(30)["gamma"])
print("seed 30 mixed-count check:", sum(1 for r in json.loads(make_instance(30)["responses_json"])
                                        if any(float(Fraction(p))>0 for p in r["probs_a"]) and False) )
