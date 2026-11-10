"""Lab E7-L02-1: Reputational Equilibrium in the Barro-Gordon (1983) Repeated Game.

Evaluates Grim Trigger strategies in an infinitely repeated Barro-Gordon game:
1. Honest commitment loss per period
2. One-period temptation gain from surprise cheating
3. Subsequent punishment loss in perpetual discretionary Nash
4. Analytical calculation of the critical discount factor beta* required for sustainable commitment
"""

from __future__ import annotations


def solve_barro_gordon_reputation(
    alpha: float,
    gamma: float,
    k: float,
    y_n: float,
) -> dict[str, float]:
    """Calculate the temptation, enforcement, and critical discount factor."""
    # Commitment: pi = 0, pi_e = 0
    # L_C = (y_n - k*y_n)^2 + gamma * 0^2 = (1 - k)^2 * y_n^2
    target_gap = (1.0 - k) * y_n
    loss_c = target_gap**2

    # Discretionary Nash: pi_e = pi_d = (alpha / gamma) * (k - 1) * y_n
    pi_d = (alpha / gamma) * (k - 1.0) * y_n
    loss_d = target_gap**2 + gamma * (pi_d**2)

    # Cheating (Temptation): People expect pi_e = 0 (commitment), but CB cheats!
    # CB chooses pi_cheat to min (y_n + alpha*(pi - 0) - k*y_n)^2 + gamma * pi^2
    # dL/dpi = 2 * alpha * (y_n + alpha*pi - k*y_n) + 2 * gamma * pi = 0
    # (alpha^2 + gamma) * pi = alpha * (k - 1) * y_n
    pi_cheat = (alpha * (k - 1.0) * y_n) / (alpha**2 + gamma)
    y_cheat = y_n + alpha * pi_cheat
    loss_cheat = (y_cheat - k * y_n) ** 2 + gamma * (pi_cheat**2)

    # Temptation gain in date t:
    temptation = loss_c - loss_cheat

    # Punishment loss per period in dates t+1, t+2, ...:
    punishment = loss_d - loss_c

    # Sustainable commitment condition:
    # Temptation <= sum_{j=1}^inf beta^j * Punishment = (beta / (1 - beta)) * Punishment
    # beta / (1 - beta) >= Temptation / Punishment
    # beta* = Temptation / (Temptation + Punishment)
    critical_beta = temptation / (temptation + punishment)

    return {
        "loss_c": loss_c,
        "loss_cheat": loss_cheat,
        "loss_d": loss_d,
        "pi_cheat": pi_cheat,
        "pi_d": pi_d,
        "temptation": temptation,
        "punishment": punishment,
        "critical_beta": critical_beta,
    }


def main() -> None:
    alpha = 1.0
    gamma = 2.0
    k = 1.10
    y_n = 100.0

    res = solve_barro_gordon_reputation(alpha, gamma, k, y_n)

    print("Barro-Gordon (1983) Reputational Mechanism:")
    print(f"  Baseline loss under zero-inflation commitment: {res['loss_c']:.2f}")
    print(f"  Cheating temptation loss (surprise inflation):  {res['loss_cheat']:.2f}")
    print(f"  Perpetual discretionary Nash loss:              {res['loss_d']:.2f}")
    print("\nIncentive Compatibility:")
    print(f"  One-period temptation gain: {res['temptation']:.4f}")
    print(f"  Per-period punishment loss: {res['punishment']:.4f}")
    print(f"  Critical discount factor beta*: {res['critical_beta']:.4f}")
    print(f"  Commitment sustainable for beta > {res['critical_beta']:.4f}: True")


main()
