"""Lab 6: The Out-of-Sample Volatility Management Critique (Cederburg et al. 2020).

Demonstrates the critique of Cederburg, O'Doherty, Wang & Yan (2020):
When the scaling constant c is estimated strictly out-of-sample using expanding windows
(eliminating look-ahead bias) and rebalancing transaction costs are deducted,
the volatility-management alpha is substantially attenuated.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # SIMULATED: Multi-decade factor return and realized variance history (480 months / 40 years)
    rng = np.random.default_rng(42)
    n_months = 480
    days_per_month = 21
    cost_rate = 0.0010  # 10 bps transaction cost on turnover

    monthly_returns = np.zeros(n_months)
    realized_variance = np.zeros(n_months)

    vol_state = 0.01
    for m in range(n_months):
        daily_rets = np.zeros(days_per_month)
        for d in range(days_per_month):
            z = rng.standard_normal()
            daily_rets[d] = 0.0004 + vol_state * z
            vol_state = max(0.004, min(0.04, 0.95 * vol_state + 0.05 * 0.01 - 0.2 * daily_rets[d]))
        monthly_returns[m] = float(np.sum(daily_rets))
        realized_variance[m] = float(np.sum(daily_rets**2))

    # Evaluation window: burn-in 120 months (10 years) for out-of-sample estimation
    burn_in = 120
    eval_len = n_months - 1 - burn_in

    # 1. Full In-Sample Scaling (Moreira-Muir lookahead benchmark)
    unscaled_all = (1.0 / realized_variance[:-1]) * monthly_returns[1:]
    target_all = monthly_returns[1:]
    c_in_sample = float(np.std(target_all, ddof=1) / np.std(unscaled_all, ddof=1))

    # Evaluate over the evaluation window [burn_in:]
    managed_is = c_in_sample * unscaled_all[burn_in:]
    target_eval = target_all[burn_in:]

    # 2. Strict Out-of-Sample Expanding Window Estimation (Cederburg et al.)
    managed_oos = np.zeros(eval_len)
    w_oos = np.zeros(eval_len)
    w_is = (c_in_sample / realized_variance[:-1])[burn_in:]

    for idx, t in enumerate(range(burn_in, n_months - 1)):
        # Estimate c strictly using past data up to month t-1
        past_target = monthly_returns[1 : t + 1]
        past_unscaled = (1.0 / realized_variance[:t]) * monthly_returns[1 : t + 1]
        c_t = float(np.std(past_target, ddof=1) / np.std(past_unscaled, ddof=1))
        # Weight for month t+1 chosen at month t
        w_t = c_t / realized_variance[t]
        w_oos[idx] = w_t
        managed_oos[idx] = w_t * monthly_returns[t + 1]

    # 3. Transaction Costs Deduction
    # Monthly turnover: |w_t - w_{t-1} * (1 + r_t)|
    turnover_is = np.zeros(eval_len)
    turnover_oos = np.zeros(eval_len)
    for i in range(1, eval_len):
        turnover_is[i] = abs(w_is[i] - w_is[i - 1] * (1.0 + target_eval[i - 1]))
        turnover_oos[i] = abs(w_oos[i] - w_oos[i - 1] * (1.0 + target_eval[i - 1]))

    managed_oos_net = managed_oos - cost_rate * turnover_oos

    # Spanning regressions: strategy = alpha + beta * target_eval
    def run_regression(y: np.ndarray, x_in: np.ndarray) -> tuple[float, float, float]:
        x = np.column_stack([np.ones(len(x_in)), x_in])
        b_hat = np.linalg.lstsq(x, y, rcond=None)[0]
        alpha = float(b_hat[0])
        res = y - x @ b_hat
        s2 = float(np.sum(res**2) / (len(y) - 2))
        se = float(np.sqrt(s2 * np.linalg.inv(x.T @ x)[0, 0]))
        return alpha * 12.0, alpha / se, float(b_hat[1])

    alpha_is, t_is, _beta_is = run_regression(managed_is, target_eval)
    alpha_oos, t_oos, _beta_oos = run_regression(managed_oos, target_eval)
    alpha_oos_net, t_oos_net, _beta_oos_net = run_regression(managed_oos_net, target_eval)

    sr_base = float(np.mean(target_eval) / np.std(target_eval, ddof=1) * np.sqrt(12.0))
    sr_is = float(np.mean(managed_is) / np.std(managed_is, ddof=1) * np.sqrt(12.0))
    sr_oos = float(np.mean(managed_oos) / np.std(managed_oos, ddof=1) * np.sqrt(12.0))
    sr_oos_net = float(np.mean(managed_oos_net) / np.std(managed_oos_net, ddof=1) * np.sqrt(12.0))

    print(f"Base Factor Sharpe: {sr_base:.4f}")
    print(f"In-Sample Managed Alpha: {alpha_is * 100:.2f}%, t-stat: {t_is:.2f}, SR: {sr_is:.4f}")
    print(f"Out-of-Sample Managed Alpha (Gross): {alpha_oos * 100:.2f}%, t-stat: {t_oos:.2f}, SR: {sr_oos:.4f}")
    print(
        f"Out-of-Sample Managed Alpha (Net 10bps): {alpha_oos_net * 100:.2f}%, "
        f"t-stat: {t_oos_net:.2f}, SR: {sr_oos_net:.4f}"
    )
    print(f"Average Monthly Turnover (OOS): {float(np.mean(turnover_oos[1:])) * 100:.2f}%")
    print(f"Alpha Attenuation (IS to Net OOS): {(alpha_is - alpha_oos_net) * 100:.2f}% percentage points")


main()
