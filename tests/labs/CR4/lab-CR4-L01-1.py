"""Lab CR4-L01-1: Altman Z-Score Model and Distance to Default Comparison.

Demonstrates calculation of Altman (1968) Z-score for manufacturing firms,
the revised Z' and Z'' models, classification thresholds, and empirical comparison
against structural Merton distance-to-default predictors.
"""

from __future__ import annotations

import math
from typing import NamedTuple


class FirmProfile(NamedTuple):
    name: str
    wc: float
    re: float
    ebit: float
    mve: float
    sales: float
    ta: float
    tl: float
    asset_val: float
    debt_face: float
    asset_vol: float


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def altman_z_score(
    wc: float,
    re: float,
    ebit: float,
    mve: float,
    sales: float,
    ta: float,
    tl: float,
) -> dict[str, float]:
    """Compute Altman (1968) Z-score and discriminant ratios.

    X1 = Working Capital / Total Assets
    X2 = Retained Earnings / Total Assets
    X3 = EBIT / Total Assets
    X4 = Market Value Equity / Total Liabilities
    X5 = Sales / Total Assets
    """
    x1 = wc / ta
    x2 = re / ta
    x3 = ebit / ta
    x4 = mve / tl
    x5 = sales / ta

    z = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 0.999 * x5
    z_prime = 0.717 * x1 + 0.847 * x2 + 3.107 * x3 + 0.420 * x4 + 0.998 * x5
    z_double_prime = 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4

    return {
        "x1": x1,
        "x2": x2,
        "x3": x3,
        "x4": x4,
        "x5": x5,
        "z": z,
        "z_prime": z_prime,
        "z_double_prime": z_double_prime,
    }


def merton_distance_to_default(
    v: float,
    d: float,
    mu: float,
    sigma: float,
    t: float,
) -> float:
    """Compute Merton distance to default (DD)."""
    return (math.log(v / d) + (mu - 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))


def classify_z(z: float) -> str:
    """Classify firm into Altman distress zones."""
    if z < 1.81:
        return "Distress"
    elif z <= 2.99:
        return "Grey"
    else:
        return "Safe"


def main() -> None:
    firms = [
        FirmProfile(
            name="Healthy Manufacturing Corp",
            wc=120.0,
            re=250.0,
            ebit=95.0,
            mve=600.0,
            sales=800.0,
            ta=500.0,
            tl=200.0,
            asset_val=800.0,
            debt_face=200.0,
            asset_vol=0.20,
        ),
        FirmProfile(
            name="Borderline Capital Inc",
            wc=30.0,
            re=50.0,
            ebit=35.0,
            mve=180.0,
            sales=400.0,
            ta=400.0,
            tl=250.0,
            asset_val=430.0,
            debt_face=250.0,
            asset_vol=0.30,
        ),
        FirmProfile(
            name="Distressed Industrial Ltd",
            wc=-40.0,
            re=-80.0,
            ebit=-15.0,
            mve=45.0,
            sales=300.0,
            ta=350.0,
            tl=320.0,
            asset_val=365.0,
            debt_face=320.0,
            asset_vol=0.45,
        ),
    ]

    print("Altman (1968) Z-Score & Merton Distance-to-Default Analysis:")
    print("Firm Name                    |   Z   | Zone      |   Z'  |  Z''  | Merton DD | Merton PD")
    print("-" * 88)

    for f in firms:
        res = altman_z_score(f.wc, f.re, f.ebit, f.mve, f.sales, f.ta, f.tl)
        zone = classify_z(res["z"])
        dd = merton_distance_to_default(f.asset_val, f.debt_face, 0.05, f.asset_vol, 1.0)
        pd = norm_cdf(-dd)

        z_str = f"{res['z']:5.2f}"
        zp_str = f"{res['z_prime']:5.2f}"
        zpp_str = f"{res['z_double_prime']:5.2f}"
        print(f"{f.name:28} | {z_str} | {zone:9} | {zp_str} | {zpp_str} |   {dd:5.2f}   |   {pd:6.4f}")

    # Invariant verification:
    # Distress firm must have Z < 1.81 and DD substantially lower than Healthy firm
    h_f = firms[0]
    d_f = firms[2]
    healthy_res = altman_z_score(h_f.wc, h_f.re, h_f.ebit, h_f.mve, h_f.sales, h_f.ta, h_f.tl)
    distressed_res = altman_z_score(d_f.wc, d_f.re, d_f.ebit, d_f.mve, d_f.sales, d_f.ta, d_f.tl)

    assert healthy_res["z"] > 2.99
    assert distressed_res["z"] < 1.81
    print("\nVerified discriminant thresholds: Healthy Z > 2.99 and Distressed Z < 1.81.")


main()
