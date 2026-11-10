"""Lab S4-L01-1: Autocorrelation of raw versus squared daily returns.

Examines empirical autocorrelation functions of daily EUR/USD exchange rate log returns
and squared log returns from Board of Governors H.10 release (fx_daily.csv).
Demonstrates volatility clustering: raw returns show negligible linear autocorrelation,
while squared returns exhibit persistent positive autocorrelation.
Data source: Board of Governors of the Federal Reserve System, G.5/H.10 Foreign Exchange Rates.
Retrieved from MANIFEST: 2026-10-19.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


def sample_acf(series: list[float], max_lag: int = 5) -> list[float]:
    """Compute sample autocorrelations for lags 1 through max_lag."""
    n = len(series)
    mean_val = sum(series) / n
    var_val = sum((x - mean_val) ** 2 for x in series) / n
    if var_val <= 0.0:
        return [0.0] * max_lag
    acf_vals: list[float] = []
    for h in range(1, max_lag + 1):
        cov = sum((series[t] - mean_val) * (series[t + h] - mean_val) for t in range(n - h)) / n
        acf_vals.append(cov / var_val)
    return acf_vals


def main() -> None:
    data_path = Path("data") / "fx_daily.csv"
    with data_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        prices: list[float] = [float(row["EUR"]) for row in reader if row.get("EUR")]

    # Daily log returns: r_t = ln(P_t / P_{t-1})
    returns = [math.log(prices[t] / prices[t - 1]) for t in range(1, len(prices))]
    squared_returns = [r * r for r in returns]
    n = len(returns)

    max_lag = 5
    acf_raw = sample_acf(returns, max_lag)
    acf_sq = sample_acf(squared_returns, max_lag)

    # 95% Bartlett confidence bound under white noise null: 1.96 / sqrt(N)
    bound_95 = 1.96 / math.sqrt(n)

    print(f"Sample size: {n} daily EUR/USD returns")
    print(f"95% white noise bound: +/-{bound_95:.4f}")
    print("Lag | Raw Return ACF | Squared Return ACF | Significant Clustering?")
    print("-" * 65)
    for h in range(1, max_lag + 1):
        raw_val = acf_raw[h - 1]
        sq_val = acf_sq[h - 1]
        sig = "Yes (p < 0.05)" if sq_val > bound_95 else "No"
        print(f"  {h} |        {raw_val:+.4f}  |            {sq_val:+.4f}  | {sig}")


main()
