import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaincc

# Hansen & Singleton (1982) Two-Step Nonlinear Rational Expectations GMM
rng = np.random.default_rng(101)
t_periods = 200
gamma_true = 2.0
beta_true = 0.98

log_gc = rng.normal(0.018, 0.022, size=t_periods)
gc = np.exp(log_gc)

# Bond and stock returns generated in population equilibrium
rf_log = -np.log(beta_true) + gamma_true * 0.018 - 0.5 * (gamma_true * 0.022) ** 2
r_bond = np.exp(rf_log + rng.normal(0.0, 0.003, size=t_periods))

sigma_s = 0.07
rho_s = 0.60
cov_sc = gamma_true * rho_s * 0.022 * sigma_s
mu_s = rf_log - 0.5 * (sigma_s**2) + cov_sc
z_s = rho_s * ((log_gc - 0.018) / 0.022) + np.sqrt(1.0 - rho_s**2) * rng.normal(0.0, 1.0, size=t_periods)
r_stock = np.exp(mu_s + sigma_s * z_s)

returns = np.column_stack([r_bond, r_stock])  # (T, 2)
# Instruments: constant and lagged consumption growth
instruments = np.column_stack([np.ones(t_periods), np.roll(gc, 1)])
instruments[0, 1] = np.exp(0.018)


def moments(theta: np.ndarray) -> np.ndarray:
    b, g = float(theta[0]), float(theta[1])
    m = b * (gc ** (-g))
    u1 = m * returns[:, 0] - 1.0
    u2 = m * returns[:, 1] - 1.0
    return np.column_stack(
        [
            u1 * instruments[:, 0],
            u1 * instruments[:, 1],
            u2 * instruments[:, 0],
            u2 * instruments[:, 1],
        ]
    )


def objective(theta: np.ndarray, weight: np.ndarray) -> float:
    g_bar = np.mean(moments(theta), axis=0)
    return float(g_bar.T @ weight @ g_bar)


# Step 1: Identity weighting matrix
w1 = np.eye(4)
res1 = minimize(objective, [0.95, 1.5], args=(w1,), method="Nelder-Mead")
beta_1, gamma_1 = float(res1.x[0]), float(res1.x[1])

# Spectral density matrix S = (1/T) sum h_t h_t^T
h1 = moments(res1.x)
s_matrix = (h1.T @ h1) / float(t_periods)
w2 = np.linalg.pinv(s_matrix)

# Step 2: Optimal weighting matrix
res2 = minimize(objective, res1.x, args=(w2,), method="Nelder-Mead")
beta_2, gamma_2 = float(res2.x[0]), float(res2.x[1])

j_stat = float(t_periods * objective(res2.x, w2))
df = 4 - 2  # 4 moments minus 2 parameters
p_val = float(gammaincc(df / 2.0, j_stat / 2.0))

print(f"Step 1 estimates: beta = {beta_1:.4f}, gamma = {gamma_1:.4f}")
print(f"Step 2 estimates: beta = {beta_2:.4f}, gamma = {gamma_2:.4f}")
print(f"Hansen J-statistic: {j_stat:.4f} (df = {df}, p-value = {p_val:.4f})")
