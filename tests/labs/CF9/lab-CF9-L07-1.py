"""CF9 lab L07-1: Cross-Border Capital Budgeting - Home vs. Foreign Currency Methods.

Evaluates an international capital investment project:
1. Method 1 (Foreign Currency): Discount in foreign currency at foreign WACC, convert at spot.
2. Method 2 (Home Currency): Convert cash flows via forward rates (CIP), discount at home WACC.
3. Proves exact mathematical equivalence between the two valuation approaches.
4. Models political and expropriation risk via probability trees and country risk spreads.
Standard library only; deterministic execution.
"""

from __future__ import annotations


def evaluate_cross_border_project(
    initial_outlay_eur: float = 50_000_000.0,
    cash_flows_eur: list[float] | None = None,
    s0: float = 1.1000,
    r_usd: float = 0.05,
    r_eur: float = 0.04,
    wacc_usd: float = 0.10,
    country_risk_spread: float = 0.02,
    annual_expropriation_prob: float = 0.03,
) -> dict[str, float]:
    """Value cross-border project using Home Currency and Foreign Currency methods."""
    if cash_flows_eur is None:
        cash_flows_eur = [15_000_000.0, 20_000_000.0, 25_000_000.0, 20_000_000.0]

    n_years = len(cash_flows_eur)

    # 1. Foreign WACC derived from International Fisher / Interest Parity
    # (1 + WACC_EUR) = (1 + WACC_USD) * (1 + r_eur) / (1 + r_usd)
    wacc_eur = ((1.0 + wacc_usd) * (1.0 + r_eur) / (1.0 + r_usd)) - 1.0

    # ==========================================
    # METHOD 1: Foreign-Currency Approach
    # ==========================================
    # Discount EUR cash flows at foreign WACC
    pv_eur = sum(cf / ((1.0 + wacc_eur) ** (t + 1)) for t, cf in enumerate(cash_flows_eur))
    npv_eur = -initial_outlay_eur + pv_eur
    npv_method1_usd = npv_eur * s0

    # ==========================================
    # METHOD 2: Home-Currency Approach
    # ==========================================
    # Convert foreign cash flows to USD using forward rates: F_t = S_0 * ((1 + r_usd) / (1 + r_eur))^t
    forward_rates = [s0 * (((1.0 + r_usd) / (1.0 + r_eur)) ** (t + 1)) for t in range(n_years)]
    cash_flows_usd = [cf * fwd for cf, fwd in zip(cash_flows_eur, forward_rates, strict=True)]
    initial_outlay_usd = initial_outlay_eur * s0

    pv_usd = sum(cf / ((1.0 + wacc_usd) ** (t + 1)) for t, cf in enumerate(cash_flows_usd))
    npv_method2_usd = -initial_outlay_usd + pv_usd

    parity_gap = abs(npv_method1_usd - npv_method2_usd)

    # ==========================================
    # POLITICAL RISK & SOVEREIGN SPREAD
    # ==========================================
    # Approach A: Hurdle rate adjustment (+ sovereign spread)
    wacc_usd_adjusted = wacc_usd + country_risk_spread
    pv_usd_spread = sum(cf / ((1.0 + wacc_usd_adjusted) ** (t + 1)) for t, cf in enumerate(cash_flows_usd))
    npv_usd_spread = -initial_outlay_usd + pv_usd_spread

    # Approach B: Explicit probability of survival (1 - p)^t
    # In each year, cash flow is received only if no expropriation has occurred
    cf_expected_survival = [cf * ((1.0 - annual_expropriation_prob) ** (t + 1)) for t, cf in enumerate(cash_flows_usd)]
    pv_usd_survival = sum(cf / ((1.0 + wacc_usd) ** (t + 1)) for t, cf in enumerate(cf_expected_survival))
    npv_usd_survival = -initial_outlay_usd + pv_usd_survival

    return {
        "wacc_usd": wacc_usd,
        "wacc_eur": wacc_eur,
        "npv_eur": npv_eur,
        "npv_method1_usd": npv_method1_usd,
        "npv_method2_usd": npv_method2_usd,
        "parity_gap": parity_gap,
        "npv_usd_spread": npv_usd_spread,
        "npv_usd_survival": npv_usd_survival,
    }


def main() -> None:
    print("CF9 Lab L07-1: Cross-Border Capital Budgeting")
    print("=============================================")

    res = evaluate_cross_border_project()

    print("1. Cost of Capital Parity Derivation:")
    print(f"   Domestic WACC (USD):              {res['wacc_usd']:.2%}")
    print(f"   Implied Foreign WACC (EUR):       {res['wacc_eur']:.4%}")

    print("\n2. Valuation Equivalence (Frictionless Parity):")
    print(f"   Foreign Currency Method (EUR NPV):€{res['npv_eur']:,.2f}")
    print(f"   Converted to USD at Spot (S0):    ${res['npv_method1_usd']:,.2f}")
    print(f"   Home Currency Method (USD NPV):   ${res['npv_method2_usd']:,.2f}")
    print(f"   Parity Discrepancy Wedge:         ${res['parity_gap']:,.6f} (Exact Parity: {res['parity_gap'] < 1e-4})")

    print("\n3. Political and Country Risk Adjustments:")
    print(f"   Baseline NPV (Zero Country Risk): ${res['npv_method1_usd']:,.2f}")
    print(f"   NPV with +200 bps Country Spread: ${res['npv_usd_spread']:,.2f}")
    print(f"   NPV with 3% Annual Expropriation: ${res['npv_usd_survival']:,.2f}")
    print(f"   Expropriation Value Haircut:      ${res['npv_method1_usd'] - res['npv_usd_survival']:,.2f}")


main()
