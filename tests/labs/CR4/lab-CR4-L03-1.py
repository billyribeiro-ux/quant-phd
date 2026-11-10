"""Lab CR4-L03-1: Strategic Bargaining and Absolute Priority Rule Violations in Chapter 11.

Models strategic bargaining between senior impaired creditors and debtor equityholders
under Bankruptcy Code Section 1121 exclusivity.
Demonstrates why senior creditors concede consensual carve-outs to avoid administrative burn
and cramdown litigation costs under Section 1129(b).
"""

from __future__ import annotations


def solve_strategic_carveout(
    v_estate: float,
    d_senior: float,
    burn_rate_monthly: float,
    litigation_cost: float,
    delay_months: float,
    senior_bargaining_power: float,
) -> dict[str, float]:
    """Calculate equilibrium carve-out payment to equity under threat of delay and cramdown litigation.

    v_estate: Reorganization value before delay.
    d_senior: Senior creditor claim (d_senior > v_estate).
    burn_rate_monthly: Administrative and operational value erosion per month.
    litigation_cost: Direct legal, expert witness, and court expenses of a contested cramdown.
    delay_months: Duration of exclusivity dispute before cramdown confirmation.
    senior_bargaining_power: Share of delay-avoidance surplus captured by senior creditor (gamma in [0, 1]).
    """
    # In a cramdown without consensus, the estate suffers delay burn and litigation expenses
    total_delay_burn = burn_rate_monthly * delay_months
    cramdown_estate_value = max(0.0, v_estate - total_delay_burn - litigation_cost)

    # Under strict cramdown, senior creditor gets min(cramdown_estate_value, d_senior)
    senior_cramdown_payoff = min(cramdown_estate_value, d_senior)

    # Senior cost of litigation and delay
    senior_cost_of_fight = v_estate - senior_cramdown_payoff
    equity_carveout = (1.0 - senior_bargaining_power) * senior_cost_of_fight

    senior_consensual_payoff = v_estate - equity_carveout

    return {
        "v_estate": v_estate,
        "d_senior": d_senior,
        "delay_burn": total_delay_burn,
        "litigation_cost": litigation_cost,
        "senior_cramdown_payoff": senior_cramdown_payoff,
        "equity_carveout": equity_carveout,
        "senior_consensual_payoff": senior_consensual_payoff,
        "apr_violation_pct": (equity_carveout / v_estate) * 100.0,
    }


def main() -> None:
    # Stylized insolvent debtor: Reorganization value V = 100, Senior claim D = 140
    v_estate = 100.0
    d_senior = 140.0
    litigation_cost = 6.0
    senior_power = 0.60  # gamma = 0.60 (senior captures 60% of surplus)

    delays = [3.0, 6.0, 12.0, 18.0]
    burn_rates = [0.5, 1.0, 1.5]  # $M per month

    print("Strategic Chapter 11 Bargaining: Equilibrium Equity Carve-Out (APR Violation):")
    print("V = 100.0, D_senior = 140.0 (Firm Insolvent under strict APR), Litigation Cost = 6.0")
    print("Delay (mo) | Burn Rate ($M/mo) | Senior Cramdown | Senior Consensual | Equity Carve-Out | APR Viol (%)")
    print("-----------+--------------------+-----------------+-------------------+------------------+-------------")

    for delay in delays:
        for burn in burn_rates:
            res = solve_strategic_carveout(v_estate, d_senior, burn, litigation_cost, delay, senior_power)
            sc_cram = f"{res['senior_cramdown_payoff']:5.1f}"
            sc_cons = f"{res['senior_consensual_payoff']:5.1f}"
            eq_carv = f"{res['equity_carveout']:4.2f}"
            apr_v = f"{res['apr_violation_pct']:4.2f}%"
            d_s = f"{delay:4.1f}"
            b_s = f"{burn:4.1f}"
            row = (
                f"   {d_s}    |        {b_s}        |      {sc_cram}      |       {sc_cons}       |"
                f"       {eq_carv}       |    {apr_v}"
            )
            print(row)

    # Invariant checks:
    # 1. Consensual payoff strictly dominates cramdown payoff for senior creditor
    res_base = solve_strategic_carveout(v_estate, d_senior, 1.0, litigation_cost, 6.0, senior_power)
    assert res_base["senior_consensual_payoff"] > res_base["senior_cramdown_payoff"]
    # 2. Equity receives positive carve-out despite strict balance-sheet insolvency
    assert res_base["equity_carveout"] > 0.0
    # 3. Sum of payoffs equals total estate value
    assert abs(res_base["senior_consensual_payoff"] + res_base["equity_carveout"] - v_estate) < 1e-9

    print("\nVerified bargaining invariants:")
    print("1. Consensual agreement strictly dominates cramdown payoff for senior debt.")
    print("2. Equity extracts positive carve-out despite zero economic value under strict APR.")
    print("3. Conservation of estate value holds identically.")


main()
