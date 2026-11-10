"""CF3 project lab 3 (rung 3 check): Reference numbers for independent memo evaluation.

SIMULATED: 10 corporate issuers generated deterministically from seed 42.
Standard library only; deterministic execution.
Computes and prints the exact baseline table and regression results
that the student's project memo must reproduce and evaluate.
"""

from __future__ import annotations

import math
from statistics import NormalDist
from typing import TypedDict


class FirmData(TypedDict):
    id: str
    name: str
    e_idx: int
    g_idx: int
    assets: int
    debt: int
    mkt_eq: int
    book_eq: int


def main() -> None:
    print("CF3 Project Rung 3: Sanity Check and Memo Benchmark (Seed 42)")
    print("=============================================================")

    # Reference dataset from seed 42
    firms: list[FirmData] = [
        {
            "id": "F01",
            "name": "Apex Dynamics",
            "e_idx": 4,
            "g_idx": 8,
            "assets": 339_708_93_49,
            "debt": 87_609_92_30,
            "mkt_eq": 643_089_03_62,
            "book_eq": 252_099_01_19,
        },
        {
            "id": "F02",
            "name": "Beacon Capital",
            "e_idx": 2,
            "g_idx": 5,
            "assets": 82_486_28_50,
            "debt": 28_498_18_55,
            "mkt_eq": 182_974_56_44,
            "book_eq": 53_988_09_95,
        },
        {
            "id": "F03",
            "name": "Crestline Energy",
            "e_idx": 3,
            "g_idx": 4,
            "assets": 172_978_31_17,
            "debt": 80_564_18_85,
            "mkt_eq": 269_432_22_38,
            "book_eq": 92_414_12_32,
        },
        {
            "id": "F04",
            "name": "Delta Semiconductor",
            "e_idx": 1,
            "g_idx": 3,
            "assets": 444_208_34_67,
            "debt": 115_795_17_54,
            "mkt_eq": 1056_821_21_21,
            "book_eq": 328_413_17_13,
        },
        {
            "id": "F05",
            "name": "Echo Logistics",
            "e_idx": 5,
            "g_idx": 7,
            "assets": 218_507_20_00,
            "debt": 91_349_92_00,
            "mkt_eq": 286_878_14_40,
            "book_eq": 127_157_28_00,
        },
        {
            "id": "F06",
            "name": "Falcon Healthcare",
            "e_idx": 3,
            "g_idx": 6,
            "assets": 194_338_10_25,
            "debt": 54_899_50_00,
            "mkt_eq": 398_492_10_50,
            "book_eq": 139_438_60_25,
        },
        {
            "id": "F07",
            "name": "Global Maritime",
            "e_idx": 4,
            "g_idx": 7,
            "assets": 126_749_18_80,
            "debt": 60_298_20_00,
            "mkt_eq": 169_843_91_19,
            "book_eq": 66_450_98_80,
        },
        {
            "id": "F08",
            "name": "Horizon Tech",
            "e_idx": 2,
            "g_idx": 3,
            "assets": 371_880_24_90,
            "debt": 85_940_12_00,
            "mkt_eq": 892_512_59_76,
            "book_eq": 285_940_12_90,
        },
        {
            "id": "F09",
            "name": "Ironclad Materials",
            "e_idx": 5,
            "g_idx": 9,
            "assets": 265_441_90_10,
            "debt": 119_448_85_54,
            "mkt_eq": 371_618_66_14,
            "book_eq": 145_993_04_56,
        },
        {
            "id": "F10",
            "name": "Jupiter Media",
            "e_idx": 3,
            "g_idx": 5,
            "assets": 158_920_11_20,
            "debt": 41_319_22_91,
            "mkt_eq": 317_840_22_40,
            "book_eq": 117_600_88_29,
        },
    ]

    print(f"{'Firm':<22} | {'E-Index':>7} | {'G-Index':>7} | {'Assets ($M)':>12} | {'Debt ($M)':>10} | {'Tobin Q':>8}")
    print("-" * 78)

    e_scores: list[float] = []
    g_scores: list[float] = []
    q_vals: list[float] = []

    for f in firms:
        q = (f["assets"] - f["book_eq"] + f["mkt_eq"]) / f["assets"]
        e_scores.append(float(f["e_idx"]))
        g_scores.append(float(f["g_idx"]))
        q_vals.append(q)

        print(
            f"{f['name']:<22} | {f['e_idx']:7d} | {f['g_idx']:7d} | "
            f"${f['assets'] / 100_000_00:10.2f}M | ${f['debt'] / 100_000_00:8.2f}M | {q:8.4f}"
        )

    # OLS Regression of Tobin's Q on E-Index
    n = len(e_scores)
    mean_e = sum(e_scores) / n
    mean_q = sum(q_vals) / n
    s_ee = sum((ei - mean_e) ** 2 for ei in e_scores)
    s_eq = sum((ei - mean_e) * (qi - mean_q) for ei, qi in zip(e_scores, q_vals, strict=True))
    s_qq = sum((qi - mean_q) ** 2 for qi in q_vals)

    beta = s_eq / s_ee
    alpha = mean_q - beta * mean_e
    rss = sum((qi - (alpha + beta * ei)) ** 2 for ei, qi in zip(e_scores, q_vals, strict=True))
    s2 = rss / (n - 2)
    se_beta = math.sqrt(s2 / s_ee)
    t_stat = beta / se_beta
    r2 = 1.0 - (rss / s_qq)

    # Power
    dist = NormalDist()
    z_crit = dist.inv_cdf(1.0 - 0.05 / 2.0)
    delta = abs(beta) / se_beta
    power = (1.0 - dist.cdf(z_crit - delta)) + dist.cdf(-z_crit - delta)

    print("\nBenchmark OLS Results (N = 10, Seed 42):")
    print(f"  Intercept (alpha):    {alpha:.4f}")
    print(f"  Slope (beta):         {beta:.4f}")
    print(f"  Std Error (se_beta):  {se_beta:.4f}")
    print(f"  t-statistic:          {t_stat:.4f}")
    print(f"  R-squared:            {r2:.4%}")
    print(f"  Residual Stdev (s):   {math.sqrt(s2):.4f}")
    print(f"  Analytical Power:     {power:.2%}")


main()
