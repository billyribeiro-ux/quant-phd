"""Round 8 (M7-d): exact check of the degenerate hand case (test_project.py HAND_CASES 'degenerate box with zero turnover').
Case: gamma 1, Sigma = I, mu = (0.3, 0.1), lower = upper = w0 = (0.5, 0.5), tau = 0, one sector cap 1.0 over both assets.
Claim checked: the answer (0.5, 0.5) also has a multiplier set with EVERY inequality multiplier strictly positive, so the dual
residual must be floored. Usage: python -I degenerate_multipliers_r8.py"""
from fractions import Fraction as F

gamma = F(1)
sigma = [[F(1), F(0)], [F(0), F(1)]]
mu = [F(3, 10), F(1, 10)]
w = [F(1, 2), F(1, 2)]
nu = F(-3, 10)
lower = [F(1, 2), F(1, 2)]
upper = [F(11, 20), F(7, 20)]
eta = F(1, 20)
alpha = [F(1), F(1)]
beta = [F(1), F(1)]
kappa = F(2)
for i in range(2):
    rw = gamma * sum(sigma[i][j] * w[j] for j in range(2)) - mu[i] + nu - lower[i] + upper[i] + eta + alpha[i] - beta[i]
    rt = kappa - alpha[i] - beta[i]
    print(f"asset {i}: r_w = {rw}, r_t = {rt}")
positive = all(v > 0 for v in [*lower, *upper, eta, *alpha, *beta, kappa])
print("every inequality multiplier positive:", positive, "| smallest:", str(min([*lower, *upper, eta, *alpha, *beta, kappa])))
print("unfloored dual residual = -smallest =", str(-min([*lower, *upper, eta, *alpha, *beta, kappa])), "; floored = 0")
