"""Lab Project 1 (Worked Example): End-to-end replication audit and divergence decomposition."""

from __future__ import annotations

import numpy as np


def main() -> None:
    # 5 stocks, 1 month
    permnos = np.array([10001, 10002, 10003, 10004, 10005])
    shrcd = np.array([11, 10, 31, 11, 12])  # 31 is REIT, 12 is foreign ADR
    exchcd = np.array([1, 2, 1, 3, 1])
    raw_ret = np.array([0.05, -0.02, 0.15, 0.08, -0.10])
    dlret = np.array([np.nan, np.nan, np.nan, -0.40, np.nan])
    dlstcd = np.array([0, 0, 0, 580, 0])  # Stock 4 delisted for performance
    me = np.array([500.0, 1500.0, 200.0, 300.0, 800.0])

    # 1. Share code filtering (SHRCD 10/11 only)
    valid_mask = np.isin(shrcd, [10, 11]) & np.isin(exchcd, [1, 2, 3])
    print(f"Step 1: Universe Filter: Retained {np.sum(valid_mask)} of {len(permnos)} stocks (excluded REIT and ADR).")

    # 2. Shumway Delisting Adjustment on filtered stocks
    adj_ret = np.copy(raw_ret)
    for i in range(len(permnos)):
        if dlstcd[i] > 0:
            d_ret = dlret[i]
            if np.isnan(d_ret):
                d_ret = -0.55 if exchcd[i] == 3 else -0.30
            adj_ret[i] = (1.0 + raw_ret[i]) * (1.0 + d_ret) - 1.0

    s4_raw = raw_ret[3]
    s4_adj = adj_ret[3]
    s4_dl = dlret[3]
    print(f"Step 2: Delist Adj on Stock 4: Raw {s4_raw:+.2f} -> Compounded {s4_adj:+.4f} (DLRET = {s4_dl:.2f})")

    # 3. Portfolio Weighting: Equal-weighted vs Value-weighted on valid stocks
    valid_ret = adj_ret[valid_mask]
    valid_me = me[valid_mask]

    ew_ret = float(np.mean(valid_ret))
    weights = valid_me / np.sum(valid_me)
    vw_ret = float(np.sum(weights * valid_ret))

    print(f"Step 3: Equal-Weighted Return: {ew_ret * 100:.3f}%")
    print(f"        Value-Weighted Return: {vw_ret * 100:.3f}%")
    print(f"        Weighting Wedge: {(vw_ret - ew_ret) * 100:+.3f}%")

    # 4. Articulation breakdown
    published_target = 0.040  # 4.0%
    divergence = vw_ret - published_target
    print(f"Step 4: Divergence from target ({published_target * 100:.1f}%): {divergence * 100:+.3f}%")


main()
