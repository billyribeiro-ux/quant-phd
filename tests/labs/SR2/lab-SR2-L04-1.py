"""Lab SR2-L04-1: Multi-Period Leverage Cycle Simulation.

Simulates the full multi-period leverage cycle of Geanakoplos (2010) across tranquil
expansion, bad-news volatility shock, margin spike, and wealth redistribution.
"""


def solve_node_equilibrium(vu: float, vd: float, rf: float = 1.0) -> tuple[float, float, float]:
    """Calculate price, loan, and marginal buyer in collateral equilibrium."""
    loan = vd / rf
    h_star = rf / (rf + (vu - vd))
    price = loan + (1.0 - h_star)
    return price, loan, h_star


def main() -> None:
    # Terminal payoffs at t=2 (SIMULATED macroeconomic states)
    # Under tranquil expectations at t=0, future volatility is perceived as low
    # Path UU: boom continues; Path UD: mild dip
    # Path DU: volatile recovery; Path DD: deep recession
    v_uu = 2.40
    v_ud = 1.60
    v_du = 1.20
    v_dd = 0.30
    rf = 1.00

    print("=== MULTI-PERIOD LEVERAGE CYCLE TREE (SIMULATED) ===")
    print(f"Terminal Payoffs: V_UU=${v_uu:.2f}, V_UD=${v_ud:.2f}, V_DU=${v_du:.2f}, V_DD=${v_dd:.2f}")

    # Step 1: Solve t=1 subgame equilibria
    p_u, loan_u, h_u = solve_node_equilibrium(v_uu, v_ud, rf)
    p_d, loan_d, h_d = solve_node_equilibrium(v_du, v_dd, rf)

    margin_u = p_u - loan_u
    lev_u = p_u / margin_u
    margin_d = p_d - loan_d
    lev_d = p_d / margin_d

    print("\n--- Period t=1 Conditional Equilibria ---")
    print(
        f"Good News State U: Price P_U = ${p_u:.4f} | Loan = ${loan_u:.4f} | Leverage = {lev_u:.2f}x | h*_U = {h_u:.4f}"
    )
    print(
        f"Bad News State D:  Price P_D = ${p_d:.4f} | Loan = ${loan_d:.4f} | Leverage = {lev_d:.2f}x | h*_D = {h_d:.4f}"
    )

    # Step 2: Solve t=0 equilibrium where asset delivers (P_U, P_D) at t=1
    p_0, loan_0, h_0 = solve_node_equilibrium(p_u, p_d, rf)
    margin_0 = p_0 - loan_0
    lev_0 = p_0 / margin_0
    haircut_0 = margin_0 / p_0

    print("\n--- Period t=0 Initial Boom Equilibrium ---")
    print(f"Asset Price P_0: ${p_0:.4f}")
    print(f"Collateralized Loan L_0: ${loan_0:.4f}")
    print(f"Required Margin m_0: ${margin_0:.4f} | Haircut: {haircut_0 * 100:.2f}%")
    print(f"Equilibrium Leverage: {lev_0:.2f}x | Marginal Buyer h*_0: {h_0:.4f}")

    # Step 3: Crisis dynamics when State D is realized at t=1
    # Leveraged optimists borrowed L_0 = P_D backed by the asset.
    # At t=1 in State D, the asset is worth P_D, exactly equal to the debt owed L_0.
    optimist_equity_at_1 = p_d - loan_0  # exactly 0.0
    price_crash = p_0 - p_d
    price_crash_pct = (price_crash / p_0) * 100.0

    print("\n--- Period t=1 Crash Dynamics (Bad News State D Realized) ---")
    print(f"Asset Price Collapse: ${p_0:.4f} ==> ${p_d:.4f} (-{price_crash_pct:.2f}%)")
    print(f"Optimist Equity Remaining: ${optimist_equity_at_1:.4f} (100% equity wipeout)")
    print(f"Haircut at t=1 in State D: {(margin_d / p_d) * 100:.2f}% (widened from {haircut_0 * 100:.2f}% at t=0)")
    print(f"Leverage Collapses from {lev_0:.2f}x at t=0 to {lev_d:.2f}x at t=1")


main()
