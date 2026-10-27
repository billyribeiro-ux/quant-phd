# Verifier-written numeric checks for L05-L06 cards c049, c055, c056, c080 on random markets (not the builder's data).
import numpy as np
worst = dict(c080=0.0, c049=0.0, c055_viol=0, c056=0.0, c048=0.0)
for seed in range(200):
    rng = np.random.default_rng(1000 + seed)
    S, N = int(rng.integers(4, 9)), int(rng.integers(1, 4))
    pi = rng.dirichlet(np.ones(S))
    X = np.column_stack([np.ones(S), rng.lognormal(0, 0.3, (S, N))])
    m_true = np.exp(rng.normal(0, 0.3, S)); m_true /= pi @ m_true
    p = X.T @ (pi * m_true)
    Sig = X.T @ np.diag(pi) @ X
    b = np.linalg.solve(Sig, p); xs = X @ b
    Ex = pi @ xs
    # c080: x* is the minimum-variance SDF at its own mean v* = E[x*]
    v = Ex
    mu = pi @ X[:, 1:]
    Sig_x = (X[:, 1:] - mu).T @ np.diag(pi) @ (X[:, 1:] - mu)
    p_x = p[1:] - 0  # use payoffs excluding riskless column for the centered formula
    # m_v = v + (x - mu)' Sigma^-1 (p - v mu) with the centering of the risky payoffs
    cov = Sig_x
    coef = np.linalg.solve(cov, p[1:] - v * mu)
    mv = v + (X[:, 1:] - mu) @ coef
    worst['c080'] = max(worst['c080'], np.max(np.abs(mv - xs)))
    # c049 variance formula for m_v equals (p - v mu)' Sigma^-1 (p - v mu) (centered form) with mv prices all payoffs
    var_mv = pi @ (mv - v) ** 2
    worst['c049'] = max(worst['c049'], abs(var_mv - (p[1:] - v * mu) @ coef))
    # c055: E[R*] < R_f whenever Var(x*) > 0
    Rf = 1 / (pi @ xs)
    Rstar = xs / (pi @ xs**2)
    if not (pi @ Rstar < Rf or pi @ xs**2 - (pi @ xs) ** 2 < 1e-12):
        worst['c055_viol'] += 1
    # c056: E[R] - R_f = -R_f Cov(m, R) for a risky gross return R
    R = X[:, 1] / p[1]  # gross return: price 1
    lhs = pi @ R - Rf
    rhs = -Rf * (pi @ ((m_true - pi @ m_true) * (R - pi @ R)))
    worst['c056'] = max(worst['c056'], abs(lhs - rhs))
    # c048: R* = x*/E[x*^2] has second moment 1/E[x*^2]
    worst['c048'] = max(worst['c048'], abs(pi @ Rstar**2 - 1 / (pi @ xs**2)))
print("200 random markets:", worst)
