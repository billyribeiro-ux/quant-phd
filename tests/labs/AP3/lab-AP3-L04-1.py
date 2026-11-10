import numpy as np

# Mehra & Prescott (1985) Calibration of the Equity Premium Puzzle
mu_c = 0.0183
sigma_c = 0.0357
rho_c = -0.14

delta = sigma_c
phi = (1.0 + rho_c) / 2.0  # 0.43

lambda_states = np.array([1.0 + mu_c + delta, 1.0 + mu_c - delta])
pi_matrix = np.array([[phi, 1.0 - phi], [1.0 - phi, phi]])
stat_dist = np.array([0.5, 0.5])


def solve_economy(beta: float, gamma: float) -> tuple[float, float, float]:
    a_matrix = beta * pi_matrix * (lambda_states ** (1.0 - gamma))
    if np.max(np.abs(np.linalg.eigvals(a_matrix))) >= 1.0:
        return np.nan, np.nan, np.nan
    w = np.linalg.solve(np.eye(2) - a_matrix, a_matrix @ np.ones(2))
    if np.any(w <= 0.0):
        return np.nan, np.nan, np.nan

    # Expected equity return: E[R^e | i] = sum_j Pi_ij * (w_j + 1) * lambda_j / w_i
    exp_re_states = np.array([float(np.sum(pi_matrix[i] * (w + 1.0) * lambda_states) / w[i]) for i in range(2)])
    exp_re = float(np.sum(stat_dist * exp_re_states))

    # Risk-free bond price: q_i = beta * sum_j Pi_ij * lambda_j^(-gamma)
    q = beta * (pi_matrix @ (lambda_states ** (-gamma)))
    rf_states = 1.0 / q
    exp_rf = float(np.sum(stat_dist * rf_states))

    return exp_re - 1.0, exp_rf - 1.0, exp_re - exp_rf


gammas = [1.0, 2.0, 5.0, 10.0]
betas = [0.95, 0.98, 0.99]
max_premium = 0.0

print(f"{'gamma':>5} | {'beta':>5} | {'E[Re]-1':>8} | {'Rf-1':>7} | {'Premium':>8}")
print("-" * 43)
for g in gammas:
    for b in betas:
        re, rf, prem = solve_economy(b, g)
        if not np.isnan(prem):
            if prem > max_premium:
                max_premium = prem
            print(f"{g:5.1f} | {b:5.2f} | {re * 100:7.2f}% | {rf * 100:6.2f}% | {prem * 100:7.3f}%")

print("-" * 43)
print(f"Max model premium (gamma <= 10): {max_premium * 100:.3f}%")
print("Historical US equity premium (1889-1978): 6.180%")
