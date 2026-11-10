"""Lab SR2-L03-1: Margin Spirals and Fire Sales.

Simulates the coupled loss and margin spirals of Brunnermeier and Pedersen (2008)
under cash-in-the-market pricing and endogenous haircuts. Computes the dynamic
liquidation cascade and checks the theoretical feedback multiplier condition.
"""


def main() -> None:
    # Model parameters (SIMULATED wholesale repo market)
    initial_price = 100.0  # Initial asset price P_0
    asset_units = 10.0  # Leveraged fund asset holdings Q = 10 units
    initial_equity = 150.0  # Fund initial capital E_0 = $150
    # Fund balance sheet: Assets = 10 * 100 = $1,000; Debt = $850; Margin haircut = 15%
    initial_margin_rate = 0.15  # m_0 = 15%

    # Liquidity parameters
    price_impact_lambda = 0.50  # Price drop per unit of asset fire-sold: dP = -lambda * S
    margin_sensitivity_gamma = 0.005  # Margin expansion sensitivity: m_t = m_0 + gamma * (P_0 - P_t)

    # Fundamental shock at t=1: exogenous 5% drop in asset fundamental value
    p_current = 95.0
    margin_rate = initial_margin_rate + margin_sensitivity_gamma * (initial_price - p_current)
    equity = initial_equity - asset_units * (initial_price - p_current)  # 150 - 10 * 5 = 100.0

    print("=== DYNAMIC LOSS & MARGIN SPIRAL SIMULATION (SIMULATED) ===")
    print(f"Initial State: Price = ${initial_price:.2f} | Margin Haircut = {initial_margin_rate * 100:.1f}%")
    print(
        f"Exogenous Shock: Price drops to ${p_current:.2f} (-5.0%) | "
        f"Fund Equity: ${equity:.2f} (from ${initial_equity:.2f})"
    )

    history: list[tuple[int, float, float, float, float]] = []
    # (iteration, price, margin_rate, equity, sales)

    tolerance = 1e-5
    max_iter = 20

    for step in range(1, max_iter + 1):
        # Fund equity must cover margin requirement: Equity >= margin_rate * (Q * Price)
        # Required capital: C_req = margin_rate * asset_units * p_current
        # If Equity < C_req, fund must liquidate assets Delta S:
        # Equity >= margin_rate * (asset_units - Delta S) * p_current
        # ==> Delta S = asset_units - Equity / (margin_rate * p_current)
        max_sustainable_units = equity / (margin_rate * p_current) if (margin_rate * p_current) > 0.0 else 0.0
        forced_sales = max(0.0, asset_units - max_sustainable_units)

        history.append((step, p_current, margin_rate, equity, forced_sales))

        if forced_sales < tolerance:
            break

        # Execute forced sales
        asset_units -= forced_sales
        p_next = p_current - price_impact_lambda * forced_sales
        # Losses from fire sales further reduce equity
        price_drop_step = p_current - p_next
        equity -= asset_units * price_drop_step
        # Margin haircut expands further with price decline
        margin_rate = min(0.60, initial_margin_rate + margin_sensitivity_gamma * (initial_price - p_next))
        p_current = p_next

    print(f"\nSpiral converged in {len(history)} rounds:")
    for step, p_val, m_val, e_val, s_val in history[:6]:
        print(
            f"  Round {step:02d}: Price = ${p_val:.4f} | Haircut = {m_val * 100:.2f}% | "
            f"Equity = ${e_val:.2f} | Forced Sales = {s_val:.4f} units"
        )

    p_final = history[-1][1]
    total_drop_pct = (initial_price - p_final) / initial_price * 100.0
    print(f"\nFinal Equilibrium Price: ${p_final:.4f} (Total decline: {total_drop_pct:.2f}%)")

    # Analytical feedback multiplier check
    # Initial sensitivity: dSales/dP = -asset_units / (m * P)
    # Price impact: dP/dSales = -lambda
    # Multiplier: M = 1 / [1 - lambda * (1 / (m * P))]
    loop_gain = price_impact_lambda * (1.0 / (initial_margin_rate * initial_price))
    multiplier = 1.0 / (1.0 - loop_gain) if loop_gain < 1.0 else float("inf")
    print(f"Analytical Loop Gain (lambda / (m*P)): {loop_gain:.4f}")
    print(f"Feedback Multiplier: {multiplier:.4f}")


main()
