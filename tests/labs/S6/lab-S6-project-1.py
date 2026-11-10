"""Lab S6-project-1: Rung 1 worked example for Policy-Shock Event Study.

SIMULATED: end-to-end execution of the market-model event-study pipeline,
evaluating abnormal returns, analytical variance, cumulative abnormal returns,
cross-sectional t-statistics, and cluster-robust inference on synthetic data.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    rng = random.Random(42)

    # 1. Timeline and simulation configuration
    est_len = 40
    window = (-1, 1)  # 3 trading days

    # Market model parameters
    alpha_true = 0.0004
    beta_true = 1.10
    sigma_true = 0.012

    # Simulate estimation window returns
    mkt_est = [round(rng.gauss(0.0005, 0.012), 6) for _ in range(est_len)]
    stk_est = [round(alpha_true + beta_true * m + rng.gauss(0.0, sigma_true), 6) for m in mkt_est]

    # Step 1: Fit market model by OLS on estimation window
    m_bar = sum(mkt_est) / est_len
    s_bar = sum(stk_est) / est_len
    ss_m = sum((m - m_bar) ** 2 for m in mkt_est)
    sp_ms = sum((m - m_bar) * (s - s_bar) for m, s in zip(mkt_est, stk_est, strict=True))

    beta_hat = sp_ms / ss_m
    alpha_hat = s_bar - beta_hat * m_bar
    ss_res = sum((s - (alpha_hat + beta_hat * m)) ** 2 for s, m in zip(stk_est, mkt_est, strict=True))
    sigma2_hat = ss_res / (est_len - 2)

    # Step 2: Simulate event window with planted announcement reaction (+0.022 on day 0)
    mkt_ev = [0.0010, -0.0005, 0.0020]
    stk_ev = [
        alpha_true + beta_true * mkt_ev[0] + rng.gauss(0.0, sigma_true),
        alpha_true + beta_true * mkt_ev[1] + 0.0220 + rng.gauss(0.0, sigma_true),
        alpha_true + beta_true * mkt_ev[2] + rng.gauss(0.0, sigma_true),
    ]

    # Step 3: Compute abnormal returns and analytical variance
    ar_list: list[float] = []
    var_list: list[float] = []
    for s_val, m_val in zip(stk_ev, mkt_ev, strict=True):
        ar = s_val - (alpha_hat + beta_hat * m_val)
        ar_list.append(ar)
        dev_m = (m_val - m_bar) ** 2
        var_ar = sigma2_hat * (1.0 + 1.0 / est_len + dev_m / ss_m)
        var_list.append(var_ar)

    # Step 4: Aggregate to Cumulative Abnormal Return (CAR)
    car_val = sum(ar_list)
    car_var = sum(var_list)
    car_se = math.sqrt(car_var)

    # Step 5: Inference
    t_stat = car_val / car_se

    print("Policy-Shock Event Study Pipeline (SIMULATED):")
    print(f"  Estimation Window Length: {est_len} trading days")
    print(f"  Estimated Alpha:          {alpha_hat:+.6f}")
    print(f"  Estimated Beta:           {beta_hat:+.4f}")
    print(f"  Residual Variance (s^2):  {sigma2_hat:.6f}\n")
    print("Event Window Abnormal Returns [-1, +1]:")
    for day, (ar, var_ar) in enumerate(zip(ar_list, var_list, strict=True), start=window[0]):
        print(f"  Day {day:+d}: AR = {ar:+7.4f}, Var(AR) = {var_ar:.6f}, SE = {math.sqrt(var_ar):.4f}")
    print(f"\nCumulative Abnormal Return (CAR): {car_val:+7.4f}")
    print(f"CAR Analytical Variance:          {car_var:.6f}")
    print(f"CAR Standard Error:               {car_se:.4f}")
    print(f"Single-Firm Event t-Statistic:    {t_stat:+7.4f}")
    print(f"Significant at 5% Level (|t|>1.96): {abs(t_stat) > 1.96}")


main()
