"""Lab S6-L01-1: Potential outcomes and the selection problem.

SIMULATED: compares naive difference in means against the true Average Treatment Effect (ATE)
under observational selection (confounded) versus randomized treatment assignment.
"""

from __future__ import annotations

import random


def main() -> None:
    rng = random.Random(42)
    n = 10000

    # True structural parameters
    mu_0 = 10.0
    true_tau = 2.50

    # Generate potential outcomes for population
    # U_i is an unobserved confounder (e.g. manager skill, firm quality)
    u = [rng.gauss(0.0, 1.5) for _ in range(n)]
    y0 = [mu_0 + u[i] + rng.gauss(0.0, 0.5) for i in range(n)]
    y1 = [y0[i] + true_tau for i in range(n)]

    true_ate = sum(y1[i] - y0[i] for i in range(n)) / n

    # 1. Observational Selection: treatment assignment correlated with confounder U_i
    # Higher U_i -> higher probability of selecting into treatment D_obs = 1
    d_obs = [1 if u[i] + rng.gauss(0.0, 1.0) > 0.0 else 0 for i in range(n)]
    y_obs = [y1[i] if d_obs[i] == 1 else y0[i] for i in range(n)]

    n_treat_obs = sum(d_obs)
    n_ctrl_obs = n - n_treat_obs

    mean_treat_obs = sum(y_obs[i] for i in range(n) if d_obs[i] == 1) / n_treat_obs
    mean_ctrl_obs = sum(y_obs[i] for i in range(n) if d_obs[i] == 0) / n_ctrl_obs
    naive_diff_obs = mean_treat_obs - mean_ctrl_obs

    # Actual baseline difference in potential outcome Y(0) between groups (Selection Bias)
    e_y0_treat = sum(y0[i] for i in range(n) if d_obs[i] == 1) / n_treat_obs
    e_y0_ctrl = sum(y0[i] for i in range(n) if d_obs[i] == 0) / n_ctrl_obs
    selection_bias = e_y0_treat - e_y0_ctrl

    # 2. Randomized Assignment: treatment assigned independently with probability 0.5
    d_rand = [1 if rng.random() < 0.5 else 0 for _ in range(n)]
    y_rand = [y1[i] if d_rand[i] == 1 else y0[i] for i in range(n)]

    n_treat_rnd = sum(d_rand)
    n_ctrl_rnd = n - n_treat_rnd

    mean_treat_rnd = sum(y_rand[i] for i in range(n) if d_rand[i] == 1) / n_treat_rnd
    mean_ctrl_rnd = sum(y_rand[i] for i in range(n) if d_rand[i] == 0) / n_ctrl_rnd
    naive_diff_rnd = mean_treat_rnd - mean_ctrl_rnd

    print("Potential Outcomes Identification Analysis (SIMULATED):")
    print(f"  Population size N: {n}")
    print(f"  True ATE: {true_ate:.4f}")
    print("\nObservational Sample (Confounded Selection):")
    print(f"  Treated mean Y: {mean_treat_obs:.4f} (N={n_treat_obs})")
    print(f"  Control mean Y: {mean_ctrl_obs:.4f} (N={n_ctrl_obs})")
    print(f"  Naive Difference: {naive_diff_obs:.4f}")
    print(f"  Baseline Y(0) Bias: {selection_bias:.4f}")
    print(f"  Decomposition Check (ATE + Bias): {true_ate + selection_bias:.4f}")
    print("\nRandomized Assignment Sample:")
    print(f"  Treated mean Y: {mean_treat_rnd:.4f} (N={n_treat_rnd})")
    print(f"  Control mean Y: {mean_ctrl_rnd:.4f} (N={n_ctrl_rnd})")
    print(f"  Randomized Difference: {naive_diff_rnd:.4f}")
    print(f"  Absolute Error vs ATE: {abs(naive_diff_rnd - true_ate):.4f}")


main()
