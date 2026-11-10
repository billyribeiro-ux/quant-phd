"""Lab CF4-L02-1: DCF Valuation and Discounting Conventions.

Evaluates explicit present values under year-end versus mid-year cash flow arrival
assumptions and quantifies the exact mid-year valuation adjustment factor.
"""

from __future__ import annotations

import numpy as np


def dcf_discount_comparison(
    fcff: np.ndarray,
    wacc: float,
) -> dict[str, float | np.ndarray]:
    """Compare year-end vs mid-year discounting conventions."""
    h = len(fcff)
    periods = np.arange(1, h + 1, dtype=np.float64)

    # Year-end discount factors: (1 + WACC)^(-t)
    df_yearend = 1.0 / np.power(1.0 + wacc, periods)
    pv_yearend = np.sum(fcff * df_yearend)

    # Mid-year discount factors: (1 + WACC)^(-(t - 0.5))
    df_midyear = 1.0 / np.power(1.0 + wacc, periods - 0.5)
    pv_midyear = np.sum(fcff * df_midyear)

    # Exact adjustment factor: sqrt(1 + WACC)
    exact_factor = np.sqrt(1.0 + wacc)
    empirical_ratio = pv_midyear / pv_yearend

    return {
        "pv_yearend": float(pv_yearend),
        "pv_midyear": float(pv_midyear),
        "dollar_difference": float(pv_midyear - pv_yearend),
        "empirical_ratio": float(empirical_ratio),
        "exact_factor": float(exact_factor),
    }


def main() -> None:
    print("CF4 Lab L02-1: DCF Discounting Conventions")
    print("==========================================")

    fcff = np.array([110.0, 121.5, 135.75, 150.5, 168.0])

    print("WACC     Year-End PV   Mid-Year PV   Difference   Ratio    Exact Sqrt(1+WACC)")
    print("-----------------------------------------------------------------------------")
    for wacc in [0.07, 0.08, 0.09, 0.10, 0.12]:
        res = dcf_discount_comparison(fcff, wacc)
        print(
            f"{wacc * 100:4.1f}%    ${res['pv_yearend']:8.2f}M   "
            f"${res['pv_midyear']:8.2f}M   "
            f"${res['dollar_difference']:7.2f}M   "
            f"{res['empirical_ratio']:.6f}  "
            f"{res['exact_factor']:.6f}"
        )
        assert abs(res["empirical_ratio"] - res["exact_factor"]) < 1e-9

    print("-----------------------------------------------------------------------------")
    print("Mid-year scalar equality pv_midyear == pv_yearend * sqrt(1 + WACC): True")


main()
