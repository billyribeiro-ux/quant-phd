"""Lab SR2-project-3: Project Rung 3 Comparative Statics and Parameter Sweep.

Performs parameter sweeps over collateral loan ratios, down-state payoffs, and
interest rates to quantify non-linear price and leverage elasticities in collateral equilibrium.
"""


def solve_geanakoplos_equilibrium(
    v_u: float,
    v_d: float,
    risk_free_rate: float = 1.0,
    max_loan_ratio: float = 1.0,
) -> dict[str, float]:
    """Calculate the collateral equilibrium for a two-state asset."""
    loan = (max_loan_ratio * v_d) / risk_free_rate
    num = risk_free_rate - (1.0 - max_loan_ratio) * v_d
    den = risk_free_rate + (v_u - v_d)
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
    # Baseline parameters (SIMULATED)
    v_u = 1.50
    v_d = 0.50
    rf = 1.00

    print("=== PROJECT RUNG 3: COMPARATIVE STATICS SWEEP (SIMULATED) ===")
    print(f"Asset Payoffs: V_U = ${v_u:.2f}, V_D = ${v_d:.2f} | R_f = {rf:.2f}")

    # Sweep loan ratio theta from 1.0 down to 0.0 (progressive margin tightening)
    loan_ratios = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]

    print("\nLoan Ratio theta | Price P  | Loan L   | Margin m | Leverage | Marginal Buyer h*")
    print("--------------------------------------------------------------------------------")
    for theta in loan_ratios:
        res = solve_geanakoplos_equilibrium(v_u, v_d, rf, theta)
        print(
            f"      {theta:0.2f}      | ${res['price']:0.4f} | ${res['loan']:0.4f} | "
            f"${res['margin']:0.4f} |  {res['leverage']:0.2f}x   |      {res['marginal_buyer']:0.4f}"
        )

    # Down-state payoff sensitivity sweep (V_D from 0.70 down to 0.10)
    print("\n--- Down-State Payoff Sensitivity (V_D from 0.70 down to 0.10, theta=1.0) ---")
    vd_grid = [0.70, 0.50, 0.30, 0.10]
    for vd_val in vd_grid:
        res_vd = solve_geanakoplos_equilibrium(v_u, vd_val, rf, 1.0)
        print(
            f"  V_D = ${vd_val:0.2f} | Price = ${res_vd['price']:0.4f} | "
            f"Loan = ${res_vd['loan']:0.4f} | Leverage = {res_vd['leverage']:0.2f}x | "
            f"h* = {res_vd['marginal_buyer']:0.4f}"
        )


main()
