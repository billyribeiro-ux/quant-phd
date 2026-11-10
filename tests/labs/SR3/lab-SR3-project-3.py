"""Lab SR3-project-3 (Rung 4 Stretch Extension): Dynamic Multi-Horizon Stress Cascade Engine.

SIMULATED: couples interbank default clearing with endogenous fire-sale price impact
over multiple stress horizons, evaluating systemic liquidation spirals.
"""

from __future__ import annotations

import numpy as np


def clear_network(l_mat: np.ndarray, z_vec: np.ndarray, b_vec: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    p_bar = np.sum(l_mat, axis=1)
    pi_mat = np.zeros_like(l_mat)
    has_liab = p_bar > 1e-12
    pi_mat[has_liab] = l_mat[has_liab] / p_bar[has_liab, None]

    p = p_bar.copy()
    for _ in range(300):
        p_next = np.minimum(p_bar, np.maximum(0.0, z_vec + pi_mat.T @ p - b_vec))
        if np.max(np.abs(p_next - p)) < 1e-9:
            p = p_next
            break
        p = p_next
    defaults = (p < p_bar - 1e-7).astype(int)
    return p, defaults


def main() -> None:
    n_banks = 4
    n_periods = 3
    fire_sale_alpha = 0.015  # Linear price impact parameter (1.5% drop per $1B liquidated)

    # Base interbank network
    l_mat = np.array(
        [
            [0.0, 30.0, 20.0, 10.0],
            [20.0, 0.0, 25.0, 15.0],
            [15.0, 25.0, 0.0, 20.0],
            [10.0, 15.0, 25.0, 0.0],
        ]
    )
    p_bar = np.sum(l_mat, axis=1)

    # Holdings of illiquid common asset (units): [20, 35, 45, 30]
    asset_holdings = np.array([20.0, 35.0, 45.0, 30.0])
    price_t = 1.0  # Initial asset price

    # Liquid cash reserves z_cash and senior outside liabilities b
    z_cash = np.array([2.0, 4.0, 6.0, 3.0])
    b_senior = np.array([20.0, 15.0, 18.0, 14.0])

    print("=== Dynamic Multi-Horizon Stress Cascade Engine (Stretch) ===")
    print(f"Network Size: N={n_banks} banks | Stress Horizons: T={n_periods}")
    print("-" * 75)

    cumulative_defaults = np.zeros(n_banks, dtype=int)

    for t in range(1, n_periods + 1):
        # Exogenous macro shock in period 1: 30% fundamental asset price decline
        if t == 1:
            price_t = 0.70

        # Outside asset valuation: cash + mark-to-market illiquid assets
        z_total = z_cash + asset_holdings * price_t

        # Solve interbank clearing
        p_star, period_defaults = clear_network(l_mat, z_total, b_senior)
        new_defaults = (period_defaults == 1) & (cumulative_defaults == 0)
        cumulative_defaults = np.maximum(cumulative_defaults, period_defaults)

        # Forced fire sales: newly defaulting banks liquidate 70% of illiquid assets
        liquidated_units = float(np.sum(asset_holdings[new_defaults] * 0.70))
        liquidation_dollar = liquidated_units * price_t

        # Endogenous price impact: Delta P / P = - alpha * liquidation_dollar
        price_drop_pct = fire_sale_alpha * liquidation_dollar
        next_price = price_t * max(0.20, 1.0 - price_drop_pct)

        print(f"Horizon t={t}:")
        print(f"  Asset Price: ${price_t:.4f} (Fire-Sale Impact: -{price_drop_pct * 100:.2f}%)")
        n_new = int(np.sum(new_defaults))
        n_cum = int(np.sum(cumulative_defaults))
        print(f"  New Defaults: {n_new} | Cumulative Defaults: {n_cum}/{n_banks}")
        print(f"  Forced Fire Sales: ${liquidation_dollar:.2f}B | Systemic Shortfall: ${np.sum(p_bar - p_star):.2f}B")

        price_t = next_price

    print("-" * 75)
    print("Coupled Contagion Outcome: Feedback between interbank contractual insolvencies")
    print("and fire-sale asset devaluations amplifies cumulative defaults across horizons.")


main()
