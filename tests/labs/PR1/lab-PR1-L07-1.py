"""Lab 7: Out-of-sample backtesting: turnover, costs, and look-ahead bias.

SIMULATED: synthetic return series generated under seed 7.
Compares a strictly honest rolling-window backtest against an intentionally
contaminated look-ahead variant that peeks at period t return during allocation.
Demonstrates how look-ahead bias artificially inflates the out-of-sample Sharpe ratio.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    rng = random.Random(7)
    n_assets = 4
    h_periods = 120
    t_window = 60
    cost_rate = 0.001  # 10 basis points per unit of one-way turnover

    returns: list[list[float]] = [[rng.gauss(0.006, 0.04) for _ in range(n_assets)] for _ in range(h_periods)]

    def backtest(lookahead: bool) -> tuple[float, float, float]:
        k_dates = h_periods - t_window
        w_prev = [1.0 / n_assets] * n_assets
        net_returns: list[float] = []
        turnovers: list[float] = []

        for k in range(k_dates):
            t = t_window + k
            win = returns[t - t_window + 1 : t + 1] if lookahead else returns[t - t_window : t]

            mu_hat = [sum(win[s][i] for s in range(t_window)) / t_window for i in range(n_assets)]
            pos = [max(m, 0.0) for m in mu_hat]
            sum_pos = sum(pos)
            w = [p / sum_pos for p in pos] if sum_pos > 0 else [1.0 / n_assets] * n_assets

            turnover = sum(abs(w[i] - w_prev[i]) for i in range(n_assets))
            cost = cost_rate * turnover
            gross = sum(w[i] * returns[t][i] for i in range(n_assets))
            net = gross - cost

            net_returns.append(net)
            turnovers.append(turnover)
            w_prev = w

        mean_net = sum(net_returns) / k_dates
        var_net = sum((r - mean_net) ** 2 for r in net_returns) / (k_dates - 1)
        sr = mean_net / math.sqrt(var_net)
        mean_turnover = sum(turnovers) / k_dates
        return sr, mean_net, mean_turnover

    sr_honest, ret_honest, to_honest = backtest(lookahead=False)
    sr_lookahead, ret_lookahead, to_lookahead = backtest(lookahead=True)

    print(f"Honest backtest:    Net SR={sr_honest:.4f}, Net Ret={ret_honest:.4f}, TO={to_honest:.4f}")
    print(f"Lookahead backtest: Net SR={sr_lookahead:.4f}, Net Ret={ret_lookahead:.4f}, TO={to_lookahead:.4f}")
    print(f"Artificial Sharpe inflation: +{(sr_lookahead - sr_honest):.4f}")


main()
