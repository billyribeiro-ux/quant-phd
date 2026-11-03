"""Independent check of the Lab 3 reference-case numbers quoted on project.html (round 4, slice e).

Re-derives the twelve answers from the page's ANSWERS block (read from project.html, not imported from the twin),
the certainty equivalents with exact Fractions for the probabilities, and the maximum-likelihood estimate by
scipy Nelder-Mead from several starts. Prints the quantities the page quotes: estimates, standard errors (observed
information by central differences, delta method), log-likelihood, the mixed-pair count, the prize range, the number
of prizes per lottery, and the pure pairs.
Usage: python3 -I lab3_exemplar_check.py <checkout>
"""
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

root = Path(sys.argv[1])
page = (root / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
block = page[page.index("ANSWERS: list"):]
block = block[: block.index("\n]\n") + 3]
rows = re.findall(r"\((\d+), \"([AB])\", \[([^\]]*)\], \[([^\]]*)\], \[([^\]]*)\], \[([^\]]*)\]\)", block)
answers = []
for pid, ch, pa, qa, pb, qb in rows:
    f = lambda s: [int(x) for x in s.split(",") if x.strip()]  # noqa: E731
    g = lambda s: [Fraction(x.strip().strip('"')) for x in s.split(",") if x.strip()]  # noqa: E731
    answers.append((int(pid), ch, f(pa), g(qa), f(pb), g(qb)))
assert len(answers) == 12, len(answers)
for _, _, pa, qa, pb, qb in answers:
    assert sum(qa) == 1 and sum(qb) == 1


def value(x: float, gamma: float, lam: float) -> float:
    return x ** (1 - gamma) if x >= 0 else -lam * (-x) ** (1 - gamma)


def ce(prizes, probs, gamma, lam) -> float:
    total = sum(float(p) * value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))
    return total ** (1 / (1 - gamma)) if total >= 0 else -((-total / lam) ** (1 / (1 - gamma)))


def loglik(theta) -> float:
    gamma = 1 / (1 + math.exp(-theta[0]))
    lam, kappa = math.exp(theta[1]), math.exp(theta[2])
    out = 0.0
    for _, ch, pa, qa, pb, qb in answers:
        z = kappa * (ce(pa, qa, gamma, lam) - ce(pb, qb, gamma, lam)) / 10_000
        out += -math.log1p(math.exp(-z)) if ch == "A" else -math.log1p(math.exp(z))
    return out


best = None
for g0 in (0.05, 0.3, 0.6, 0.85):
    for l0 in (0.5, 2.0, 6.0):
        for k0 in (0.5, 2.0, 5.0):
            x0 = [math.log(g0 / (1 - g0)), math.log(l0), math.log(k0)]
            res = minimize(lambda t: -loglik(t), x0, method="Nelder-Mead",
                           options={"xatol": 1e-12, "fatol": 1e-14, "maxiter": 20000, "maxfev": 40000})
            if best is None or res.fun < best.fun:
                best = res
xi = best.x
# refine with BFGS from the Nelder-Mead point
res2 = minimize(lambda t: -loglik(t), xi, method="BFGS", options={"gtol": 1e-10})
if res2.fun < best.fun:
    xi = res2.x
gamma = 1 / (1 + math.exp(-xi[0]))
lam, kappa = math.exp(xi[1]), math.exp(xi[2])


def hessian(f, x, h):
    n = len(x)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            ei = np.zeros(n); ej = np.zeros(n)
            ei[i] = h; ej[j] = h
            H[i, j] = (f(x + ei + ej) - f(x + ei - ej) - f(x - ei + ej) + f(x - ei - ej)) / (4 * h * h)
    return H


H = hessian(loglik, np.array(xi), 1e-4)
info = -H
cov = np.linalg.inv(info)
se_gamma = gamma * (1 - gamma) * math.sqrt(cov[0, 0])
se_lambda = lam * math.sqrt(cov[1, 1])
se_kappa = kappa * math.sqrt(cov[2, 2])
print(f"gamma_hat {gamma:.6f} se {se_gamma:.4f}")
print(f"lambda_hat {lam:.6f} se {se_lambda:.4f}")
print(f"kappa_hat {kappa:.6f} se {se_kappa:.4f}")
print(f"logL {loglik(xi):.6f}")
print("prizes min", min(x for a in answers for x in a[2] + a[4]), "max", max(x for a in answers for x in a[2] + a[4]))
print("prizes per lottery", sorted({len(a[2]) for a in answers} | {len(a[4]) for a in answers}))
mixed = []
for pid, ch, pa, qa, pb, qb in answers:
    def has(prizes, probs):
        return any(x > 0 and p > 0 for x, p in zip(prizes, probs, strict=True)) and any(
            x < 0 and p > 0 for x, p in zip(prizes, probs, strict=True))
    mixed.append(has(pa, qa) or has(pb, qb))
print("mixed pairs", sum(mixed), "pure pairs", [a[0] for a, m in zip(answers, mixed, strict=True) if not m])
print("scipy", best.success, res2.success, "fun", best.fun)
