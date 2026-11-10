"""Fail to account for non-borrowed downside payoff when calculating marginal buyer indifference.

The student incorrectly sets h* = R_f / (R_f + v_u - v_d) regardless of max_loan_ratio theta.
"""


def solve_geanakoplos_equilibrium(
    v_u: float,
    v_d: float,
    risk_free_rate: float = 1.0,
    max_loan_ratio: float = 1.0,
) -> dict[str, float]:
    if v_d <= 0.0 or v_u <= v_d or risk_free_rate < 1.0 or not (0.0 < max_loan_ratio <= 1.0):
        raise ValueError("Invalid parameters")

    loan = (max_loan_ratio * v_d) / risk_free_rate
    # WRONG: ignores (1 - theta) * v_d term in numerator
    marginal_buyer = risk_free_rate / (risk_free_rate + (v_u - v_d))
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
    if shocked_loan_ratio > initial_loan_ratio:
        raise ValueError("shocked_loan_ratio must be <= initial_loan_ratio")

    eq_initial = solve_geanakoplos_equilibrium(v_u, v_d, risk_free_rate, initial_loan_ratio)
    eq_shocked = solve_geanakoplos_equilibrium(v_u, v_d, risk_free_rate, shocked_loan_ratio)
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
    if v_ud <= 0.0 or v_dd <= 0.0 or v_uu <= v_ud or v_du <= v_dd:
        raise ValueError("Invalid parameters")

    eq_u = solve_geanakoplos_equilibrium(v_uu, v_ud, risk_free_rate, 1.0)
    eq_d = solve_geanakoplos_equilibrium(v_du, v_dd, risk_free_rate, 1.0)
    p_u = eq_u["price"]
    p_d = eq_d["price"]
    eq_0 = solve_geanakoplos_equilibrium(p_u, p_d, risk_free_rate, 1.0)
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
