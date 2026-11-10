"""Lab CR3-L05-1: Leveraged Loan Restructuring and Cov-Lite Recovery Impairment.

SIMULATED: models default loss waterfalls in syndicated leveraged loans, comparing
traditional maintenance covenants against covenant-lite (cov-lite) structures
and analyzing the impact of EBITDA add-backs on reported versus true leverage.
"""

from __future__ import annotations


def calculate_waterfall(
    initial_debt: float,
    cash_ebitda: float,
    addback_pct: float,
    senior_share: float,
    distress_drop: float,
    cov_lite: bool,
) -> dict[str, float]:
    """Calculate loan restructuring recovery rates."""
    reported_ebitda = cash_ebitda * (1.0 + addback_pct)
    distressed_ebitda = max(1e-6, cash_ebitda * (1.0 - distress_drop))

    reported_leverage = initial_debt / reported_ebitda
    actual_leverage = initial_debt / cash_ebitda

    # Enterprise valuation at restructuring: multiple of 7.0x distressed EBITDA
    base_ev = distressed_ebitda * 7.0
    # Cov-lite delay permits equity burn-through and asset stripping, causing 35% EV erosion
    ev = base_ev * 0.65 if cov_lite else base_ev

    senior_debt = initial_debt * senior_share
    junior_debt = initial_debt * (1.0 - senior_share)

    senior_rec = min(senior_debt, ev)
    rem_ev = max(0.0, ev - senior_rec)
    junior_rec = min(junior_debt, rem_ev)

    senior_recovery_rate = senior_rec / senior_debt
    junior_recovery_rate = junior_rec / junior_debt if junior_debt > 0 else 1.0
    total_recovery_rate = (senior_rec + junior_rec) / initial_debt

    return {
        "reported_leverage": reported_leverage,
        "actual_leverage": actual_leverage,
        "enterprise_value": ev,
        "senior_rec": senior_recovery_rate,
        "junior_rec": junior_recovery_rate,
        "total_rec": total_recovery_rate,
    }


def main() -> None:
    initial_debt = 600.0
    cash_ebitda = 100.0
    addback_pct = 0.30  # 30% add-backs
    senior_share = 0.80  # 80% First Lien, 20% Second Lien
    distress_scenarios = [0.20, 0.40, 0.60]

    print("Leveraged Loan Default Waterfall: Maintenance vs Cov-Lite Underwriting:")
    print("  Distress | Covenant Type | EV ($M) | Senior Recovery | Junior Recovery | Total Recovery")
    print("-----------+---------------+---------+-----------------+-----------------+---------------")

    for dist in distress_scenarios:
        for cov_lite in [False, True]:
            res = calculate_waterfall(initial_debt, cash_ebitda, addback_pct, senior_share, dist, cov_lite)
            label = "Cov-Lite   " if cov_lite else "Maintenance"
            s_rec = res["senior_rec"] * 100
            j_rec = res["junior_rec"] * 100
            t_rec = res["total_rec"] * 100
            ev_val = res["enterprise_value"]
            print(
                f"    {dist * 100:2.0f}%    |  {label}  |  {ev_val:5.1f}  |     "
                f"{s_rec:5.1f}%     |      {j_rec:5.1f}%     |     {t_rec:5.1f}%"
            )

    # Leverage distortion from add-backs
    base_res = calculate_waterfall(initial_debt, cash_ebitda, addback_pct, senior_share, 0.40, True)
    print("\nEBITDA Add-Back Leverage Distortion:")
    print(f"  Reported Debt / EBITDA (with add-backs): {base_res['reported_leverage']:.2f}x")
    print(f"  True Cash Debt / EBITDA:                 {base_res['actual_leverage']:.2f}x")

    assert base_res["actual_leverage"] > base_res["reported_leverage"]


main()
