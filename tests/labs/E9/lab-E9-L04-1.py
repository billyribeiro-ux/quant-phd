"""Lab 4: Sudden stops, real exchange rate collapse, and banking insolvency (Calvo 1998).

SIMULATED two-sector open economy. Standard library only.
Verifies the relative price adjustment of non-traded goods following a sudden stop,
the balance-sheet currency mismatch, and the threshold for banking crisis insolvency.
"""

from __future__ import annotations


def relative_nontraded_price(
    traded_output: float,
    capital_inflow: float,
    nontraded_output: float,
    traded_share: float,
) -> float:
    """Compute equilibrium relative price of non-traded goods p_N under Cobb-Douglas utility.

    Utility: u(c_T, c_N) = gamma * ln(c_T) + (1 - gamma) * ln(c_N).
    Equilibrium: p_N = [(1 - gamma) / gamma] * [ (y_T + FA) / y_N ]
    where c_T = y_T + FA and c_N = y_N.
    """
    if traded_share <= 0.0 or traded_share >= 1.0:
        msg = f"Traded expenditure share gamma must be in (0, 1), got {traded_share}"
        raise ValueError(msg)
    c_traded = traded_output + capital_inflow
    if c_traded <= 0.0:
        msg = f"Traded goods consumption must be positive: y_T + FA = {c_traded}"
        raise ValueError(msg)
    return ((1.0 - traded_share) / traded_share) * (c_traded / nontraded_output)


def bank_capital(
    price_nontraded: float,
    nontraded_loans: float,
    foreign_debt: float,
) -> float:
    """Compute banking sector equity capital.

    Assets are backed by non-traded sector revenues (valued at p_N),
    liabilities are denominated in foreign currency (traded goods):
    Capital = p_N * L_N - D*
    """
    return price_nontraded * nontraded_loans - foreign_debt


def main() -> None:
    # Model parameters
    y_t = 100.0  # Traded goods endowment
    y_n = 100.0  # Non-traded goods endowment
    gamma = 0.50  # Equal preference weights (gamma = 0.5 => (1 - gamma)/gamma = 1.0)

    # Banking balance sheet parameters
    l_n = 120.0  # Non-traded loans
    d_star = 110.0  # Foreign-currency liabilities (denominated in traded units)

    # 1. Pre-crisis baseline: Net capital inflow of +20 (FA = +20)
    fa_pre = 20.0
    p_n_pre = relative_nontraded_price(y_t, fa_pre, y_n, gamma)
    k_pre = bank_capital(p_n_pre, l_n, d_star)
    cap_ratio_pre = k_pre / (p_n_pre * l_n)

    # 2. Sudden Stop episode: Inflows reverse to net outflow of -20 (FA = -20)
    fa_post = -20.0
    p_n_post = relative_nontraded_price(y_t, fa_post, y_n, gamma)
    k_post = bank_capital(p_n_post, l_n, d_star)
    cap_ratio_post = k_post / (p_n_post * l_n)

    # 3. Calculate threshold capital flow causing bank insolvency (K = 0)
    # p_N * L_N - D* = 0 => p_N = D* / L_N
    # p_N = (y_T + FA*) / y_N => FA* = y_N * (D* / L_N) - y_T
    p_n_crit = d_star / l_n
    fa_crit = y_n * p_n_crit - y_t

    price_decline_pct = (p_n_post - p_n_pre) / p_n_pre * 100.0

    print("=== Calvo (1998) Sudden Stop & Banking Insolvency ===")
    print(f"Pre-Crisis Capital Inflow FA:     +{fa_pre:.2f}")
    print(f"Pre-Crisis Relative Price p_N:    {p_n_pre:.4f}")
    print(f"Pre-Crisis Bank Capital:          {k_pre:.4f}")
    print(f"Pre-Crisis Capital Ratio:         {cap_ratio_pre * 100.0:.2f}%")
    print("\n=== Post-Sudden Stop Capital Reversal ===")
    print(f"Post-Crisis Capital Flow FA:      {fa_post:.2f}")
    print(f"Post-Crisis Relative Price p_N:   {p_n_post:.4f}")
    print(f"Relative Price Decline:           {price_decline_pct:.2f}%")
    print(f"Post-Crisis Bank Capital:         {k_post:.4f}")
    print(f"Post-Crisis Capital Ratio:        {cap_ratio_post * 100.0:.2f}%")
    print("\n=== Insolvency Boundary Analysis ===")
    print(f"Critical Relative Price for K=0:  {p_n_crit:.4f}")
    print(f"Critical Capital Inflow FA*:      {fa_crit:.2f}")

    assert p_n_pre == 1.20, "Pre-crisis price must be 1.0 * (120 / 100) = 1.20"
    assert p_n_post == 0.80, "Post-crisis price must be 1.0 * (80 / 100) = 0.80"
    assert k_pre > 0.0, "Pre-crisis banking sector must be solvent"
    assert k_post < 0.0, "Post-crisis banking sector must be insolvent (banking crisis)"
    assert round(fa_crit, 2) == -8.33, "Critical FA* must be 100 * (110 / 120) - 100 = -8.33"


main()
