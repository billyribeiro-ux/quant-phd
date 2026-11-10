"""Lab SR4-project-3: Project Rung 3 Case Generator and Calibration.

SIMULATED. Comprehensive 8-regime Regulatory Impact Analysis (RIA) model
quantifying dealer Treasury intermediation capacity, leverage shadow costs,
secondary market bid-ask spreads, and net social welfare across alternative
post-crisis regulatory designs (Federal Reserve Board, 2020, 2025; BCBS, 2014).
"""

from __future__ import annotations


def evaluate_regime(
    regime_id: int,
    name: str,
    equity: float,
    slr_ratio: float,
    non_treasury_assets: float,
    is_exempt: bool,
    cost_of_equity: float,
    annual_volume: float,
    annual_issuance: float,
    default_prob_annual: float,
    bailout_loss: float,
) -> dict[str, float | str | int]:
    """Evaluate dealer balance-sheet capacity, hurdle rates, and welfare for a single regime."""
    if equity <= 0 or slr_ratio <= 0:
        raise ValueError("equity and slr_ratio must be positive")

    # Total balance sheet capacity
    if is_exempt:
        # If Treasuries are exempt from SLR, dealer can expand up to risk-weighted capacity (~$1,200B)
        total_capacity = equity / slr_ratio + 400.0
        treasury_capacity = 600.0
        hurdle_bps = 0.0  # Zero shadow cost on zero-risk assets
        spread_bps = 0.20
        issuance_bps = 1.00
    else:
        total_capacity = equity / slr_ratio
        treasury_capacity = max(50.0, total_capacity - non_treasury_assets)
        hurdle_bps = slr_ratio * cost_of_equity * 10000.0  # in basis points (e.g. 0.05 * 0.12 * 10000 = 60.0 bps)
        capacity_factor = 400.0 / treasury_capacity
        spread_bps = 0.20 * capacity_factor
        issuance_bps = 1.00 * capacity_factor

    # Welfare components ($ billions / year)
    # Baseline comparison spread: 0.80 bps; baseline issuance concession: 4.00 bps
    spread_savings = max(0.0, 0.80 - spread_bps)
    liquidity_benefit = annual_volume * (spread_savings / 10000.0)

    issuance_savings = max(0.0, 4.00 - issuance_bps)
    debt_benefit = annual_issuance * (issuance_savings / 10000.0)

    expected_bailout = default_prob_annual * bailout_loss
    net_welfare = liquidity_benefit + debt_benefit - expected_bailout

    return {
        "regime_id": regime_id,
        "name": name,
        "slr_pct": slr_ratio * 100.0,
        "total_capacity": total_capacity,
        "treasury_capacity": treasury_capacity,
        "hurdle_bps": hurdle_bps,
        "spread_bps": spread_bps,
        "net_welfare": net_welfare,
    }


def main() -> None:
    # Industry-wide dealer parameters (SIMULATED)
    equity = 60.0  # $60B Tier 1 equity
    non_treasury = 750.0  # $750B existing non-Treasury loan and credit assets
    r_e = 0.12  # 12.0% cost of equity
    ann_vol = 150000.0  # $150T annual secondary volume
    ann_iss = 4000.0  # $4T annual gross Treasury issuance
    bailout_cost = 500.0  # $500B social bailout cost

    regimes_def = [
        (1, "Baseline G-SIB Holding Company (5.0% SLR)", 0.050, False, 0.0010),
        (2, "Insured Depository Institution Subsidiary (6.0% SLR)", 0.060, False, 0.0008),
        (3, "Recalibrated Buffer Proposal (4.0% SLR)", 0.040, False, 0.0012),
        (4, "Basel III International Minimum (3.0% SLR)", 0.030, False, 0.0016),
        (5, "2020 Emergency Temporary Exemption (5.0% SLR, Exempt)", 0.050, True, 0.0013),
        (6, "Permanent Safe-Asset Exemption + Surcharge (5.5% SLR, Exempt)", 0.055, True, 0.0011),
        (7, "Stress Window (Inbound Selling $250B, 5.0% SLR)", 0.050, False, 0.0018),
        (8, "Severe Crisis Shock (Inbound Selling $400B, 5.0% SLR)", 0.050, False, 0.0028),
    ]

    results = []
    for rid, name, slr, exempt, pd in regimes_def:
        res = evaluate_regime(
            regime_id=rid,
            name=name,
            equity=equity,
            slr_ratio=slr,
            non_treasury_assets=non_treasury,
            is_exempt=exempt,
            cost_of_equity=r_e,
            annual_volume=ann_vol,
            annual_issuance=ann_iss,
            default_prob_annual=pd,
            bailout_loss=bailout_cost,
        )
        results.append(res)

    print("=== PROJECT RUNG 3: 8-REGIME REGULATORY IMPACT ANALYSIS TABLE (SIMULATED) ===")
    print("Part A: Case Table")
    for r in results:
        rid = int(r["regime_id"])
        name = str(r["name"])
        slr = float(r["slr_pct"])
        t_cap = float(r["treasury_capacity"])
        hurdle = float(r["hurdle_bps"])
        welf = float(r["net_welfare"])
        print(
            f"  Regime {rid}: {name:<55} | SLR: {slr:4.1f}% | Treasury Cap: ${t_cap:6.1f}B | "
            f"Hurdle: {hurdle:5.1f} bps | Net Welfare: ${welf:5.2f}B"
        )

    t_caps = [float(r["treasury_capacity"]) for r in results]
    welfares = [float(r["net_welfare"]) for r in results]
    hurdles = [float(r["hurdle_bps"]) for r in results]

    print("\nPart B: Intermediation Capacity Summary")
    print(f"  Minimum Treasury Capacity: ${min(t_caps):.1f}B (Regime 2, 6.0% IDI SLR)")
    print(f"  Maximum Treasury Capacity: ${max(t_caps):.1f}B (Regime 4, 3.0% Basel Floor)")
    print(f"  Mean Treasury Capacity across 8 Regimes: ${sum(t_caps) / len(t_caps):.1f}B")

    print("\nPart C: Shadow Cost / Hurdle Rate Summary")
    print(f"  Peak Leverage Hurdle Rate: {max(hurdles):.1f} bps (Regime 2, 6.0% SLR)")
    print(f"  Exempt Leverage Hurdle Rate: {min(hurdles):.1f} bps (Regimes 5 and 6)")

    print("\nPart D: Social Welfare Maximization")
    best_idx = welfares.index(max(welfares))
    best_r = results[best_idx]
    baseline_welf = float(results[0]["net_welfare"])
    welf_gain = float(best_r["net_welfare"]) - baseline_welf
    print(f"  Optimal Policy Regime: Regime {best_r['regime_id']} ({best_r['name']})")
    print(f"  Max Net Social Welfare: ${float(best_r['net_welfare']):.2f}B / year")
    print(f"  Annual Welfare Gain over Baseline Status Quo: +${welf_gain:.2f}B / year")

    print("\nPart E: Elasticity of Treasury Capacity with Respect to SLR Ratio")
    # Arc elasticity between Baseline (Regime 1, 5%) and Recalibrated (Regime 3, 4%):
    # e = (delta_Cap / avg_Cap) / (delta_SLR / avg_SLR)
    c1, c3 = float(results[0]["treasury_capacity"]), float(results[2]["treasury_capacity"])
    s1, s3 = 0.05, 0.04
    delta_c = c3 - c1
    avg_c = (c1 + c3) / 2.0
    delta_s = s3 - s1
    avg_s = (s1 + s3) / 2.0
    elasticity = (delta_c / avg_c) / (delta_s / avg_s)
    print(f"  Arc Elasticity of Capacity (Regime 1 to 3): {elasticity:.4f}")


main()
