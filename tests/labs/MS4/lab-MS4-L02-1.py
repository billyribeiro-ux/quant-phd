"""Lab MS4-L02-1: Anomaly returns net of trading costs across turnover tiers.

Computes monthly and annualized net returns, Sharpe erosion, and break-even trading cost
thresholds for canonical market anomalies (Novy-Marx & Velikov 2016; Patton & Weller 2020).
SIMULATED: empirical parameters calibrated to NYSE/AMEX/NASDAQ cross-sectional anomalies.
"""

from __future__ import annotations


def run_anomaly_cost_analysis() -> None:
    # Anomaly profiles: (name, monthly_turnover_frac, gross_alpha_bps, effective_half_spread_bps, vol_ann)
    # Annual turnover = monthly_turnover * 12
    anomalies = [
        ("Gross Profitability (Low Turnover)", 0.015, 38.0, 18.0, 0.12),
        ("Asset Growth (Medium Turnover)", 0.045, 42.0, 20.0, 0.14),
        ("Price Momentum (High Turnover)", 0.180, 68.0, 24.0, 0.18),
    ]

    print("Anomaly Strategy Cost and Net Alpha Comparison:")
    print("-----------------------------------------------------------------------------------------")

    for name, turnover, gross_bps, spread_bps, vol in anomalies:
        ann_turnover = turnover * 12.0
        # Monthly transaction cost in bps = 2 * turnover * spread_bps (round trip)
        cost_monthly_bps = 2.0 * turnover * spread_bps
        net_monthly_bps = gross_bps - cost_monthly_bps

        # Annualized gross and net returns
        gross_ann_pct = (gross_bps * 12.0) / 100.0
        cost_ann_pct = (cost_monthly_bps * 12.0) / 100.0
        net_ann_pct = (net_monthly_bps * 12.0) / 100.0

        # Sharpe ratios
        gross_sharpe = gross_ann_pct / (vol * 100.0)
        net_sharpe = net_ann_pct / (vol * 100.0)
        sharpe_retention = (net_sharpe / gross_sharpe) * 100.0 if gross_sharpe > 0 else 0.0

        # Break-even effective half-spread threshold: cost_monthly_bps = gross_bps
        # 2 * turnover * c_star = gross_bps => c_star = gross_bps / (2 * turnover)
        breakeven_spread_bps = gross_bps / (2.0 * turnover)

        print(f"Strategy: {name}")
        print(f"  Monthly Turnover:       {turnover * 100.0:.2f}% (Annual: {ann_turnover * 100.0:.2f}%)")
        print(f"  Gross Alpha:            {gross_bps:.2f} bps/mo ({gross_ann_pct:.2f}% ann)")
        print(f"  Trading Cost Drag:      {cost_monthly_bps:.2f} bps/mo ({cost_ann_pct:.2f}% ann)")
        print(f"  Net Alpha:              {net_monthly_bps:.2f} bps/mo ({net_ann_pct:.2f}% ann)")
        print(f"  Gross Sharpe Ratio:     {gross_sharpe:.4f}")
        print(f"  Net Sharpe Ratio:       {net_sharpe:.4f} ({sharpe_retention:.2f}% retention)")
        print(f"  Break-even Half-Spread: {breakeven_spread_bps:.2f} bps")
        print(f"  Viable Net of Cost:     {net_monthly_bps > 0.0}")
        print("-----------------------------------------------------------------------------------------")


def main() -> None:
    run_anomaly_cost_analysis()


main()
