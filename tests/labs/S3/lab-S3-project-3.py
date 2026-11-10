"""Lab S3-project-3: Empirical pairs-trading audit on Federal Reserve FX rates.

Audits all 15 currency pairs from data/fx_daily.csv (Federal Reserve H.10),
measuring formation cointegration test statistics against precomputed 5%
critical values and tracking out-of-sample half-lives.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


def ols_1d(y: list[float], x: list[float]) -> tuple[float, float]:
    m = len(y)
    mx = sum(x) / m
    my = sum(y) / m
    cov = sum((x[i] - mx) * (y[i] - my) for i in range(m))
    var_x = sum((x[i] - mx) ** 2 for i in range(m))
    beta = cov / var_x
    alpha = my - beta * mx
    return alpha, beta


def eg_t(y: list[float], x: list[float], split: int) -> float:
    alpha, beta = ols_1d(y[:split], x[:split])
    u = [y[t] - alpha - beta * x[t] for t in range(split)]
    m = len(u)
    du = [u[i] - u[i - 1] for i in range(1, m)]
    y_dep = du[1:]
    x0 = [u[t - 1] for t in range(2, m)]
    x1 = [du[t - 2] for t in range(2, m)]
    n_obs = len(y_dep)

    s00 = sum(x0[r] * x0[r] for r in range(n_obs))
    s01 = sum(x0[r] * x1[r] for r in range(n_obs))
    s11 = sum(x1[r] * x1[r] for r in range(n_obs))
    det = s00 * s11 - s01 * s01
    inv00 = s11 / det
    inv01 = -s01 / det
    sy0 = sum(x0[r] * y_dep[r] for r in range(n_obs))
    sy1 = sum(x1[r] * y_dep[r] for r in range(n_obs))
    gamma = inv00 * sy0 + inv01 * sy1
    delta = inv01 * sy0 + (s00 / det) * sy1

    res = [y_dep[r] - gamma * x0[r] - delta * x1[r] for r in range(n_obs)]
    rss = sum(r * r for r in res)
    sigma2 = rss / (n_obs - 2)
    se_gamma = math.sqrt(sigma2 * inv00)
    return gamma / se_gamma


def half_life(spread: list[float]) -> float:
    y = spread[1:]
    x = spread[:-1]
    _, phi = ols_1d(y, x)
    if phi <= 0.0:
        raise ValueError("phi <= 0")
    if phi >= 1.0:
        return math.inf
    return math.log(2.0) / (-math.log(phi))


def main() -> None:
    data_path = Path("data") / "fx_daily.csv"
    with data_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    currencies = ["AUD", "CAD", "CHF", "EUR", "GBP", "JPY"]
    n = len(rows)
    split = math.floor(0.6 * n)  # 4023
    eg_crit_5pct = -3.3287

    log_rates = {c: [math.log(float(r[c])) for r in rows] for c in currencies}

    print(f"Federal Reserve H.10 FX Audit (N={n}, Formation Split={split}, Critical Value={eg_crit_5pct}):")
    print("Pair    | Formation Alpha | Beta (Hedge) | EG t-stat | Trading Half-Life | Survives")
    print("-" * 75)

    survivor_count = 0
    for i in range(len(currencies)):
        for j in range(i + 1, len(currencies)):
            c1, c2 = currencies[i], currencies[j]
            y = log_rates[c1]
            x = log_rates[c2]
            alpha, beta = ols_1d(y[:split], x[:split])
            stat = eg_t(y, x, split)

            spread = [y[t] - alpha - beta * x[t] for t in range(split, n)]
            hl = half_life(spread)
            survives = (stat < eg_crit_5pct) and math.isfinite(hl)
            if survives:
                survivor_count += 1

            hl_str = f"{hl:6.2f} d" if math.isfinite(hl) else "    inf "
            print(
                f"{c1}/{c2:3s} |     {alpha:7.4f}     |    {beta:7.4f}   |"
                f"   {stat:6.4f}  |     {hl_str}      |  {survives}"
            )

    print("-" * 75)
    print(f"Total surviving pairs: {survivor_count} / 15")


main()
