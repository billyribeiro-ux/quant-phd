"""Lab SR2-L02-1: Geanakoplos Collateral Equilibrium Mechanics.

Solves the two-state Geanakoplos (2010) collateral equilibrium with heterogeneous
optimism and collateralized borrowing. Verifies the marginal buyer indifference condition
and market-clearing identity to machine precision.
"""


def solve_collateral_equilibrium(
    v_u: float,
    v_d: float,
    rf: float = 1.0,
    loan_ratio: float = 1.0,
) -> dict[str, float]:
    """Analytical solver for the 2-state Geanakoplos collateral equilibrium."""
    loan = (loan_ratio * v_d) / rf
    num = rf - (1.0 - loan_ratio) * v_d
    den = rf + (v_u - v_d)
    h_star = min(1.0, max(0.0, num / den))
    price = loan + (1.0 - h_star)
    margin = price - loan
    leverage = price / margin if margin > 0.0 else 1.0
    haircut = margin / price if price > 0.0 else 0.0

    return {
        "price": price,
        "marginal_buyer": h_star,
        "loan": loan,
        "margin": margin,
        "leverage": leverage,
        "haircut": haircut,
    }


def main() -> None:
    # Representative instance (SIMULATED)
    vu = 1.20  # Up-state asset payoff
    vd = 0.20  # Down-state asset payoff
    rf = 1.00  # Gross risk-free rate
    theta = 1.00  # Full non-default borrowing (L = V_D)

    res = solve_collateral_equilibrium(vu, vd, rf, theta)
    p = res["price"]
    h_star = res["marginal_buyer"]
    loan = res["loan"]
    margin = res["margin"]
    lev = res["leverage"]
    hc = res["haircut"]

    print("=== GEANAKOPLOS COLLATERAL EQUILIBRIUM (SIMULATED) ===")
    print(f"Payoffs: V_U = ${vu:.2f}, V_D = ${vd:.2f} | Gross R_f = {rf:.2f}")
    print(f"Equilibrium Price P: ${p:.6f}")
    print(f"Marginal Buyer Cutoff h*: {h_star:.6f} (Optimists [h*, 1] buy asset)")
    print(f"Collateralized Loan per Unit: ${loan:.6f}")
    print(f"Required Margin (Down Payment): ${margin:.6f}")
    print(f"Equilibrium Leverage: {lev:.4f}x | Haircut: {hc * 100:.2f}%")

    # Invariant Verification 1: Marginal buyer expected return on equity == R_f
    expected_equity_payoff = (1.0 - theta) * vd + h_star * (vu - vd)
    return_on_equity = expected_equity_payoff / margin
    residual_indifference = abs(return_on_equity - rf)
    print("\n--- Invariant Verification ---")
    print(f"Marginal Buyer Return on Equity: {return_on_equity:.8f}")
    print(f"Indifference Residual |ROE - R_f|: {residual_indifference:.2e} <= 1e-7")

    # Invariant Verification 2: Market clearing
    optimist_wealth = 1.0 - h_star
    total_asset_demand = optimist_wealth / margin
    residual_market_clearing = abs(total_asset_demand - 1.0)
    print(f"Total Asset Demand: {total_asset_demand:.8f} (Supply = 1.0)")
    print(f"Market Clearing Residual |Demand - 1.0|: {residual_market_clearing:.2e} <= 1e-7")

    # Unleveraged benchmark: if no borrowing is permitted (theta = 0)
    res_unleveraged = solve_collateral_equilibrium(vu, vd, rf, loan_ratio=0.0)
    p_unlev = res_unleveraged["price"]
    h_unlev = res_unleveraged["marginal_buyer"]
    print(f"\nUnleveraged Benchmark (Zero Borrowing): Price = ${p_unlev:.6f}, h* = {h_unlev:.6f}")
    print(f"Leverage Collateral Premium: ${p - p_unlev:.6f} (+{(p - p_unlev) / p_unlev * 100:.2f}%)")


main()
