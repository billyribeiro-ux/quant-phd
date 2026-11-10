"""Lab X2-L06-1: Multi-Factor Currency Allocation: Carry, Momentum, and Value.

Simulates cross-sectional currency factors (Carry, Momentum, Value), evaluates
their correlation structure (Asness et al. 2013), and measures multi-factor diversification.
"""

from __future__ import annotations

import math
import random
from typing import Any


def simulate_currency_styles(
    n_months: int = 120,
    seed: int = 888,
) -> dict[str, Any]:
    """Simulate Carry, Momentum, and Value factors and multi-factor portfolio.

    Args:
        n_months: Number of simulated months.
        seed: Random seed.

    Returns:
        Dictionary of factor correlations, annualized statistics, and multi-factor gains.
    """
    rng = random.Random(seed)

    carry_rets: list[float] = []
    mom_rets: list[float] = []
    val_rets: list[float] = []

    for _ in range(n_months):
        z_liq = rng.gauss(0.0, 1.0)
        z_trend = rng.gauss(0.0, 1.0)
        z_ppp = rng.gauss(0.0, 1.0)

        # Carry factor
        r_carry = 0.0050 + 0.014 * z_liq + rng.gauss(0.0, 0.014)

        # Momentum factor
        r_mom = 0.0045 + 0.014 * z_trend + 0.004 * z_liq + rng.gauss(0.0, 0.014)

        # Value factor
        r_val = 0.0045 + 0.014 * z_ppp - 0.010 * z_trend + rng.gauss(0.0, 0.014)

        carry_rets.append(r_carry)
        mom_rets.append(r_mom)
        val_rets.append(r_val)

    # Compute correlation matrix
    def corr(x: list[float], y: list[float]) -> float:
        mx = sum(x) / len(x)
        my = sum(y) / len(y)
        cov = sum((a - mx) * (b - my) for a, b in zip(x, y, strict=True))
        vx = sum((a - mx) ** 2 for a in x)
        vy = sum((b - my) ** 2 for b in y)
        return cov / math.sqrt(vx * vy)

    r_cm = corr(carry_rets, mom_rets)
    r_cv = corr(carry_rets, val_rets)
    r_mv = corr(mom_rets, val_rets)

    # Annualized stats for single factors
    def factor_stats(series: list[float]) -> tuple[float, float, float]:
        m = sum(series) / len(series)
        v = sum((r - m) ** 2 for r in series) / (len(series) - 1)
        s = math.sqrt(v)
        ann_m = m * 12.0
        ann_s = s * math.sqrt(12.0)
        sr = ann_m / ann_s if ann_s > 1e-8 else 0.0
        return ann_m, ann_s, sr

    _m_c, _s_c, sr_c = factor_stats(carry_rets)
    _m_m, _s_m, sr_m = factor_stats(mom_rets)
    _m_v, _s_v, sr_v = factor_stats(val_rets)

    # Multi-factor equal-weighted blend
    multi_rets = [(carry_rets[t] + mom_rets[t] + val_rets[t]) / 3.0 for t in range(n_months)]
    _m_multi, _s_multi, sr_multi = factor_stats(multi_rets)
    best_single_sr = max(sr_c, sr_m, sr_v)
    sr_gain = ((sr_multi / best_single_sr) - 1.0) * 100.0

    return {
        "n_months": n_months,
        "corr_carry_mom": round(r_cm, 3),
        "corr_carry_val": round(r_cv, 3),
        "corr_mom_val": round(r_mv, 3),
        "sr_carry": round(sr_c, 3),
        "sr_mom": round(sr_m, 3),
        "sr_val": round(sr_v, 3),
        "sr_multi": round(sr_multi, 3),
        "sr_gain_pct": round(sr_gain, 1),
    }


def main() -> None:
    res = simulate_currency_styles(n_months=120, seed=888)
    print("=== Multi-Factor Currency Styles: Carry, Momentum, Value ===")
    print(f"Sample length: {res['n_months']} months")
    print("Pairwise Correlations:")
    print(f"  Corr(Carry, Momentum): {res['corr_carry_mom']:>6.3f}")
    print(f"  Corr(Carry, Value):    {res['corr_carry_val']:>6.3f}")
    print(f"  Corr(Momentum, Value): {res['corr_mom_val']:>6.3f} (strong negative diversification)")
    print("Sharpe Ratios (Annualized):")
    print(f"  Carry alone:    {res['sr_carry']:.3f}")
    print(f"  Momentum alone: {res['sr_mom']:.3f}")
    print(f"  Value alone:    {res['sr_val']:.3f}")
    print(f"  Multi-Factor:   {res['sr_multi']:.3f} (+{res['sr_gain_pct']:.1f}% Sharpe ratio expansion)")


main()
