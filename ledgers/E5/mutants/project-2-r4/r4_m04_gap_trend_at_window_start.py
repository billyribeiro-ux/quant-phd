"""Rung 2 completed solution: the term spread and the output gap of the latest quarter, on a SIMULATED path.

Standard library only. Every series here is SIMULATED: the macro path is the path of the rung 1 worked example
(seed 2026, 2020 Q4 to 2026 Q3), and the 24 quarterly pairs of yields are drawn from a seeded generator (seed 2027)
around the policy rate. The yields are not the embedded snapshot read in rung 3. All rates are in percent per year.

* Term spread, in percentage points: the 10-year constant-maturity yield minus the 3-month bill rate, both in
  percent per year, for the latest quarter. This lab draws 24 SIMULATED quarterly pairs of yields and reads the latest
  one, so no mean of daily spreads is taken here.
* Output gap, the log gap y_log of the conventions: 100 * (ln Y_t minus the fitted trend at t), where the trend is the
  least-squares line in ln Y over the window of WINDOW quarters that ends at t, read at the window's last quarter.
* Growth and inflation: as in the rung 1 worked example.

Every printed rate and spread is rounded to two decimals from its unrounded float.
"""

import math
import random

SEED = 2026
QUARTERS = 24
WINDOW = 20


def quarter_label(k: int) -> str:
    """The quarter k of the path, where k = 0 is 2020 Q4, written as year and quarter, for example 2026 Q3."""
    month_index = 9 + 3 * k  # months after January 2020; 9 is October 2020
    year = 2020 + month_index // 12
    quarter = (month_index % 12) // 3 + 1
    return f"{year} Q{quarter}"


def simulated_path(seed: int = SEED) -> dict[str, list[float]]:
    """A SIMULATED quarterly path: GDP level in billions, price index (2020 Q4 = 100), unemployment and policy rate."""
    rng = random.Random(seed)
    gdp = [20000.0]
    for _ in range(QUARTERS - 1):
        gdp.append(gdp[-1] * (1 + 0.004 + 0.012 * (rng.random() - 0.5)))
    price = [100.0]
    for _ in range(QUARTERS - 1):
        price.append(price[-1] * (1 + 0.005 + 0.004 * (rng.random() - 0.5)))
    unemployment = [4.2]
    for _ in range(QUARTERS - 1):
        step = unemployment[-1] + 0.4 * (rng.random() - 0.5)
        unemployment.append(min(7.0, max(3.5, step)))
    policy = [1.0]
    for _ in range(QUARTERS - 1):
        policy.append(max(0.0, policy[-1] + 0.5 * (rng.random() - 0.5)))
    return {"gdp": gdp, "price": price, "unemployment": unemployment, "policy": policy}


def simulated_yields(policy: list[float], seed: int = SEED + 1) -> dict[str, list[float]]:
    """SIMULATED quarterly yields in percent per year: the 3-month bill tracks the policy rate; the 10-year is above."""
    rng = random.Random(seed)
    tbill = [max(0.0, p + 0.1 * (rng.random() - 0.5)) for p in policy]
    cmt = [p + 0.8 + 0.8 * (rng.random() - 0.5) for p in policy]
    return {"tbill_3m": tbill, "cmt_10y": cmt}


def growth_annualised(gdp: list[float], t: int) -> float:
    """GDP growth in percent per year: the quarter-on-quarter ratio raised to the fourth power, minus one."""
    return 100.0 * ((gdp[t] / gdp[t - 1]) ** 4 - 1.0)


def inflation_yoy(price: list[float], t: int) -> float:
    """Inflation in percent per year: the change in the price index over the four quarters ending at t."""
    return 100.0 * (price[t] / price[t - 4] - 1.0)


def trend_fit(gdp: list[float], t: int) -> tuple[float, float]:
    """The least-squares intercept and slope of ln Y over the window of WINDOW quarters that ends at t.

    The time index inside the window runs 0 to WINDOW - 1, so the intercept is the trend at the window's first quarter.
    """
    first = t - WINDOW + 1
    xs = [float(k) for k in range(WINDOW)]
    ys = [math.log(gdp[first + k]) for k in range(WINDOW)]
    xbar = sum(xs) / WINDOW
    ybar = sum(ys) / WINDOW
    slope = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys, strict=True)) / sum((x - xbar) ** 2 for x in xs)
    return ybar - slope * xbar, slope


def main() -> None:
    path = simulated_path()
    gdp, price = path["gdp"], path["price"]
    yields = simulated_yields(path["policy"])
    latest = QUARTERS - 1
    growth = growth_annualised(gdp, latest)
    inflation = inflation_yoy(price, latest)
    intercept, slope = trend_fit(gdp, latest)
    spread = yields["cmt_10y"][latest] - yields["tbill_3m"][latest]
    gap = 100.0 * (math.log(gdp[latest]) - intercept)
    print("SIMULATED path, seed", SEED, "| latest quarter:", quarter_label(latest))
    print("GDP growth, annualised (%):", f"{growth:.2f}")
    print("inflation, year on year (%):", f"{inflation:.2f}")
    print("term spread, 10-year minus 3-month (pp):", f"{spread:.2f}")
    print("output gap (%):", f"{gap:.2f}")


main()
