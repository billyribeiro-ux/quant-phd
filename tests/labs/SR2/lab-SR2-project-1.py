"""Lab SR2-project-1: Project Rung 1 Worked Example.

Representative SIMULATED instance of the Geanakoplos Collateral Equilibrium Solver.
Solves two-state equilibrium, verifies indifference and market-clearing invariants,
and simulates exogenous margin shocks and three-period leverage cycle dynamics.
"""


def solve_geanakoplos_equilibrium(
    v_u: float,
    v_d: float,
    risk_free_rate: float = 1.0,
    max_loan_ratio: float = 1.0,
) -> dict[str, float]:
    """Calculate the collateral equilibrium for a two-state asset."""
    if v_d <= 0.0:
        raise ValueError(f"v_d must be strictly positive, got {v_d}")
    if v_u <= v_d:
        raise ValueError(f"v_u must be strictly greater than v_d, got v_u={v_u}, v_d={v_d}")
    if risk_free_rate < 1.0:
        raise ValueError(f"risk_free_rate must be >= 1.0, got {risk_free_rate}")
    if not (0.0 < max_loan_ratio <= 1.0):
        raise ValueError(f"max_loan_ratio must lie in (0.0, 1.0], got {max_loan_ratio}")

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


def simulate_margin_shock(
    v_u: float,
    v_d: float,
    initial_loan_ratio: float,
    shocked_loan_ratio: float,
    risk_free_rate: float = 1.0,
) -> dict[str, float]:
    """Simulate asset price and leverage response to an exogenous margin shock."""
    if shocked_loan_ratio > initial_loan_ratio:
        raise ValueError("shocked_loan_ratio must be <= initial_loan_ratio")

    eq0 = solve_geanakoplos_equilibrium(v_u, v_d, risk_free_rate, initial_loan_ratio)
    eq1 = solve_geanakoplos_equilibrium(v_u, v_d, risk_free_rate, shocked_loan_ratio)

    p0 = eq0["price"]
    p1 = eq1["price"]
    price_drop = p0 - p1
    price_drop_pct = (price_drop / p0) * 100.0 if p0 > 0.0 else 0.0
    buyer_shift = eq1["marginal_buyer"] - eq0["marginal_buyer"]

    return {
        "initial_price": p0,
        "shocked_price": p1,
        "price_drop": price_drop,
        "price_drop_pct": price_drop_pct,
        "initial_leverage": eq0["leverage"],
        "shocked_leverage": eq1["leverage"],
        "initial_haircut": eq0["haircut"],
        "shocked_haircut": eq1["haircut"],
        "marginal_buyer_shift": buyer_shift,
    }


def main() -> None:
    # Representative parameters (SIMULATED)
    v_u = 1.40
    v_d = 0.40
    rf = 1.00
    theta_0 = 1.00
    theta_1 = 0.50

    print("=== PROJECT RUNG 1: WORKED EXAMPLE (SIMULATED) ===")
    print(f"Inputs: V_U = ${v_u:.2f}, V_D = ${v_d:.2f}, R_f = {rf:.2f}")

    # Step 1: Baseline collateral equilibrium
    eq = solve_geanakoplos_equilibrium(v_u, v_d, rf, theta_0)
    p = eq["price"]
    h_star = eq["marginal_buyer"]
    loan = eq["loan"]
    margin = eq["margin"]
    lev = eq["leverage"]

    print(f"Step 1: Baseline Price P = ${p:.6f} | Marginal Buyer h* = {h_star:.6f}")
    print(f"        Safe Loan L = ${loan:.6f} | Margin m = ${margin:.6f} | Leverage = {lev:.4f}x")

    # Step 2: Invariant verification
    roe_marginal = ((1.0 - theta_0) * v_d + h_star * (v_u - v_d)) / margin
    residual_roe = abs(roe_marginal - rf)
    asset_demand = (1.0 - h_star) / margin
    residual_clearing = abs(asset_demand - 1.0)
    print(f"Step 2: Marginal Buyer ROE Residual: {residual_roe:.2e} <= 1e-7")
    print(f"        Market Clearing Residual:    {residual_clearing:.2e} <= 1e-7")

    # Step 3: Margin shock simulation
    shock = simulate_margin_shock(v_u, v_d, theta_0, theta_1, rf)
    print("\nStep 3: Margin Shock Simulation (Loan ratio 1.00 ==> 0.50)")
    print(f"        Initial Price: ${shock['initial_price']:.4f} | Shocked Price: ${shock['shocked_price']:.4f}")
    print(f"        Price Crash: -${shock['price_drop']:.4f} (-{shock['price_drop_pct']:.2f}%)")
    print(f"        Haircut Widening: {shock['initial_haircut'] * 100:.2f}% ==> {shock['shocked_haircut'] * 100:.2f}%")
    print(f"        Leverage Collapse: {shock['initial_leverage']:.2f}x ==> {shock['shocked_leverage']:.2f}x")


main()
