"""Round-10 verifier facts for E3-d: seed-level numbers quoted in project.html and test_project.py docstrings."""
import json
import math
import sys
from fractions import Fraction

sys.path.insert(0, "/tmp/E3d_r10_ws/ref")
import elicit as ref  # noqa: E402  (the reference solution, copied as elicit.py)
from instance import make_instance  # noqa: E402

GRADER = "/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/course/modules/E/E3/grader"


def parse(r):
    return ([int(x) for x in r["prizes_a"]], [Fraction(s) for s in r["probs_a"]],
            [int(x) for x in r["prizes_b"]], [Fraction(s) for s in r["probs_b"]], r["choice"])


def oracle_value(x, g, l):
    return math.pow(float(x), 1.0 - g) if x >= 0 else -l * math.pow(float(-x), 1.0 - g)


def oracle_prospect(pr, pb, g, l):
    total = sum(float(p) * oracle_value(x, g, l) for x, p in zip(pr, pb, strict=True))
    return math.pow(total, 1.0 / (1.0 - g)) if total >= 0 else -math.pow(-total / l, 1.0 / (1.0 - g))


def oracle_loglik(parsed, g, l, k):
    t = 0.0
    for pa, qa, pb, qb, ch in parsed:
        z = k * (oracle_prospect(pa, qa, g, l) - oracle_prospect(pb, qb, g, l)) / 10_000.0
        t += -math.log1p(math.exp(-z)) if ch == "A" else -math.log1p(math.exp(z))
    return t


def se_at(parsed, theta, h):
    def at(*moves):
        y = list(theta)
        for i, a in moves:
            y[i] += a
        g = 1.0 / (1.0 + math.exp(-y[0]))
        return oracle_loglik(parsed, g, math.exp(y[1]), math.exp(y[2]))
    f0 = at()
    info = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        info[i][i] = -(at((i, h)) - 2 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4 * h * h)
            info[i][j] = info[j][i] = v
    # invert 3x3 by Gauss-Jordan
    aug = [list(r) + [1.0 if i == j else 0.0 for j in range(3)] for i, r in enumerate(info)]
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


def report(seed):
    inst = make_instance(seed)
    resp = json.loads(inst["responses_json"])
    fit = ref.estimate(resp)
    parsed = [parse(r) for r in resp]
    print(f"seed {seed}: true gamma={inst['gamma']} lambda={inst['lambda']} kappa={inst['kappa']} wealth={inst['wealth_cents']}")
    print("  fit:", {k: round(v, 6) for k, v in fit.items()})
    return inst, fit, parsed


if __name__ == "__main__":
    # seed 49: docstring numbers
    inst, fit, parsed = report(49)
    g, l, k = fit["gamma_hat"], fit["lambda_hat"], fit["kappa_hat"]
    theta = [math.log(g / (1 - g)), math.log(l), math.log(k)]
    for h in (1e-5, 1e-6):
        cov = se_at(parsed, theta, h)
        se = {
            "se_gamma": g * (1 - g) * math.sqrt(cov[0][0]),
            "se_lambda": l * math.sqrt(cov[1][1]),
            "se_kappa": k * math.sqrt(cov[2][2]),
        }
        print(f"  step {h:g}: ", {kk: round(vv, 5) for kk, vv in se.items()})
    # reverse-order summation effect on se_lambda (docstring: 135.05 -> 136.78 at 1e-5; 97.67 -> 98.09 at 1e-6)
    rev = list(reversed(parsed))
    for h in (1e-5, 1e-6):
        cov = se_at(rev, theta, h)
        print(f"  reverse order step {h:g}: se_lambda", round(l * math.sqrt(cov[1][1]), 5),
              "se_gamma", round(g * (1 - g) * math.sqrt(cov[0][0]), 5))
    print("  lambda_hat > 10:", l > 10, "| lambda_hat", round(l, 4))
    # seed 30
    inst30, fit30, _ = report(30)
    print("  seed 30 kappa_hat", round(fit30["kappa_hat"], 5), "< 1:", fit30["kappa_hat"] < 1)
