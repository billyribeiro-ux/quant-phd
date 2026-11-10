"""Lab QR5-L03-1: Continuous Policy Gradient Verification & Variance Reduction.

Demonstrates:
1. Continuous action Gaussian policy parameterization for portfolio allocation.
2. Derivation and implementation of the REINFORCE score function estimator.
3. Variance reduction via state-value baseline subtraction.
4. Numerical validation of empirical policy gradient against finite difference approximation.
"""

from __future__ import annotations

import numpy as np


def evaluate_trajectory_return(theta: float, noise: np.ndarray) -> tuple[float, float]:
    """Simulate portfolio rebalancing with Gaussian policy a ~ Normal(theta, sigma^2).

    Reward R(a) = mu_asset * a - 0.5 * lambda_cost * a^2.
    """
    sigma_a = 0.5
    action = theta + sigma_a * noise
    # True market return: quadratic utility
    reward = float(0.12 * action - 0.05 * (action**2))
    # Score function d ln pi(a | theta) / d theta = (a - theta) / sigma_a^2
    score = float((action - theta) / (sigma_a**2))
    return reward, score


def main() -> None:
    rng = np.random.default_rng(42)
    n_samples = 40000
    theta_0 = 1.0

    shocks = rng.normal(0.0, 1.0, size=n_samples)

    # 1. Analytical Expected Return J(theta) = E[0.12*(theta + sigma*z)
    #    - 0.05*(theta^2 + 2*theta*sigma*z + sigma^2*z^2)]
    # J(theta) = 0.12*theta - 0.05*theta^2 - 0.05*sigma^2
    # dJ/dtheta = 0.12 - 0.10*theta
    expected_grad_analytical = 0.12 - 0.10 * theta_0

    # 2. REINFORCE Empirical Policy Gradient
    scores = np.zeros(n_samples)
    rewards = np.zeros(n_samples)

    for i in range(n_samples):
        r, sc = evaluate_trajectory_return(theta_0, shocks[i])
        rewards[i] = r
        scores[i] = sc

    # Raw REINFORCE gradient
    raw_grad_samples = scores * rewards
    var_raw = float(np.var(raw_grad_samples))

    # Baseline-subtracted REINFORCE
    baseline = float(np.mean(rewards))
    baseline_grad_samples = scores * (rewards - baseline)
    grad_baseline = float(np.mean(baseline_grad_samples))
    var_baseline = float(np.var(baseline_grad_samples))

    # 3. Finite Difference Gradient
    delta = 1e-4
    rewards_plus = np.zeros(n_samples)
    rewards_minus = np.zeros(n_samples)
    for i in range(n_samples):
        r_p, _ = evaluate_trajectory_return(theta_0 + delta, shocks[i])
        r_m, _ = evaluate_trajectory_return(theta_0 - delta, shocks[i])
        rewards_plus[i] = r_p
        rewards_minus[i] = r_m

    grad_fd = float(np.mean((rewards_plus - rewards_minus) / (2.0 * delta)))

    variance_reduction = (var_raw - var_baseline) / var_raw * 100.0

    print(f"Analytical gradient dJ/dtheta: {expected_grad_analytical:.6f}")
    print(f"Finite difference gradient: {grad_fd:.6f}")
    print(f"REINFORCE empirical gradient: {grad_baseline:.6f}")
    print(f"Raw gradient variance: {var_raw:.6f}")
    print(f"Baseline gradient variance: {var_baseline:.6f}")
    print(f"Variance reduction from baseline: {variance_reduction:.2f}%")


main()
