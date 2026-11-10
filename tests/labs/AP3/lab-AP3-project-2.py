import numpy as np

# Rung 2 Completion Problem: Hansen-Jagannathan Bound Computation
rng = np.random.default_rng(123)
t_periods = 180

# 2 simulated asset return series
returns = np.column_stack(
    [
        1.02 + rng.normal(0.0, 0.015, size=t_periods),
        1.08 + rng.normal(0.0, 0.150, size=t_periods),
    ]
)


def compute_hj_bound(gross_returns: np.ndarray, nu_target: float) -> float:
    """Compute the Hansen-Jagannathan minimum SDF volatility at target mean nu_target."""
    mu = np.mean(gross_returns, axis=0)
    cov = np.cov(gross_returns, rowvar=False)
    diff = np.ones(gross_returns.shape[1]) - nu_target * mu
    var_m = float(diff.T @ np.linalg.pinv(cov) @ diff)
    return float(np.sqrt(max(0.0, var_m)))


bound_095 = compute_hj_bound(returns, 0.95)
bound_098 = compute_hj_bound(returns, 0.98)
bound_100 = compute_hj_bound(returns, 1.00)

print(f"HJ bound at E[M]=0.95: {bound_095:.4f}")
print(f"HJ bound at E[M]=0.98: {bound_098:.4f}")
print(f"HJ bound at E[M]=1.00: {bound_100:.4f}")
