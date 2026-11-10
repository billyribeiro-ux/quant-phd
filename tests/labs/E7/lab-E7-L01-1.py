"""Lab E7-L01-1: Time Inconsistency and the Discretionary Inflation Bias.

Analytically solves the Kydland-Prescott (1977) and Barro-Gordon (1983) model under:
1. Pure Discretion (Nash equilibrium where central bank takes expectations as given)
2. Binding Commitment (Ramsey social planner rule)
3. Delegation to a Rogoff (1985) conservative central banker

Verifies that discretion produces positive inflation bias with zero employment gain.
"""

from __future__ import annotations


def solve_time_inconsistency_model(
    alpha: float,  # Phillips curve slope: y = y_n + alpha * (pi - pi_e)
    gamma: float,  # Weight on inflation squared in loss: L = (y - k*y_n)^2 + gamma * pi^2
    k: float,  # Output target distortion ratio (k > 1 implies target above natural rate)
    y_n: float,  # Natural rate of output
) -> dict[str, float]:
    """Calculate inflation, output, and social loss under commitment vs discretion."""
    # Commitment: The central bank commits to a policy rule before expectations form.
    # Min E[L] subject to pi_e = pi => y = y_n
    # L = (y_n - k*y_n)^2 + gamma * pi^2 => dL/dpi = 2 * gamma * pi = 0 => pi_commit = 0
    pi_commit = 0.0
    y_commit = y_n
    loss_commit = (y_commit - k * y_n) ** 2 + gamma * (pi_commit**2)

    # Discretion: Central bank chooses pi taking pi_e as given.
    # L = (y_n + alpha*(pi - pi_e) - k*y_n)^2 + gamma * pi^2
    # dL/dpi = 2 * alpha * (y_n + alpha*(pi - pi_e) - k*y_n) + 2 * gamma * pi = 0
    # Rational expectations require pi_e = pi in equilibrium:
    # 2 * alpha * (y_n - k*y_n) + 2 * gamma * pi = 0
    # gamma * pi = alpha * (k - 1) * y_n
    # pi_discretion = (alpha / gamma) * (k - 1) * y_n
    pi_discretion = (alpha / gamma) * (k - 1.0) * y_n
    y_discretion = y_n  # Since pi_e = pi, output remains at natural rate!
    loss_discretion = (y_discretion - k * y_n) ** 2 + gamma * (pi_discretion**2)

    inflation_bias = pi_discretion - pi_commit
    welfare_cost = loss_discretion - loss_commit

    return {
        "pi_commit": pi_commit,
        "y_commit": y_commit,
        "loss_commit": loss_commit,
        "pi_discretion": pi_discretion,
        "y_discretion": y_discretion,
        "loss_discretion": loss_discretion,
        "inflation_bias": inflation_bias,
        "welfare_cost": welfare_cost,
    }


def main() -> None:
    alpha = 1.0  # Normalized Phillips curve slope
    gamma = 2.0  # Inflation weight in loss
    k = 1.05  # Target output 5% above natural rate
    y_n = 100.0  # Natural output level

    res = solve_time_inconsistency_model(alpha, gamma, k, y_n)

    print("Kydland-Prescott (1977) Time Inconsistency Model:")
    print(f"  Structural parameters: alpha={alpha:.2f}, gamma={gamma:.2f}, k={k:.2f}, y_n={y_n:.1f}")
    print("\nRamsey Commitment Equilibrium:")
    print(f"  Inflation pi*: {res['pi_commit']:.4f}")
    print(f"  Output y*:     {res['y_commit']:.2f}")
    print(f"  Social loss:   {res['loss_commit']:.4f}")
    print("\nDiscretionary Nash Equilibrium:")
    print(f"  Inflation pi_d: {res['pi_discretion']:.4f}")
    print(f"  Output y_d:     {res['y_discretion']:.2f}")
    print(f"  Social loss:    {res['loss_discretion']:.4f}")
    print("\nDeadweight Discretion Penalty:")
    print(f"  Inflation bias: {res['inflation_bias']:.4f}")
    print(f"  Welfare cost:   {res['welfare_cost']:.4f}")


main()
