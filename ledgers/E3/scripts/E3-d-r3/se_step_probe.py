"""Round-3 probe: does an exact observed-information standard error pass the suite's SE oracle?

For seeds 0 to 49 the reference estimate is taken (grader/reference.py). The exact observed information is computed
with 60-digit Decimal arithmetic (central differences of step 1e-20, error O(h^2) = 1e-40), inverted, and carried to
the parameters by the coordinate-change derivatives, exactly as project.html line 214 and test_project.py:873-902
describe. For each seed and each step h in (1e-5, 1e-6) the suite's own oracle standard errors are recomputed in
float (copied from test_project.py, not imported), and the test's rule is applied: a seed passes when all three
standard errors of the candidate lie within 10 percent of the oracle values at one step.

Usage: .venv/bin/python ledgers/E3/scripts/E3-d-r3/se_step_probe.py [GRADER_DIR]
"""

from __future__ import annotations

import json
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

GRADER = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "course/modules/E/E3/grader"
sys.path.insert(0, str(GRADER))
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

getcontext().prec = 60
ONE = Decimal(1)


def parse(resp: dict) -> tuple:
    pa = [int(x) for x in resp["prizes_a"]]
    qa = [Fraction(str(s)) for s in resp["probs_a"]]
    pb = [int(x) for x in resp["prizes_b"]]
    qb = [Fraction(str(s)) for s in resp["probs_b"]]
    return pa, qa, pb, qb, str(resp["choice"])


# ---- float oracle, copied from test_project.py (oracle_loglik, _invert3, _observed_information)
def oracle_value(x: int, gamma: float, lam: float) -> float:
    if x >= 0:
        return math.pow(float(x), 1.0 - gamma)
    return -lam * math.pow(float(-x), 1.0 - gamma)


def oracle_prospect(prizes, probs, gamma, lam) -> float:
    total = sum(float(p) * oracle_value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))
    if total >= 0.0:
        return math.pow(total, 1.0 / (1.0 - gamma))
    return -math.pow(-total / lam, 1.0 / (1.0 - gamma))


def oracle_loglik(parsed, gamma, lam, kappa) -> float:
    total = 0.0
    for pa, qa, pb, qb, choice in parsed:
        z = kappa * (oracle_prospect(pa, qa, gamma, lam) - oracle_prospect(pb, qb, gamma, lam)) / 10_000.0
        total += -math.log1p(math.exp(-z)) if choice == "A" else -math.log1p(math.exp(z))
    return total


def invert3(m):
    aug = [list(row) + [1.0 if i == j else 0.0 for j in range(3)] for i, row in enumerate(m)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        div = aug[col][col]
        aug[col] = [x / div for x in aug[col]]
        for r in range(3):
            if r != col:
                factor = aug[r][col]
                aug[r] = [x - factor * y for x, y in zip(aug[r], aug[col], strict=True)]
    return [row[3:] for row in aug]


def observed_information_float(parsed, theta, h):
    def at(*moves):
        y = list(theta)
        for idx, amount in moves:
            y[idx] += amount
        gamma = 1.0 / (1.0 + math.exp(-y[0]))
        return oracle_loglik(parsed, gamma, math.exp(y[1]), math.exp(y[2]))

    f0 = at()
    info = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        info[i][i] = -(at((i, h)) - 2.0 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            value = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (
                4.0 * h * h
            )
            info[i][j] = info[j][i] = value
    return info


def oracle_se(parsed, gamma, lam, kappa, h):
    theta = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
    cov = invert3(observed_information_float(parsed, theta, h))
    if not all(cov[i][i] > 0.0 for i in range(3)):
        return None
    return {
        "se_gamma": gamma * (1.0 - gamma) * math.sqrt(cov[0][0]),
        "se_lambda": lam * math.sqrt(cov[1][1]),
        "se_kappa": kappa * math.sqrt(cov[2][2]),
    }


# ---- 60-digit Decimal observed information in (zeta, log lambda, log kappa)
def dec_loglik(parsed, c: Decimal, a: Decimal, b: Decimal) -> Decimal:
    gamma = ONE / (ONE + (-c).exp())
    lam = a.exp()
    kappa = b.exp()
    one_minus = ONE - gamma
    total = Decimal(0)
    for pa, qa, pb, qb, choice in parsed:
        ces = []
        for prizes, probs in ((pa, qa), (pb, qb)):
            v = Decimal(0)
            for x, p in zip(prizes, probs, strict=True):
                pd = Decimal(p.numerator) / Decimal(p.denominator)
                if x >= 0:
                    term = Decimal(x) ** one_minus if x > 0 else Decimal(0)
                else:
                    term = -lam * (Decimal(-x) ** one_minus)
                v += pd * term
            if v >= 0:
                ces.append(v ** (ONE / one_minus) if v > 0 else Decimal(0))
            else:
                ces.append(-((-v / lam) ** (ONE / one_minus)))
        z = kappa * (ces[0] - ces[1]) / Decimal(10000)
        total += -((ONE + (-z).exp()).ln()) if choice == "A" else -((ONE + z.exp()).ln())
    return total


def dec_observed_information(parsed, theta):
    h = Decimal("1e-20")
    c0, a0, b0 = (Decimal(t) for t in theta)
    pts = [c0, a0, b0]

    def f(moves):
        v = list(pts)
        for idx, amount in moves:
            v[idx] += amount
        return dec_loglik(parsed, v[0], v[1], v[2])

    f0 = f([])
    info = [[Decimal(0)] * 3 for _ in range(3)]
    for i in range(3):
        info[i][i] = -(f([(i, h)]) - 2 * f0 + f([(i, -h)])) / (h * h)
        for j in range(i + 1, 3):
            val = -(
                f([(i, h), (j, h)]) - f([(i, h), (j, -h)]) - f([(i, -h), (j, h)]) + f([(i, -h), (j, -h)])
            ) / (4 * h * h)
            info[i][j] = info[j][i] = val
    return info


def dec_invert3(m):
    aug = [list(row) + [ONE if i == j else Decimal(0) for j in range(3)] for i, row in enumerate(m)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        div = aug[col][col]
        aug[col] = [x / div for x in aug[col]]
        for r in range(3):
            if r != col:
                factor = aug[r][col]
                aug[r] = [x - factor * y for x, y in zip(aug[r], aug[col], strict=True)]
    return [row[3:] for row in aug]


def exact_se(parsed, est):
    gamma, lam, kappa = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
    theta = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
    info = dec_observed_information(parsed, theta)
    cov = dec_invert3(info)
    g = Decimal(repr(gamma))
    lm = Decimal(repr(lam))
    kp = Decimal(repr(kappa))
    return {
        "se_gamma": float(g * (ONE - g) * cov[0][0].sqrt()),
        "se_lambda": float(lm * cov[1][1].sqrt()),
        "se_kappa": float(kp * cov[2][2].sqrt()),
        "score_check": None,
    }


def passes(candidate, oracle_by_h):
    for h, want in oracle_by_h.items():
        if want is None:
            continue
        if all(abs(candidate[k] - want[k]) <= 1e-1 * want[k] for k in want):
            return True
    return False


def main() -> int:
    worst = []
    for seed in range(50):
        inst = make_instance(seed)
        responses = json.loads(str(inst["responses_json"]))
        parsed = [parse(r) for r in responses]
        est = ref.estimate(responses)
        oracles = {h: oracle_se(parsed, est["gamma_hat"], est["lambda_hat"], est["kappa_hat"], h) for h in (1e-5, 1e-6)}
        reference_ok = passes({k: est[k] for k in ("se_gamma", "se_lambda", "se_kappa")}, oracles)
        exact = exact_se(parsed, est)
        exact_ok = passes(exact, oracles)
        dev = {
            h: {k: round(100.0 * (exact[k] - want[k]) / want[k], 2) for k in want} for h, want in oracles.items() if want
        }
        line = {
            "seed": seed,
            "reference_pass": reference_ok,
            "exact_hessian_pass": exact_ok,
            "reference_se": {k: round(est[k], 6) for k in ("se_gamma", "se_lambda", "se_kappa")},
            "exact_se": {k: round(exact[k], 6) for k in ("se_gamma", "se_lambda", "se_kappa")},
            "exact_vs_oracle_percent": dev,
        }
        print(json.dumps(line))
        if not exact_ok:
            worst.append(seed)
    print(f"exact-Hessian candidate fails the suite's SE rule on seeds: {worst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
