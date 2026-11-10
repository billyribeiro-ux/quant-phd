import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaincc

# Rung 1 Worked Example: GMM Euler Estimation & Hansen-Jagannathan Frontier
rng = np.random.default_rng(0)
t_periods = 160
beta_true, gamma_true = 0.98, 2.0

log_gc = rng.normal(0.018, 0.022, size=t_periods)
c_growth = np.exp(log_gc)
std_c = (log_gc - 0.018) / 0.022

rf_log = -np.log(beta_true) + gamma_true * 0.018 - 0.5 * (gamma_true * 0.022) ** 2
r0 = np.exp(rf_log + 0.006 * rng.normal(0.0, 1.0, size=t_periods))

cov1 = gamma_true * 0.65 * 0.022 * 0.08
mu1 = rf_log - 0.5 * (0.08**2) + cov1
z1 = 0.65 * std_c + np.sqrt(1.0 - 0.65**2) * rng.normal(0.0, 1.0, size=t_periods)
r1 = np.exp(mu1 + 0.08 * z1)
returns = np.column_stack([r0, r1])

instruments = np.column_stack([np.ones(t_periods), np.roll(c_growth, 1)])
instruments[0, 1] = np.exp(0.018)


def moments(theta: np.ndarray) -> np.ndarray:
    b, g = float(theta[0]), float(theta[1])
    m = b * (c_growth ** (-g))
    u0 = m * returns[:, 0] - 1.0
    u1 = m * returns[:, 1] - 1.0
    return np.column_stack(
        [
            u0 * instruments[:, 0],
            u0 * instruments[:, 1],
            u1 * instruments[:, 0],
            u1 * instruments[:, 1],
        ]
    )


def objective(theta: np.ndarray, w: np.ndarray) -> float:
    g_bar = np.mean(moments(theta), axis=0)
    return float(g_bar.T @ w @ g_bar)


# Step 1: Identity weighting matrix
w1 = np.eye(4)
res1 = minimize(objective, [0.95, 2.0], args=(w1,), method="Nelder-Mead")

# Step 2: Optimal weighting matrix
h1 = moments(res1.x)
s_matrix = (h1.T @ h1) / float(t_periods)
w2 = np.linalg.pinv(s_matrix)
res2 = minimize(objective, res1.x, args=(w2,), method="Nelder-Mead")

beta_hat, gamma_hat = float(res2.x[0]), float(res2.x[1])
j_stat = float(t_periods * objective(res2.x, w2))
df = 4 - 2
j_pval = float(gammaincc(df / 2.0, j_stat / 2.0))

print(f"GMM estimates: beta = {beta_hat:.4f}, gamma = {gamma_hat:.4f}")
print(f"Hansen J-statistic: {j_stat:.4f} (p-value: {j_pval:.4f})")

# Hansen-Jagannathan bound at nu = 0.98
mu_r = np.mean(returns, axis=0)
sigma_r = np.cov(returns, rowvar=False)
sigma_inv = np.linalg.pinv(sigma_r)
diff = np.ones(2) - 0.98 * mu_r
hj_vol = float(np.sqrt(diff.T @ sigma_inv @ diff))
print(f"Hansen-Jagannathan volatility lower bound at E[M]=0.98: {hj_vol:.4f}")
