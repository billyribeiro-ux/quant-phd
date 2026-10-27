import numpy as np
rng = np.random.default_rng(2026)
worst_identity = 0.0; worst_feas = 0.0; worst_min = 0.0
for trial in range(200):
    T, N = 60, 4
    X = 1 + 0.3 * rng.normal(size=(T, N))
    p = X.mean(axis=0) * (1 + 0.02 * rng.normal(size=N))
    S = X.T @ X / T
    b = np.linalg.solve(S, p); xs = X @ b
    worst_identity = max(worst_identity, np.max(np.abs(X.T @ xs / T - p)))  # A3 identity E_T[x* x] = p
    # A4: m_v = v + (x-mu)' beta, beta = Sigma^{-1}(p - v mu), Sigma = Cov_T(x)
    v = 0.97; mu = X.mean(axis=0); C = (X - mu).T @ (X - mu) / T
    beta = np.linalg.solve(C, p - v * mu); mv = v + (X - mu) @ beta
    worst_feas = max(worst_feas, abs(mv.mean() - v), np.max(np.abs(X.T @ mv / T - p)))
    var_formula = (p - v * mu) @ np.linalg.solve(C, p - v * mu)
    assert abs(mv.var() - var_formula) < 1e-10 * max(1, var_formula)
    # perturb within the feasible set: m' = m_v + eps with E_T[eps]=0 and E_T[eps x]=0 => must have larger variance
    Z = rng.normal(size=(T, N)); coef = np.linalg.lstsq(np.column_stack([np.ones(T), X]), Z[:, 0], rcond=None)[0]
    eps = Z[:, 0] - np.column_stack([np.ones(T), X]) @ coef
    worst_min = max(worst_min, 0.0) if mv.var() <= (mv + 0.1 * eps).var() + 1e-15 else 1.0
print("A3 identity worst |E_T[x*x]-p|:", worst_identity)
print("A4 worst feasibility error:", worst_feas, " minimality violations (0 = none):", worst_min)
