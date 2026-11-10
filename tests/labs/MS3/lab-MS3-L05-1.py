"""Lab MS3-L05-1: Obizhaeva-Wang optimal execution with limit order book resilience.

Simulates optimal execution under transient impact with exponential resilience rho,
demonstrating discrete boundary block trades and steady continuous rate.
"""

from __future__ import annotations


def obizhaeva_wang_schedule(
    total_shares: float,
    horizon: float,
    resilience: float,
) -> tuple[float, float, float]:
    """Compute Obizhaeva-Wang (2013) optimal execution strategy:

    x_0 = X / (2 + rho * T)
    v^* = rho * X / (2 + rho * T)
    x_t = X / (2 + rho * T)
    """
    denom = 2.0 + resilience * horizon
    x_0 = total_shares / denom
    v_star = (resilience * total_shares) / denom
    x_t = total_shares / denom
    return x_0, v_star, x_t


def main() -> None:
    total_shares = 100_000.0  # 100,000 shares
    horizon = 1.0  # 1 trading day

    # Resilience parameter rho (replenishment rate per day)
    resilience_values = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0]

    print("Obizhaeva-Wang Optimal Execution Strategy (X=100k, T=1.0d):")
    print("  Resilience rho | Initial Block x_0 | Steady Rate v^* (sh/d) | Terminal Block x_t | Sum Traded")
    print("------------------------------------------------------------------------------------------------")

    for rho in resilience_values:
        x_0, v_star, x_t = obizhaeva_wang_schedule(total_shares, horizon, rho)
        continuous_shares = v_star * horizon
        total_traded = x_0 + continuous_shares + x_t
        print(f"  {rho:14.1f} | {x_0:17,.1f} | {v_star:22,.1f} | {x_t:18,.1f} | {total_traded:10,.1f}")

    print("------------------------------------------------------------------------------------------------")
    print("Theoretical limits:")
    print("  1. Zero resilience (rho -> 0): Order splits into two equal lump trades of 50k at t=0 and t=T.")
    print("  2. Infinite resilience (rho -> inf): Boundary trades vanish, recovering continuous TWAP.")
    print("Exact conservation: x_0 + v^* * T + x_t = 100,000 shares across all resilience values.")


main()
