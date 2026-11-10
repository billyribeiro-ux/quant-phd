import numpy as np

# Breeden (1979) Continuous-Time CCAPM: Multi-Beta ICAPM Collapse
rng = np.random.default_rng(42)
t_periods = 2000
gamma = 3.0

# 2 Merton investment opportunity state variables (e.g. interest rate & volatility shocks)
cov_z = np.array([[0.04, 0.01], [0.01, 0.04]])
dz = rng.multivariate_normal([0.0, 0.0], cov_z, size=t_periods)
dw = rng.normal(0.0, 0.15, size=t_periods)  # aggregate wealth shock

# By Breeden's envelope theorem: u'(c) = J_W, so consumption growth aggregates all state hedging demands
dc = (0.20 * dw + 0.15 * dz[:, 0] - 0.10 * dz[:, 1]) / gamma

# 4 assets with diverse factor loadings on wealth and state variables
betas = np.array(
    [
        [0.8, 0.5, -0.2],
        [1.2, -0.3, 0.6],
        [0.5, 1.0, 0.4],
        [1.5, 0.2, -0.8],
    ]
)
idiosyncratic = rng.normal(0.0, 0.02, size=(t_periods, 4))
shocks = np.column_stack([dw, dz])
excess_returns = shocks @ betas.T + idiosyncratic

# Consumption betas: beta_{i, c} = Cov(R_i, dc) / Var(dc)
var_c = float(np.var(dc))
cov_c = np.array([float(np.cov(excess_returns[:, i], dc)[0, 1]) for i in range(4)])
consumption_betas = cov_c / var_c
mean_excess = np.mean(excess_returns, axis=0)

# Cross-sectional regression: E[R_i - R_f] = lambda_c * beta_{i, c}
lambda_c = float(np.linalg.lstsq(consumption_betas[:, None], mean_excess, rcond=None)[0][0])
pricing_errors = mean_excess - consumption_betas * lambda_c
max_error = float(np.max(np.abs(pricing_errors)))

print("Consumption betas:", np.round(consumption_betas, 4).tolist())
print("Mean excess returns:", np.round(mean_excess, 4).tolist())
print(f"Consumption risk price lambda_c: {lambda_c:.6f}")
print(f"Max absolute pricing error: {max_error:.5f}")
