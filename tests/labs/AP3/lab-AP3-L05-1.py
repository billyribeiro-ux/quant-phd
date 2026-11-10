import numpy as np

# Weil (1989) Risk-Free Rate Puzzle: CRRA Coupling of RRA and EIS
mu_c = 0.018  # annual consumption growth (1.8%)
sigma_c = 0.015  # post-war consumption volatility (1.5%)
beta = 0.99  # subjective discount factor

gamma_grid = [1.0, 5.0, 10.0, 20.0, 30.0, 40.0]

print(f"{'gamma':>5} | {'EIS':>7} | {'Growth Term':>12} | {'Precautionary':>14} | {'Net rf':>8}")
print("-" * 56)
for g in gamma_grid:
    eis = 1.0 / g
    growth_term = g * mu_c
    prec_term = -0.5 * (g**2) * (sigma_c**2)
    rf_net = -np.log(beta) + growth_term + prec_term
    print(f"{g:5.1f} | {eis:7.4f} | {growth_term * 100:11.2f}% | {prec_term * 100:13.2f}% | {rf_net * 100:7.2f}%")

print("-" * 56)
print("Historical US real risk-free rate (1889-1978): ~0.80%")
