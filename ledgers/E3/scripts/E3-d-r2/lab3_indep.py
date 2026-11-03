"""Independent Lab 3 check: scipy optimiser from random starts, own finite-difference Hessian (Richardson), delta method."""
import math, re, sys
from fractions import Fraction as F
import numpy as np
from scipy.optimize import minimize
src = open(sys.argv[1], encoding="utf-8").read()
ns = {}
exec(compile(src.split("def value(")[0], "answers", "exec"), ns)  # imports + ANSWERS only
ANSWERS = ns["ANSWERS"]
def ce(prizes, probs, g, lam):
    total = 0.0
    for x, p in zip(prizes, probs):
        pf = float(F(p))
        total += pf * (x ** (1 - g) if x >= 0 else -lam * (-x) ** (1 - g))
    if total >= 0:
        return total ** (1 / (1 - g))
    return -((-total / lam) ** (1 / (1 - g)))
def ll(th):
    g = 1 / (1 + math.exp(-th[0])); lam = math.exp(th[1]); k = math.exp(th[2])
    s = 0.0
    for _, c, pa, qa, pb, qb in ANSWERS:
        z = k * (ce(pa, qa, g, lam) - ce(pb, qb, g, lam)) / 1e4
        s += -math.log1p(math.exp(-z)) if c == "A" else -math.log1p(math.exp(z))
    return s
best = None
rng = np.random.default_rng(12345)
for trial in range(60):
    x0 = np.array([rng.normal(0, 1.5), rng.normal(0.5, 1.2), rng.normal(0.5, 1.0)])
    r = minimize(lambda t: -ll(t), x0, method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000, "maxfev": 40000})
    r = minimize(lambda t: -ll(t), r.x, method="BFGS", options={"gtol": 1e-10})
    if best is None or r.fun < best.fun - 1e-12:
        best = r
th = best.x
print("trials best -ll", -best.fun)
g = 1 / (1 + math.exp(-th[0])); lam = math.exp(th[1]); k = math.exp(th[2])
print("gamma_hat %.6f lambda_hat %.6f kappa_hat %.6f" % (g, lam, k))
# central-difference Hessian at step h with Richardson extrapolation
def hess(t, h):
    H = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            def f(di, dj):
                u = t.copy(); u[i] += di; u[j] += dj; return ll(u)
            H[i, j] = (f(h, h) - f(h, -h) - f(-h, h) + f(-h, -h)) / (4 * h * h)
    return H
H1 = hess(th, 1e-4); H2 = hess(th, 5e-5)
Hr = (4 * H2 - H1) / 3
info = -Hr
cov = np.linalg.inv(info)
se_g = g * (1 - g) * math.sqrt(cov[0, 0]); se_l = lam * math.sqrt(cov[1, 1]); se_k = k * math.sqrt(cov[2, 2])
print("se_gamma %.4f se_lambda %.4f se_kappa %.4f" % (se_g, se_l, se_k))
grad = np.zeros(3)
for i in range(3):
    e = np.zeros(3); e[i] = 1e-5
    grad[i] = (ll(th + e) - ll(th - e)) / 2e-5
print("gradient at estimate (zeta, loglam, logkappa):", grad)
print("loglik %.6f" % ll(th))
print("eigen info", np.linalg.eigvalsh(info))
