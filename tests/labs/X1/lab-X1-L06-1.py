"""Lab X1-L06-1: Real exchange rates and the Meese-Rogoff random-walk benchmark.

Evaluates out-of-sample 1-month-ahead forecasting errors for a driftless random walk
against structural fundamentals and real exchange rate mean-reversion models (Meese & Rogoff 1983).
"""

from __future__ import annotations

import math
import random


def run_random_walk_benchmark(
    seed: int = 55,
    n_obs: int = 150,
    window_size: int = 40,
) -> dict[str, float]:
    """Compare 1-month-ahead rolling out-of-sample forecast accuracy.

    Models:
      1. Random Walk Benchmark: E_t[s_{t+1}] = s_t
      2. Fundamentals Model: E_t[s_{t+1}] = alpha_hat + beta_hat * f_{t+1}
      3. Mean-Reversion Model: E_t[s_{t+1}] = s_t + theta_hat * (s_bar - s_t)
    """
    rng = random.Random(seed)

    # Generate fundamental series f_t (persistent AR(1))
    f: list[float] = [0.0]
    for _ in range(1, n_obs):
        f.append(0.95 * f[-1] + rng.gauss(0.0, 0.02))

    # Generate log spot exchange rate s_t (random walk with tiny fundamental loading)
    s: list[float] = [0.0]
    for t in range(1, n_obs):
        ds = 0.15 * (f[t] - f[t - 1]) + rng.gauss(0.0, 0.03)
        s.append(s[-1] + ds)

    eval_actual: list[float] = []
    rw_preds: list[float] = []
    fund_preds: list[float] = []
    mr_preds: list[float] = []

    for t in range(window_size, n_obs - 1):
        target = s[t + 1]
        eval_actual.append(target)

        # 1. Random walk forecast
        rw_pred = s[t]
        rw_preds.append(rw_pred)

        # 2. Fundamentals rolling regression
        s_win = s[t - window_size : t]
        f_win = f[t - window_size : t]
        mean_s = sum(s_win) / window_size
        mean_f = sum(f_win) / window_size
        var_f = sum((x - mean_f) ** 2 for x in f_win)
        cov_sf = sum((x - mean_f) * (y - mean_s) for x, y in zip(f_win, s_win, strict=True))
        beta = cov_sf / var_f if var_f > 1e-12 else 0.0
        alpha = mean_s - beta * mean_f
        fund_pred = alpha + beta * f[t + 1]
        fund_preds.append(fund_pred)

        # 3. Real exchange rate mean-reversion forecast (AR(1))
        # Estimate s_tau = c + rho * s_{tau-1}
        y_mr = s_win[1:]
        x_mr = s_win[:-1]
        m_x = sum(x_mr) / (window_size - 1)
        m_y = sum(y_mr) / (window_size - 1)
        v_x = sum((xi - m_x) ** 2 for xi in x_mr)
        c_xy = sum((xi - m_x) * (yi - m_y) for xi, yi in zip(x_mr, y_mr, strict=True))
        rho = c_xy / v_x if v_x > 1e-12 else 0.0
        c_val = m_y - rho * m_x
        mr_pred = c_val + rho * s[t]
        mr_preds.append(mr_pred)

    n_eval = len(eval_actual)
    rmse_rw = math.sqrt(sum((a - p) ** 2 for a, p in zip(eval_actual, rw_preds, strict=True)) / n_eval)
    rmse_fund = math.sqrt(sum((a - p) ** 2 for a, p in zip(eval_actual, fund_preds, strict=True)) / n_eval)
    rmse_mr = math.sqrt(sum((a - p) ** 2 for a, p in zip(eval_actual, mr_preds, strict=True)) / n_eval)

    # Theil's U relative to Random Walk
    u_fund = rmse_fund / rmse_rw
    u_mr = rmse_mr / rmse_rw

    return {
        "n_eval": float(n_eval),
        "rmse_rw": round(rmse_rw, 5),
        "rmse_fund": round(rmse_fund, 5),
        "theil_u_fund": round(u_fund, 4),
        "rmse_mr": round(rmse_mr, 5),
        "theil_u_mr": round(u_mr, 4),
    }


def main() -> None:
    print("Lab X1-L06-1 | Meese-Rogoff Random-Walk Benchmark Horse Race")
    print("-------------------------------------------------------------")

    res = run_random_walk_benchmark(seed=55, n_obs=150, window_size=40)

    print(f"Evaluation Observations (out-of-sample): {int(res['n_eval'])}")
    print(f"{'Forecasting Model':<28} | {'1-Mo RMSE':<10} | {'Theil U (vs RW)':<15}")
    print("-" * 58)
    print(f"{'1. Driftless Random Walk':<28} | {res['rmse_rw']:<10.5f} | {'1.0000 (Benchmark)':<15}")
    print(f"{'2. Monetary Fundamentals':<28} | {res['rmse_fund']:<10.5f} | {res['theil_u_fund']:<15.4f}")
    print(f"{'3. Mean-Reversion AR(1)':<28} | {res['rmse_mr']:<10.5f} | {res['theil_u_mr']:<15.4f}")
    print("\nEmpirical Takeaway (Meese & Rogoff 1983):")
    rw_wins = res["theil_u_fund"] > 1.0 and res["theil_u_mr"] > 1.0
    print(f"  Random Walk Beats Both Models (Theil's U > 1.0): {rw_wins}")


main()
