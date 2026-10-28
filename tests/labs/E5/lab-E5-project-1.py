"""Rung 1 worked example: GDP growth, an inflation rate from a price index, and one cycle flag, on a SIMULATED path.

Standard library only. Every series here is SIMULATED: a seeded generator (seed 2026) draws 24 quarters, 2020 Q4 to
2026 Q3. The first four quarters are lags for the year-on-year inflation rate. The last twenty quarters are the
five-year window. All rates are in percent per year.

* GDP growth, annualised: 100 * ((Y_t / Y_(t-1)) ** 4 - 1), from the quarter-on-quarter change, compounded to a year.
* Inflation, year on year: 100 * (P_t / P_(t-4) - 1), from the price index P.
* Output gap, the log gap y_log of the conventions: 100 * (ln Y_t minus the least-squares trend of ln Y over the
  window).
* Cycle flag: "above trend and growing" when growth and the gap are both positive, "below trend and not growing" when
  both are zero or negative, and "mixed" otherwise.

Every printed rate and gap is rounded to two decimals from its unrounded float; the flag uses the unrounded values.
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


def output_gap(gdp: list[float], t: int) -> float:
    """The output gap in percent: 100 times ln Y_t minus the fitted trend at t, which is WINDOW - 1 in window time."""
    intercept, slope = trend_fit(gdp, t)
    return 100.0 * (math.log(gdp[t]) - (intercept + slope * (WINDOW - 1)))


def cycle_flag(growth: float, gap: float) -> str:
    """The cycle flag of the rule in the module docstring."""
    if growth > 0 and gap > 0:
        return "above trend and growing"
    if growth <= 0 and gap <= 0:
        return "below trend and not growing"
    return "mixed"


def main() -> None:
    path = simulated_path()
    gdp, price = path["gdp"], path["price"]
    latest = QUARTERS - 1
    growth = growth_annualised(gdp, latest)
    inflation = inflation_yoy(price, latest)
    gap = output_gap(gdp, latest)
    print("SIMULATED path, seed", SEED, "| latest quarter:", quarter_label(latest))
    print("GDP growth, annualised (%):", f"{growth:.2f}")
    print("inflation, year on year (%):", f"{inflation:.2f}")
    print("output gap (%):", f"{gap:.2f}")
    print("cycle flag:", cycle_flag(growth, gap))
    print("window:", quarter_label(latest - WINDOW + 1), "to", quarter_label(latest), "| quarters:", WINDOW)


main()
