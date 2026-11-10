import numpy as np

# Hansen & Jagannathan (1991) Bound vs. Consumption-Implied SDF Volatility
rng = np.random.default_rng(777)
t_periods = 200

# 3 simulated test asset returns: short-term bill, equity, intermediate bond
returns = np.column_stack(
    [
        1.01 + rng.normal(0.0, 0.01, size=t_periods),
        1.07 + rng.normal(0.0, 0.16, size=t_periods),
        1.03 + rng.normal(0.0, 0.06, size=t_periods),
    ]
)

mu_r = np.mean(returns, axis=0)
sigma_r = np.cov(returns, rowvar=False)
sigma_inv = np.linalg.pinv(sigma_r)
ones = np.ones(3)


def hj_bound(nu: float) -> float:
    diff = ones - nu * mu_r
    variance = float(diff.T @ sigma_inv @ diff)
    return float(np.sqrt(max(0.0, variance)))


# Consumption growth series
gc = 1.0 + rng.normal(0.018, 0.020, size=t_periods)
beta = 0.99
gammas = [1.0, 5.0, 10.0, 25.0, 35.0]

print(f"{'gamma':>5} | {'E[M]':>6} | {'sigma(M)':>8} | {'HJ Bound':>9} | {'Verdict':>8}")
print("-" * 46)
for g in gammas:
    m = beta * (gc ** (-g))
    e_m = float(np.mean(m))
    std_m = float(np.std(m))
    bound = hj_bound(e_m)
    verdict = "FEASIBLE" if std_m >= bound else "REJECTED"
    print(f"{g:5.1f} | {e_m:6.4f} | {std_m:8.4f} | {bound:9.4f} | {verdict:>8}")
