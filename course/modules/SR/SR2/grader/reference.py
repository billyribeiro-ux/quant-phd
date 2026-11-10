"""Reference solution for SR2 project: Leverage-cycle model.

Implements the Geanakoplos collateral-equilibrium solver and margin-shock simulation.
"""


def solve_geanakoplos_equilibrium(
    v_u: float,
    v_d: float,
    risk_free_rate: float = 1.0,
    max_loan_ratio: float = 1.0,
) -> dict[str, float]:
    """Calculate the collateral equilibrium for a two-state asset.

    Parameters
    ----------
    v_u : float
        Asset payoff in the up state (V_U > V_D > 0).
    v_d : float
        Asset payoff in the down state (V_D > 0).
    risk_free_rate : float
        Gross risk-free interest rate (R_f >= 1.0). Default is 1.0.
    max_loan_ratio : float
        Fraction theta in (0, 1] of worst-case payoff lenders are willing to lend.

    Returns
    -------
    dict[str, float]
        Dictionary containing equilibrium price, marginal buyer cutoff,
        loan amount, required margin, leverage ratio, and haircut.
    """
    if v_d <= 0.0:
        raise ValueError(f"v_d must be strictly positive, got {v_d}")
    if v_u <= v_d:
        raise ValueError(f"v_u must be strictly greater than v_d, got v_u={v_u}, v_d={v_d}")
    if risk_free_rate < 1.0:
        raise ValueError(f"risk_free_rate must be >= 1.0, got {risk_free_rate}")
    if not (0.0 < max_loan_ratio <= 1.0):
        raise ValueError(f"max_loan_ratio must lie in (0.0, 1.0], got {max_loan_ratio}")

    # Maximum collateralized loan per unit of asset
    loan = (max_loan_ratio * v_d) / risk_free_rate

    # Indifference condition of marginal buyer h*:
    # Return on equity: [(1 - theta)*v_d + h*(v_u - v_d)] / (P - loan) = R_f
    # Market clearing: 1 - h* = P - loan
    # Combining yields: h* = [R_f - (1 - theta)*v_d] / [R_f + v_u - v_d]
    numerator = risk_free_rate - (1.0 - max_loan_ratio) * v_d
    denominator = risk_free_rate + (v_u - v_d)
    marginal_buyer = numerator / denominator

    # Boundary clamp for marginal buyer to [0, 1]
    marginal_buyer = min(1.0, max(0.0, marginal_buyer))

    # Equilibrium price
    price = loan + (1.0 - marginal_buyer)
    margin = price - loan
    leverage = price / margin if margin > 0.0 else 1.0
    haircut = margin / price if price > 0.0 else 0.0

    return {
        "price": price,
        "marginal_buyer": marginal_buyer,
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
    """Simulate the asset price and leverage response to an exogenous margin shock.

    Parameters
    ----------
    v_u : float
        Asset payoff in up state.
    v_d : float
        Asset payoff in down state.
    initial_loan_ratio : float
        Initial maximum loan ratio theta_0 in (0, 1].
    shocked_loan_ratio : float
        Post-shock maximum loan ratio theta_1 in (0, theta_0].
    risk_free_rate : float
        Gross risk-free rate.

    Returns
    -------
    dict[str, float]
        Initial and shocked equilibrium outcomes and comparative statistics.
    """
    if shocked_loan_ratio > initial_loan_ratio:
        raise ValueError("shocked_loan_ratio must be <= initial_loan_ratio")

    eq_initial = solve_geanakoplos_equilibrium(
        v_u=v_u,
        v_d=v_d,
        risk_free_rate=risk_free_rate,
        max_loan_ratio=initial_loan_ratio,
    )
    eq_shocked = solve_geanakoplos_equilibrium(
        v_u=v_u,
        v_d=v_d,
        risk_free_rate=risk_free_rate,
        max_loan_ratio=shocked_loan_ratio,
    )

    p0 = eq_initial["price"]
    p1 = eq_shocked["price"]
    price_drop = p0 - p1
    price_drop_pct = (price_drop / p0) * 100.0 if p0 > 0.0 else 0.0
    buyer_shift = eq_shocked["marginal_buyer"] - eq_initial["marginal_buyer"]

    return {
        "initial_price": p0,
        "shocked_price": p1,
        "price_drop": price_drop,
        "price_drop_pct": price_drop_pct,
        "initial_leverage": eq_initial["leverage"],
        "shocked_leverage": eq_shocked["leverage"],
        "initial_haircut": eq_initial["haircut"],
        "shocked_haircut": eq_shocked["haircut"],
        "marginal_buyer_shift": buyer_shift,
    }


def solve_three_period_cycle(
    v_uu: float,
    v_ud: float,
    v_du: float,
    v_dd: float,
    risk_free_rate: float = 1.0,
) -> dict[str, float]:
    """Solve a 3-period (t=0, 1, 2) leverage cycle tree.

    At t=1:
    - State U has continuation payoffs (v_uu, v_ud).
    - State D has continuation payoffs (v_du, v_dd).

    At t=0:
    - Continuation payoffs are (price_u, price_d).
    - Collateralized safe borrowing is backed by price_d.

    Returns
    -------
    dict[str, float]
        Equilibrium prices, loans, margins, and leverage at t=0 and across t=1 states.
    """
    if v_ud <= 0.0 or v_dd <= 0.0:
        raise ValueError("All terminal payoffs must be positive")
    if v_uu <= v_ud:
        raise ValueError("v_uu must exceed v_ud")
    if v_du <= v_dd:
        raise ValueError("v_du must exceed v_dd")

    # t=1 equilibrium in state U
    eq_u = solve_geanakoplos_equilibrium(v_uu, v_ud, risk_free_rate, max_loan_ratio=1.0)
    # t=1 equilibrium in state D
    eq_d = solve_geanakoplos_equilibrium(v_du, v_dd, risk_free_rate, max_loan_ratio=1.0)

    p_u = eq_u["price"]
    p_d = eq_d["price"]

    # t=0 equilibrium where asset delivers (p_u, p_d) at t=1
    eq_0 = solve_geanakoplos_equilibrium(p_u, p_d, risk_free_rate, max_loan_ratio=1.0)

    # Crash drop if state D is realized at t=1
    crash_drop = eq_0["price"] - p_d
    crash_drop_pct = (crash_drop / eq_0["price"]) * 100.0

    return {
        "p0": eq_0["price"],
        "l0": eq_0["loan"],
        "m0": eq_0["margin"],
        "leverage0": eq_0["leverage"],
        "p_u": p_u,
        "p_d": p_d,
        "crash_drop": crash_drop,
        "crash_drop_pct": crash_drop_pct,
    }
