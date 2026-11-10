"""Lab GM3-L04-1: Central Bank Policy Divergence and FX Carry Dynamics.

Quantifies foreign exchange carry trade returns, interest rate differentials,
and asymmetric crash risk (negative skewness and maximum drawdown) using
daily foreign exchange (fx_daily.csv) and Treasury yields (ust_daily.csv).
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


def load_csv_column(path: Path, date_col: str, val_col: str) -> dict[str, float]:
    """Load date-indexed numeric series from CSV, skipping empty or ND values."""
    series: dict[str, float] = {}
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = row[date_col]
            v = row[val_col]
            if v and v != "ND":
                series[d] = float(v)
    return series


def main() -> None:
    data_dir = Path("data") if Path("data").exists() else Path("course/assets/data/market")
    fx_path = data_dir / "fx_daily.csv"
    ust_path = data_dir / "ust_daily.csv"

    # Rates are USD per unit of foreign currency:
    # JPY rate is USD/JPY (approx 0.009 = ~110 JPY/USD)
    # AUD rate is USD/AUD (approx 0.70)
    jpy_rates = load_csv_column(fx_path, "date", "JPY")
    aud_rates = load_csv_column(fx_path, "date", "AUD")
    ust_rates = load_csv_column(ust_path, "date", "tbill_3m")

    # Common dates
    common_dates = sorted(set(jpy_rates.keys()) & set(aud_rates.keys()) & set(ust_rates.keys()))
    n = len(common_dates)

    # Compute daily log spot returns for USD/JPY and AUD/USD
    # Invert JPY rate to get standard JPY per USD: S_JPY = 1.0 / jpy_rates[d]
    # S_AUD is USD per AUD
    spot_jpy_per_usd = np.array([1.0 / jpy_rates[d] for d in common_dates], dtype=np.float64)
    us_tbill_3m = np.array([ust_rates[d] for d in common_dates], dtype=np.float64)

    # Daily log returns
    # Long USD / Short JPY spot return: Delta ln(S_JPY) = ln(S_t / S_{t-1})
    log_ret_usd_jpy = np.diff(np.log(spot_jpy_per_usd))

    # US short rate daily carry yield (assuming zero/near-zero JPY policy rate ~0.10%)
    # Carry differential: (i_US - i_JPY) / 252
    carry_diff_daily = (us_tbill_3m[:-1] - 0.10) / 100.0 / 252.0

    # Total USD/JPY carry trade return: spot return + carry yield
    carry_returns = log_ret_usd_jpy + carry_diff_daily

    # Summary statistics
    mean_daily = float(np.mean(carry_returns))
    std_daily = float(np.std(carry_returns, ddof=1))
    ann_return = mean_daily * 252.0
    ann_vol = std_daily * math.sqrt(252.0)
    sharpe = ann_return / ann_vol if ann_vol > 0 else 0.0

    # Skewness: m3 / s^3
    deviations = carry_returns - mean_daily
    m3 = float(np.mean(deviations**3))
    skewness = m3 / (std_daily**3)

    # Maximum Drawdown calculation
    cum_returns = np.cumprod(1.0 + carry_returns)
    running_max = np.maximum.accumulate(cum_returns)
    drawdowns = (cum_returns - running_max) / running_max
    max_drawdown = float(np.min(drawdowns))

    print("Aligned Observation Days:", n)
    print("Annualized Carry Return (%):", round(ann_return * 100.0, 4))
    print("Annualized Volatility (%):", round(ann_vol * 100.0, 4))
    print("Annualized Sharpe Ratio:", round(sharpe, 4))
    print("Return Skewness (Crash Risk):", round(skewness, 4))
    print("Maximum Drawdown (%):", round(max_drawdown * 100.0, 4))


main()
