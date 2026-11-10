"""Lab CR3-L02-1: Synthetic Treasury Matching and Gilchrist-Zakrajšek Credit Spread.

SIMULATED: constructs synthetic risk-free benchmark bond matching corporate cash flows
under a Svensson zero-coupon Treasury curve, demonstrating elimination of maturity
and coupon bias present in naive maturity-matched corporate credit spreads.
"""

from __future__ import annotations

import math
from typing import NamedTuple


class BondItem(NamedTuple):
    id: str
    face: float
    coupon: float
    mat: float
    mkt_price: float


def svensson_zero_yield(t: float, beta: list[float], tau: list[float]) -> float:
    """Evaluate Svensson (1994) zero-coupon Treasury yield at maturity t in years.

    beta: [beta0, beta1, beta2, beta3]
    tau: [tau1, tau2]
    """
    if t <= 1e-6:
        return beta[0] + beta[1]

    t_tau1 = t / tau[0]
    t_tau2 = t / tau[1]
    e1 = math.exp(-t_tau1)
    e2 = math.exp(-t_tau2)

    term1 = beta[0]
    term2 = beta[1] * ((1.0 - e1) / t_tau1)
    term3 = beta[2] * ((1.0 - e1) / t_tau1 - e1)
    term4 = beta[3] * ((1.0 - e2) / t_tau2 - e2)

    return term1 + term2 + term3 + term4


def bond_price_from_yield(face: float, coupon_rate: float, maturity: float, ytm: float, freq: int = 2) -> float:
    """Calculate dirty price of fixed-coupon bond given continuous/semi-annual yield."""
    n_periods = round(maturity * freq)
    coupon = (face * coupon_rate) / freq
    price = 0.0
    for i in range(1, n_periods + 1):
        t = i / freq
        df = 1.0 / ((1.0 + ytm / freq) ** (freq * t))
        cf = coupon + (face if i == n_periods else 0.0)
        price += cf * df
    return price


def bond_yield_to_maturity(face: float, coupon_rate: float, maturity: float, price: float, freq: int = 2) -> float:
    """Solve for internal rate of return / yield to maturity using Newton-Raphson."""
    y = coupon_rate
    for _ in range(30):
        p = bond_price_from_yield(face, coupon_rate, maturity, y, freq)
        dp = 0.0
        n_periods = round(maturity * freq)
        coupon = (face * coupon_rate) / freq
        for i in range(1, n_periods + 1):
            t = i / freq
            df = 1.0 / ((1.0 + y / freq) ** (freq * t + 1))
            cf = coupon + (face if i == n_periods else 0.0)
            dp -= t * cf * df
        diff = p - price
        if abs(diff) < 1e-9:
            break
        y -= diff / dp
    return y


def price_synthetic_treasury(
    face: float,
    coupon_rate: float,
    maturity: float,
    beta: list[float],
    tau: list[float],
    freq: int = 2,
) -> float:
    """Price synthetic Treasury security by discounting each cash flow at exact zero yield."""
    n_periods = round(maturity * freq)
    coupon = (face * coupon_rate) / freq
    price = 0.0
    for i in range(1, n_periods + 1):
        t = i / freq
        z_rate = svensson_zero_yield(t, beta, tau)
        # Continuous or semi-annual discounting
        df = math.exp(-z_rate * t)
        cf = coupon + (face if i == n_periods else 0.0)
        price += cf * df
    return price


def main() -> None:
    # Calibrated US Treasury parameters: upward-sloping curve
    beta_ust = [0.045, -0.020, 0.015, -0.010]
    tau_ust = [1.5, 6.0]

    # Sample of three corporate bonds with different coupons and maturities
    bonds = [
        BondItem("Bond A (High Coupon)", 100.0, 0.075, 5.0, 108.50),
        BondItem("Bond B (Low Coupon)", 100.0, 0.030, 5.0, 94.20),
        BondItem("Bond C (Long Mat)", 100.0, 0.055, 10.0, 98.70),
    ]

    print("Gilchrist-Zakrajsek (2012) Micro Credit Spread Construction:")
    print("  Bond ID              | Corp YTM (%) | Synth T-YTM (%) | GZ Spread (bp) | Naive TS Spread (bp)")
    print("-----------------------+--------------+-----------------+----------------+---------------------")

    for b in bonds:
        corp_ytm = bond_yield_to_maturity(b.face, b.coupon, b.mat, b.mkt_price)
        synth_price = price_synthetic_treasury(b.face, b.coupon, b.mat, beta_ust, tau_ust)
        synth_ytm = bond_yield_to_maturity(b.face, b.coupon, b.mat, synth_price)

        # GZ micro credit spread
        gz_spread_bp = (corp_ytm - synth_ytm) * 10000.0

        # Naive benchmark: single maturity zero rate
        naive_zero = svensson_zero_yield(b.mat, beta_ust, tau_ust)
        naive_spread_bp = (corp_ytm - naive_zero) * 10000.0

        c_pct = corp_ytm * 100
        s_pct = synth_ytm * 100
        print(
            f"  {b.id:20s} |    {c_pct:5.2f}%   |     {s_pct:5.2f}%     |    "
            f"{gz_spread_bp:5.1f}       |       {naive_spread_bp:5.1f}"
        )

        assert gz_spread_bp > 0.0


main()
