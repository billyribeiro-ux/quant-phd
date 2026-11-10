"""Lab CR3-L04-1: Credit Sentiment and Two-Stage Predictable Reversals.

SIMULATED: evaluates López-Salido, Stein & Zakrajšek (2017) hypothesis that elevated
credit-market sentiment (high HY issuance share, compressed spreads) predictably
forecasts credit spread widening and subsequent macroeconomic contractions.
"""

from __future__ import annotations

from typing import NamedTuple


class SentimentPeriod(NamedTuple):
    t: str
    hy_share: float
    spread: float
    fwd_spread_widening: float
    fwd_gdp: float


def main() -> None:
    # Stylized semi-annual credit cycle observations (10 periods, 5 years)
    periods = [
        SentimentPeriod("T1", 0.38, 120.0, 160.0, -1.5),
        SentimentPeriod("T2", 0.42, 105.0, 195.0, -2.8),
        SentimentPeriod("T3", 0.35, 135.0, 140.0, -0.8),
        SentimentPeriod("T4", 0.24, 210.0, 20.0, 1.4),
        SentimentPeriod("T5", 0.12, 340.0, -130.0, 4.5),
        SentimentPeriod("T6", 0.10, 360.0, -150.0, 4.8),
        SentimentPeriod("T7", 0.18, 260.0, -60.0, 3.6),
        SentimentPeriod("T8", 0.28, 175.0, 50.0, 2.2),
        SentimentPeriod("T9", 0.34, 130.0, 135.0, 0.2),
        SentimentPeriod("T10", 0.40, 110.0, 180.0, -2.0),
    ]

    hy_vals = [p.hy_share for p in periods]
    spr_widening = [p.fwd_spread_widening for p in periods]
    fwd_gdp = [p.fwd_gdp for p in periods]

    def ols(x: list[float], y: list[float]) -> tuple[float, float, float]:
        mx = sum(x) / len(x)
        my = sum(y) / len(y)
        s_xx = sum((xi - mx) ** 2 for xi in x)
        s_xy = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y, strict=False))
        s_yy = sum((yi - my) ** 2 for yi in y)
        b = s_xy / s_xx if s_xx > 0 else 0.0
        a = my - b * mx
        r2 = (s_xy**2) / (s_xx * s_yy) if (s_xx * s_yy) > 0 else 0.0
        return a, b, r2

    # Stage 1: Predictable spread widening from high-yield issuance share
    _a1, b_stage1, r2_stage1 = ols(hy_vals, spr_widening)

    # Stage 2: Real GDP contraction from sentiment
    _a2, b_stage2, r2_stage2 = ols(hy_vals, fwd_gdp)

    print("Two-Stage Credit Sentiment Predictive Dynamics (López-Salido et al. 2017):")
    print("  Period | HY Issuance Share | Spread (bp) | Fwd Spread Change (bp) | Fwd GDP Growth (%)")
    print("---------+-------------------+-------------+------------------------+-------------------")
    for p in periods:
        hy_pct = p.hy_share * 100
        spr = p.spread
        spr_chg = p.fwd_spread_widening
        gdp = p.fwd_gdp
        print(
            f"   {p.t:4s}  |       {hy_pct:4.1f}%       |    {spr:5.1f}    |         "
            f"{spr_chg:+5.1f}          |       {gdp:+4.1f}%"
        )

    print("\nTwo-Stage Regression Results:")
    print(
        f"  Stage 1 (Spread Reversal):    beta = {b_stage1:+6.1f} bp per 100% HY share, R^2 = {r2_stage1 * 100:4.1f}%"
    )
    print(
        f"  Stage 2 (Output Contraction): beta = {b_stage2:+6.2f} % GDP per 100% HY share, "
        f"R^2 = {r2_stage2 * 100:4.1f}%"
    )

    # High sentiment positively predicts future spread widening and negatively predicts future GDP growth
    assert b_stage1 > 0.0
    assert b_stage2 < 0.0
    assert r2_stage1 > 0.60


main()
