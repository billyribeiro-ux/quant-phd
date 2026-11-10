"""Lab GM4-L02-1: Relative-Value Curve Trade: Duration-Neutral Yield Curve Steepener.

Backtests a duration-neutral 3M/10Y Treasury curve steepener using historical US Treasury data
from ust_daily.csv (retrieved 2026-10-17). Demonstrates level isolation and slope capture.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


def load_treasury_data(filepath: Path) -> tuple[np.ndarray, np.ndarray, list[str]]:
    dates: list[str] = []
    r_3m: list[float] = []
    r_10y: list[float] = []
    with filepath.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                val_3m = float(row["tbill_3m"])
                val_10y = float(row["cmt_10y"])
                dates.append(row["date"])
                r_3m.append(val_3m)
                r_10y.append(val_10y)
            except ValueError, KeyError:
                continue
    return np.array(r_3m, dtype=np.float64), np.array(r_10y, dtype=np.float64), dates


def main() -> None:
    data_file = Path("data") / "ust_daily.csv"
    if not data_file.exists():
        data_file = Path("course/assets/data/market/ust_daily.csv")

    rates_3m, rates_10y, dates = load_treasury_data(data_file)
    n_days = len(rates_3m)

    # Yield curve slope: 10Y minus 3M in basis points
    slope_bps = (rates_10y - rates_3m) * 100.0

    # Daily changes in basis points
    delta_3m = np.diff(rates_3m) * 100.0
    delta_10y = np.diff(rates_10y) * 100.0

    # Duration assumptions: 3M duration = 0.25, 10Y duration = 7.85
    dur_3m = 0.25
    dur_10y = 7.85

    # DV01 per $1M notional: dur * 1e-4 * 1,000,000 = dur * 100 ($ per bp)
    dv01_3m = dur_3m * 100.0  # $25 / bp per $1M
    dv01_10y = dur_10y * 100.0  # $785 / bp per $1M

    # Duration-neutral hedge ratio: notional_3m per notional_10y = dv01_10y / dv01_3m
    hedge_ratio = dv01_10y / dv01_3m  # 31.4x notional

    # Steepener portfolio: Long 3M (pays off when short rate drops), Short 10Y (pays off when long rate rises)
    # Daily P&L ($ per $1M 10Y notional) = -notional_10y * dv01_10y * delta_10y + notional_3m * dv01_3m * (-delta_3m)
    # where negative yield change means positive bond return
    # Daily dollar return:
    pnl_steepener = -(dv01_10y * delta_10y) + (hedge_ratio * dv01_3m * (-delta_3m))

    # Compare correlation with parallel shift factor (level = 0.5 * (r_3m + r_10y))
    parallel_shift = 0.5 * (delta_3m + delta_10y)
    slope_change = delta_10y - delta_3m

    corr_level = float(np.corrcoef(pnl_steepener, parallel_shift)[0, 1])
    corr_slope = float(np.corrcoef(pnl_steepener, slope_change)[0, 1])

    mean_pnl = float(np.mean(pnl_steepener))
    std_pnl = float(np.std(pnl_steepener, ddof=1))
    annualized_sr = (mean_pnl / std_pnl) * np.sqrt(252) if std_pnl > 0 else 0.0

    print(f"Historical Sample Dates: {dates[0]} to {dates[-1]}")
    print(f"Total Observations: {n_days}")
    print(f"Initial 10Y-3M Slope: {slope_bps[0]:.1f} bps")
    print(f"Ending 10Y-3M Slope: {slope_bps[-1]:.1f} bps")
    print(f"DV01 Hedge Ratio (3M per 10Y notional): {hedge_ratio:.2f}")
    print(f"Correlation with Level Shift: {corr_level:.4f}")
    print(f"Correlation with Slope Change: {corr_slope:.4f}")
    print(f"Daily P&L Mean ($): {mean_pnl:.2f}")
    print(f"Daily P&L Std ($): {std_pnl:.2f}")
    print(f"Annualized Sharpe Ratio: {annualized_sr:.3f}")


main()
