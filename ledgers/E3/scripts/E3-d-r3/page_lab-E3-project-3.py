"""Rung 3 reference case: the estimates and standard errors for one fixed questionnaire of twelve SIMULATED answers.

Standard library only. The twelve answers are fixed SIMULATED data, printed here as data; this file does not record how
they were drawn, and the participant is not a real person. The estimates below are the numbers your elicit.py must
reproduce for this case (copy this file as run_case.py, then replace the estimate function with a call to your module;
it must print the same lines).

Each answer is (pair_id, choice, prizes of A, probabilities of A, prizes of B, probabilities of B). Prizes are whole
cents and probabilities are exact fractions, read with Fraction. The model is the prospect model of the
specification: gamma in (0, 1), lambda > 0, kappa > 0. Standard errors come from the observed information, the
negative Hessian of the log-likelihood in the coordinates (zeta, log lambda, log kappa),
zeta = log(gamma / (1 - gamma)), inverted and carried to the parameters by the derivative of each change of coordinates.
"""

import math
from fractions import Fraction

# (pair_id, choice, prizes of A, probabilities of A, prizes of B, probabilities of B)
ANSWERS: list[tuple[int, str, list[int], list[str], list[int], list[str]]] = [
    (0, "B", [6200, -15100], ["9/10", "1/10"], [3300, -3000, -700], ["1/20", "7/20", "3/5"]),
    (1, "B", [-9400, -10100, 19000], ["2/5", "3/10", "3/10"], [-12200, 17000, -1100], ["1/2", "1/4", "1/4"]),
    (2, "A", [10700, -3400, -13400], ["7/10", "1/10", "1/5"], [-14900, -13600, 15200], ["9/20", "2/5", "3/20"]),
    (3, "A", [18800, -12500], ["3/4", "1/4"], [16500, -17700], ["2/5", "3/5"]),
    (4, "B", [-10700, -5600, -7300], ["1/2", "2/5", "1/10"], [-13800, -9700], ["1/4", "3/4"]),
    (5, "B", [-11600, 7900, -12200], ["3/4", "1/10", "3/20"], [-12000, 11300], ["17/20", "3/20"]),
    (6, "A", [-9900, 5400, -4200], ["1/2", "1/4", "1/4"], [-15300, 16100, 6800], ["1/4", "1/2", "1/4"]),
    (7, "A", [600, -17500], ["3/5", "2/5"], [15800, -2600, -17600], ["2/5", "2/5", "1/5"]),
    (8, "B", [-10400, 13800], ["9/10", "1/10"], [10400, 1800], ["1/20", "19/20"]),
    (9, "B", [-17900, -12000, -3600], ["1/4", "1/4", "1/2"], [15600, 11600, -12200], ["3/10", "13/20", "1/20"]),
    (10, "B", [17000, 1600], ["1/10", "9/10"], [-18700, 3800], ["7/20", "13/20"]),
    (11, "B", [10400, -11300], ["2/5", "3/5"], [9300, 7200, -13200], ["1/2", "1/4", "1/4"]),
]


def value(x: float, gamma: float, lam: float) -> float:
    """Prospect value of a change x from 0: x^(1-gamma) for gains, -lam (-x)^(1-gamma) for losses."""
    if x >= 0.0:
        return math.pow(x, 1.0 - gamma)
    return -lam * math.pow(-x, 1.0 - gamma)


def certainty_equivalent(prizes: list[int], probs: list[str], gamma: float, lam: float) -> float:
    """The sure change whose prospect value equals the lottery's value, in cents, unrounded."""
    total = sum(float(Fraction(p)) * value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))
    if total >= 0.0:
        return math.pow(total, 1.0 / (1.0 - gamma))
    return -math.pow(-total / lam, 1.0 / (1.0 - gamma))


def log_likelihood(theta: list[float]) -> float:
    """The logit log-likelihood at theta = (zeta, log lambda, log kappa); each answer contributes log P(chosen)."""
    gamma = 1.0 / (1.0 + math.exp(-theta[0]))
    lam, kappa = math.exp(theta[1]), math.exp(theta[2])
    total = 0.0
    for _, choice, pa, qa, pb, qb in ANSWERS:
        z = kappa * (certainty_equivalent(pa, qa, gamma, lam) - certainty_equivalent(pb, qb, gamma, lam)) / 10_000.0
        total += -math.log1p(math.exp(-z)) if choice == "A" else -math.log1p(math.exp(z))
    return total


def grid_start() -> list[float]:
    """The best point of a small grid over gamma, lambda and kappa, used to start the search."""
    best = [0.0, 0.0, 0.0]
    best_value = log_likelihood(best)
    for gamma in (0.05, 0.25, 0.45, 0.65, 0.85):
        for lam in (1.0, 2.0, 4.0):
            for kappa in (0.5, 2.0, 5.0):
                start = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
                if log_likelihood(start) > best_value:
                    best, best_value = start, log_likelihood(start)
    return best


def second_order_search(theta: list[float]) -> list[float]:
    """A second-derivative search on the log-likelihood, with central differences of step 1e-6 and step halving."""
    h = 1e-6
    for _ in range(100):
        f0 = log_likelihood(theta)
        grad = [0.0, 0.0, 0.0]
        neg_hess = [[0.0] * 3 for _ in range(3)]
        for i in range(3):
            up = [x + (h if k == i else 0.0) for k, x in enumerate(theta)]
            down = [x - (h if k == i else 0.0) for k, x in enumerate(theta)]
            grad[i] = (log_likelihood(up) - log_likelihood(down)) / (2 * h)
            neg_hess[i][i] = -(log_likelihood(up) - 2 * f0 + log_likelihood(down)) / (h * h)
        for i in range(3):
            for j in range(i + 1, 3):
                pp = [x + (h if k in (i, j) else 0.0) for k, x in enumerate(theta)]
                pm = [x + (h if k == i else 0.0) - (h if k == j else 0.0) for k, x in enumerate(theta)]
                mp = [x - (h if k == i else 0.0) + (h if k == j else 0.0) for k, x in enumerate(theta)]
                mm = [x - (h if k in (i, j) else 0.0) for k, x in enumerate(theta)]
                neg_hess[i][j] = neg_hess[j][i] = -(
                    log_likelihood(pp) - log_likelihood(pm) - log_likelihood(mp) + log_likelihood(mm)
                ) / (4 * h * h)
        step = solve3(neg_hess, grad)
        scale = 1.0
        while scale > 1e-14 and log_likelihood([x + scale * d for x, d in zip(theta, step, strict=True)]) <= f0:
            scale /= 2.0
        if scale <= 1e-14:
            break
        theta = [x + scale * d for x, d in zip(theta, step, strict=True)]
        if max(abs(g) for g in grad) < 1e-7:
            break
    return theta


def solve3(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    """Solves a 3 by 3 linear system by Gaussian elimination with partial pivoting."""
    rows = [[*row, b] for row, b in zip(matrix, rhs, strict=True)]
    n = 3
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(rows[r][col]))
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(n):
            if r != col:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[col], strict=True)]
    return [rows[i][n] / rows[i][i] for i in range(n)]


def inverse3(matrix: list[list[float]]) -> list[list[float]]:
    """The inverse of a 3 by 3 matrix, column by column with solve3."""
    columns = [solve3(matrix, [1.0 if k == i else 0.0 for k in range(3)]) for i in range(3)]
    return [[columns[j][i] for j in range(3)] for i in range(3)]


def observed_information(theta: list[float]) -> list[list[float]]:
    """The negative Hessian of the log-likelihood at theta, by central differences of step 1e-5."""
    h = 1e-5
    f0 = log_likelihood(theta)
    info = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        up = [x + (h if k == i else 0.0) for k, x in enumerate(theta)]
        down = [x - (h if k == i else 0.0) for k, x in enumerate(theta)]
        info[i][i] = -(log_likelihood(up) - 2 * f0 + log_likelihood(down)) / (h * h)
    for i in range(3):
        for j in range(i + 1, 3):
            pp = [x + (h if k in (i, j) else 0.0) for k, x in enumerate(theta)]
            pm = [x + (h if k == i else 0.0) - (h if k == j else 0.0) for k, x in enumerate(theta)]
            mp = [x - (h if k == i else 0.0) + (h if k == j else 0.0) for k, x in enumerate(theta)]
            mm = [x - (h if k in (i, j) else 0.0) for k, x in enumerate(theta)]
            info[i][j] = info[j][i] = -(
                log_likelihood(pp) - log_likelihood(pm) - log_likelihood(mp) + log_likelihood(mm)
            ) / (4 * h * h)
    return info


def main() -> None:
    theta = second_order_search(grid_start())
    gamma = 1.0 / (1.0 + math.exp(-theta[0]))
    lam, kappa = math.exp(theta[1]), math.exp(theta[2])
    cov = inverse3(observed_information(theta))
    se_gamma = gamma * (1.0 - gamma) * math.sqrt(cov[0][0])
    se_lambda = lam * math.sqrt(cov[1][1])
    se_kappa = kappa * math.sqrt(cov[2][2])
    print("answers:", len(ANSWERS), "| mixed-sign answers:", sum(1 for a in ANSWERS if mixed_pair(a)))
    print("gamma_hat:", f"{gamma:.4f}", "| se_gamma:", f"{se_gamma:.2f}")
    print("lambda_hat:", f"{lam:.4f}", "| se_lambda:", f"{se_lambda:.2f}")
    print("kappa_hat:", f"{kappa:.4f}", "| se_kappa:", f"{se_kappa:.2f}")
    print("log-likelihood at the estimate:", f"{log_likelihood(theta):.4f}")
    print("largest score component at the estimate:", f"{largest_score(theta):.2e}")
    print("every parameter lies in its domain:", 0.0 < gamma < 1.0 and lam > 0.0 and kappa > 0.0)


def largest_score(theta: list[float]) -> float:
    """The largest absolute partial derivative of the log-likelihood at theta, in its three coordinates."""
    h = 1e-5
    values = []
    for i in range(3):
        up = [x + (h if k == i else 0.0) for k, x in enumerate(theta)]
        down = [x - (h if k == i else 0.0) for k, x in enumerate(theta)]
        values.append(abs(log_likelihood(up) - log_likelihood(down)) / (2 * h))
    return max(values)


def mixed_pair(answer: tuple[int, str, list[int], list[str], list[int], list[str]]) -> bool:
    """A question is mixed when one of its two lotteries has a gain and a loss, each with positive probability."""
    _, _, pa, qa, pb, qb = answer
    for prizes, probs in ((pa, qa), (pb, qb)):
        gain = any(x > 0 and Fraction(p) > 0 for x, p in zip(prizes, probs, strict=True))
        loss = any(x < 0 and Fraction(p) > 0 for x, p in zip(prizes, probs, strict=True))
        if gain and loss:
            return True
    return False


main()