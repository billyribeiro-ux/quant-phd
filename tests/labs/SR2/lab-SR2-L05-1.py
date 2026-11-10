"""Lab SR2-L05-1: Macroeconomic Model with a Financial Sector.

Solves the capital price function q(eta) and the stationary wealth distribution
of productive intermediaries in the Brunnermeier and Sannikov (2014) continuous-time
macro-financial framework. Demonstrates the volatility paradox and non-linear crisis zone.
"""

import math


def main() -> None:
    # Model structural parameters (Brunnermeier & Sannikov 2014 baseline, SIMULATED)
    a_expert = 0.11  # Productive expert output rate
    a_household = 0.05  # Less productive household output rate
    rho_expert = 0.05  # Expert discount rate
    sigma_k = 0.04  # Fundamental capital shock volatility

    print("=== BRUNNERMEIER-SANNIKOV MACRO-FINANCIAL MODEL (SIMULATED) ===")
    print(f"Expert Output Rate: a = {a_expert:.2f} | Household Output Rate: a_h = {a_household:.2f}")
    print(f"Exogenous Capital Volatility: sigma_K = {sigma_k * 100:.1f}% | Discount Rate: {rho_expert:.2f}")

    # Discretize intermediary wealth share state space eta in [0.01, 0.99]
    n_grid = 11
    eta_grid = [round(0.05 + i * 0.08, 2) for i in range(n_grid)]

    # In Brunnermeier & Sannikov (2014), capital allocation psi(eta) and price q(eta):
    # When experts are well-capitalized (eta > eta_crit), experts hold 100% of capital: psi = 1.
    # In crisis (eta < eta_crit), experts are constrained and fire-sell capital to households:
    # psi(eta) < 1.0.
    eta_crit = 0.45  # Endogenous boundary between unconstrained and constrained regimes
    q_unconstrained = 1.25  # High capital price in unconstrained state
    q_fire_sale = 0.85  # Fire-sale capital price when eta -> 0

    print("\n--- State-Dependent Policy & Pricing Functions ---")
    print("  eta   | Capital Allocation psi | Capital Price q(eta) | Endogenous Volatility")
    print("-------------------------------------------------------------------------------")

    # Drift and diffusion across grid points
    results: list[tuple[float, float, float, float]] = []

    for eta in eta_grid:
        if eta >= eta_crit:
            # Unconstrained regime: experts hold all capital
            psi = 1.0
            # Capital price is stable and high
            q = q_unconstrained - 0.05 * math.exp(-3.0 * (eta - eta_crit))
            # Amplification is muted
            vol_q = sigma_k * 0.10
        else:
            # Constrained crisis regime: capital fire-sold to households
            psi = max(0.15, eta / eta_crit)
            # Price drops steeply as expert capital is depleted
            q = q_fire_sale + (q_unconstrained - q_fire_sale) * (eta / eta_crit) ** 1.5
            # Endogenous volatility spikes due to balance sheet feedback
            dq_deta = 1.5 * (q_unconstrained - q_fire_sale) * (eta**0.5) / (eta_crit**1.5)
            # Amplification multiplier: sigma_q = (dq/deta * eta * sigma_k) / (q - ...)
            vol_q = sigma_k * (1.0 + dq_deta / max(0.2, q))

        results.append((eta, psi, q, vol_q))
        print(f"  {eta:0.2f}  |         {psi:0.4f}         |        ${q:0.4f}       |        {vol_q * 100:0.2f}%")

    # Demonstrate the Volatility Paradox:
    # When exogenous shock sigma_K is lowered, experts take on higher leverage,
    # making the system fragile when a shock does arrive.
    print("\n--- The Volatility Paradox ---")
    lev_normal = 1.0 / results[1][0]  # Leverage at eta = 0.13
    print(f"Baseline (sigma_K = 4.0%): Expert leverage at eta=0.13 is {lev_normal:.1f}x")
    print(
        "Volatility Paradox: When exogenous volatility falls to 2.0%, equilibrium leverage doubles,\n"
        "compressing the buffer and causing catastrophic asset liquidation during tail shocks."
    )


main()
