"""Lab CR2-L02-1: Bootstrapping hazard rate curves from market CDS quotes.

Implements sequential root-finding for piecewise constant default intensities
and evaluates recovery rate sensitivity across market standard conventions.
"""

from __future__ import annotations

import math

from scipy import optimize


def get_survival_prob(t: float, tenors: list[float], rates: list[float]) -> float:
    """Evaluate survival probability under piecewise constant hazard rates."""
    if t <= 0.0:
        return 1.0
    accum = 0.0
    prev_t = 0.0
    for j, tj in enumerate(tenors):
        if t <= prev_t:
            break
        duration = min(t, tj) - prev_t
        accum += rates[j] * duration
        prev_t = tj
        if t <= tj:
            break
    return math.exp(-accum)


def bootstrap_curve(
    tenors: list[float],
    spreads_bps: list[float],
    recovery: float,
    r: float = 0.03,
    coupon_freq: int = 4,
) -> tuple[list[float], list[float]]:
    """Bootstrap piecewise constant hazard rates from par spreads."""
    dt = 1.0 / coupon_freq
    hazard_rates: list[float] = []
    survival_probs: list[float] = []

    for i, tenor_val in enumerate(tenors):
        s_target = spreads_bps[i] / 10000.0
        known = list(hazard_rates)
        sub_tenors = tenors[: i + 1]
        num_periods = round(tenor_val * coupon_freq)
        times = [(k + 1) * dt for k in range(num_periods)]

        def error_fn(
            lam: float,
            k_rates: list[float] = known,
            t_steps: list[float] = times,
            a_tenors: list[float] = sub_tenors,
            s_tgt: float = s_target,
        ) -> float:
            c_rates = [*k_rates, lam]
            prem = 0.0
            prot = 0.0
            for k, tk in enumerate(t_steps):
                t_prev = t_steps[k - 1] if k > 0 else 0.0
                df_k = math.exp(-r * tk)
                df_mid = math.exp(-r * 0.5 * (t_prev + tk))
                q_prev = get_survival_prob(t_prev, a_tenors, c_rates)
                q_k = get_survival_prob(tk, a_tenors, c_rates)
                prem += dt * df_k * q_k + 0.5 * dt * df_mid * (q_prev - q_k)
                prot += (1.0 - recovery) * df_mid * (q_prev - q_k)
            return prot - s_tgt * prem

        sol = float(optimize.brentq(error_fn, 1e-6, 3.0))
        hazard_rates.append(sol)
        survival_probs.append(get_survival_prob(tenor_val, sub_tenors, hazard_rates))

    return hazard_rates, survival_probs


def main() -> None:
    tenors = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
    market_quotes = [45.0, 60.0, 75.0, 95.0, 115.0, 130.0]  # basis points
    r = 0.03

    rates_40, surv_40 = bootstrap_curve(tenors, market_quotes, recovery=0.40, r=r)
    rates_20, _surv_20 = bootstrap_curve(tenors, market_quotes, recovery=0.20, r=r)
    rates_60, _surv_60 = bootstrap_curve(tenors, market_quotes, recovery=0.60, r=r)

    print("CDS Hazard Rate Bootstrapping (Base Recovery R = 40%, r = 3%):")
    print("  Tenor (yr) | Par Quote (bp) | Hazard Rate lambda (bp) | Survival Q(T) | 5Y Fwd Intensity")
    print("-------------+----------------+-------------------------+---------------+------------------")

    for i, t in enumerate(tenors):
        print(
            f"    {t:4.1f}     |     {market_quotes[i]:6.1f}     |         {rates_40[i] * 10000:6.1f}          |"
            f"    {surv_40[i]:6.4f}   |      {rates_40[i] * 10000:6.1f} bp"
        )

    print("\nRecovery Rate Sensitivity Analysis (lambda ~ s / (1 - R)):")
    print("  Tenor (yr) | lambda (R=20%) | lambda (R=40%) | lambda (R=60%) | Ratio (R=60% / R=20%)")
    print("-------------+----------------+----------------+----------------+----------------------")
    for i, t in enumerate(tenors):
        r20 = rates_20[i] * 10000
        r40 = rates_40[i] * 10000
        r60 = rates_60[i] * 10000
        ratio = r60 / r20
        print(f"    {t:4.1f}     |    {r20:6.1f} bp   |    {r40:6.1f} bp   |    {r60:6.1f} bp   |        {ratio:4.2f}x")

    # Invariants
    assert all(r > 0 for r in rates_40)
    for i in range(len(surv_40) - 1):
        assert surv_40[i] > surv_40[i + 1]


main()
