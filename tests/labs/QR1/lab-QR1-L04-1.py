"""QR1 Lesson 4 Inline Lab 1: Corporate action adjustment factors and split invariance.

Demonstrates backward-adjustment of price series for pure stock splits,
computes cumulative adjustment factors, and verifies Derivation 4.1
(split return invariance within 1e-12 relative tolerance).
Data: SIMULATED daily close prices and stock split events.
"""

from __future__ import annotations

from typing import NamedTuple


class SplitEvent(NamedTuple):
    ex_date: str  # YYYY-MM-DD
    ratio: float  # e.g., 2.0 for 2-for-1


class DailyPrice(NamedTuple):
    date: str
    raw_close: float


def compute_cumulative_factors(
    dates: list[str],
    splits: list[SplitEvent],
) -> list[float]:
    """Compute backward cumulative adjustment factor F_d = prod_{k: ex_date_k > d} ratio_k."""
    factors: list[float] = []
    for d in dates:
        factor = 1.0
        for s in splits:
            if s.ex_date > d:
                factor *= s.ratio
        factors.append(factor)
    return factors


def adjust_prices(raw_closes: list[float], factors: list[float]) -> list[float]:
    """Calculate backward-adjusted prices: adjusted_close = raw_close / factor."""
    return [p / f for p, f in zip(raw_closes, factors, strict=True)]


def main() -> None:
    # SIMULATED 10-day price series containing two pure split events
    # Event 1 on 2026-03-04: 2-for-1 split (ratio 2.0). 120 -> 60
    # Event 2 on 2026-03-08: 3-for-1 split (ratio 3.0). 75 -> 25
    splits = [
        SplitEvent("2026-03-04", 2.0),
        SplitEvent("2026-03-08", 3.0),
    ]

    dates = [
        "2026-03-01",
        "2026-03-02",
        "2026-03-03",
        "2026-03-04",  # Split 1 ex-date
        "2026-03-05",
        "2026-03-06",
        "2026-03-07",
        "2026-03-08",  # Split 2 ex-date
        "2026-03-09",
        "2026-03-10",
    ]

    raw_closes = [
        118.00,
        119.50,
        120.00,
        60.00,  # Pure 2-for-1 split (no change in economic value)
        65.00,
        70.00,
        75.00,
        25.00,  # Pure 3-for-1 split
        26.50,
        28.00,
    ]

    factors = compute_cumulative_factors(dates, splits)
    adj_closes = adjust_prices(raw_closes, factors)

    print("Historical Price and Corporate Action Adjustment Table:")
    print("  Date        Raw Close  Factor  Adj Close  Raw Ret     Adj Ret")

    split_ex_dates = {s.ex_date for s in splits}
    split_adj_returns: list[float] = []

    for i in range(len(dates)):
        d = dates[i]
        p_raw = raw_closes[i]
        f = factors[i]
        p_adj = adj_closes[i]

        if i == 0:
            raw_ret_str = "    ---  "
            adj_ret_str = "    ---  "
        else:
            raw_ret = (raw_closes[i] / raw_closes[i - 1]) - 1.0
            adj_ret = (adj_closes[i] / adj_closes[i - 1]) - 1.0
            raw_ret_str = f"{raw_ret:+9.2%}"
            adj_ret_str = f"{adj_ret:+9.2%}"

            if d in split_ex_dates:
                split_adj_returns.append(adj_ret)

        print(f"  {d}  {p_raw:9.2f}  {f:6.1f}  {p_adj:9.2f}  {raw_ret_str}  {adj_ret_str}")

    print("\nDerivation 4.1 Split Return Invariance Verification:")
    tolerance = 1e-12
    max_err = max(abs(r) for r in split_adj_returns)
    print(f"  Split dates evaluated: {len(split_adj_returns)}")
    print(f"  Maximum absolute adjusted return at split dates: {max_err:.2e}")
    print(f"  Invariance holds within tolerance {tolerance:.0e}: {max_err <= tolerance}")


main()
