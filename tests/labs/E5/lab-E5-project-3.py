"""Rung 3 check: the default state of the macro dashboard, recomputed from the inputs the dashboard uses.

Standard library only. Two kinds of input:

* SIMULATED: GDP, the price index, the unemployment rate and the policy rate are the seeded path of rung 1
  (seed 2026, 2020 Q4 to 2026 Q3). None of them is a real series.
* REAL: the term spread is read from data/ust_daily.csv, the embedded H.15 snapshot of the Board of Governors of the
  Federal Reserve System (H.15 Selected Interest Rates; retrieved 2026-10-20; citation and licence in the project's
  data section). The spread is the 10-year constant-maturity yield (cmt_10y) minus the 3-month Treasury bill rate
  (tbill_3m), both in percent per year. The bill rate is published on a discount basis and the 10-year on a
  constant-maturity basis, so the difference mixes two bases; this lab does not convert either. Each calendar quarter's
  spread is the exact average (fractions.Fraction) of the days on which both yields are published.

The default state is the window of 20 quarters that ends at the latest quarter, 2026 Q3. The dashboard rules are:

* growth, the output gap and inflation as in rung 1;
* inflation gap: inflation minus the target, 2.0 percent per year;
* unemployment gap: the unemployment rate minus the natural rate of unemployment, 4.0 percent;
* Taylor-rule value: i_star = r_n + pi_yoy + PHI_PI * (pi_yoy - target) + PHI_Y * y_log, where pi_yoy is the
  year-on-year inflation rate and y_log the log output gap of the conventions, and r_n = 2.0 percent per year (the
  natural real rate), PHI_PI = 0.5 and PHI_Y = 0.5 (stated assumptions, not estimates);
* policy gap: the policy rate minus the Taylor-rule value;
* term spread: the quarter average above.

The target, the natural rates and the coefficients are stated assumptions of this dashboard.
Every printed rate, gap and spread is rounded to two decimals from its unrounded value; day counts are integers.
"""

import math
import random
from fractions import Fraction
from pathlib import Path

SEED = 2026
QUARTERS = 24
WINDOW = 20
TARGET = 2.0
NATURAL_REAL_RATE = 2.0
NATURAL_UNEMPLOYMENT = 4.0
PHI_PI = 0.5
PHI_Y = 0.5
DATA_FILE = "ust_daily.csv"


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


def output_gap(gdp: list[float], t: int) -> float:
    """The output gap in percent: 100 times ln Y_t minus the least-squares trend in ln Y over the window ending at t."""
    first = t - WINDOW + 1
    xs = [float(k) for k in range(WINDOW)]
    ys = [math.log(gdp[first + k]) for k in range(WINDOW)]
    xbar = sum(xs) / WINDOW
    ybar = sum(ys) / WINDOW
    slope = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys, strict=True)) / sum((x - xbar) ** 2 for x in xs)
    intercept = ybar - slope * xbar
    return 100.0 * (math.log(gdp[t]) - (intercept + slope * (WINDOW - 1)))


def taylor_value(inflation: float, gap: float) -> float:
    """The policy rate the Taylor-rule value prescribes, in percent per year, at the dashboard's stated parameters."""
    return NATURAL_REAL_RATE + inflation + PHI_PI * (inflation - TARGET) + PHI_Y * gap


def cycle_flag(growth: float, gap: float) -> str:
    """The cycle flag of rung 1: above trend and growing, below trend and not growing, or mixed."""
    if growth > 0 and gap > 0:
        return "above trend and growing"
    if growth <= 0 and gap <= 0:
        return "below trend and not growing"
    return "mixed"


def sign(value: float | Fraction) -> str:
    """The sign of a number as a word: positive, negative or zero."""
    return "positive" if value > 0 else "negative" if value < 0 else "zero"


def read_quarter_spreads(file: Path) -> dict[str, tuple[Fraction, int]]:
    """Each quarter's average term spread (exact) and the number of days in it, from the H.15 snapshot.

    The file's header must be date,tbill_3m,cmt_10y. A value that is not a decimal number raises ValueError. A day on
    which either yield is blank is skipped, so each quarter averages only the days on which both are published.
    """
    totals: dict[str, Fraction] = {}
    days: dict[str, int] = {}
    with file.open(encoding="utf-8") as handle:
        header = next(handle).strip().split(",")
        if header != ["date", "tbill_3m", "cmt_10y"]:
            raise ValueError(f"unexpected header {header}")
        for line in handle:
            date, tbill, cmt = line.strip().split(",")
            if tbill == "" or cmt == "":
                continue
            label = f"{int(date[:4])} Q{(int(date[5:7]) - 1) // 3 + 1}"
            totals[label] = totals.get(label, Fraction(0)) + (Fraction(cmt) - Fraction(tbill))
            days[label] = days.get(label, 0) + 1
    return {label: (totals[label] / days[label], days[label]) for label in totals}


def main() -> None:
    path = simulated_path()
    gdp, price = path["gdp"], path["price"]
    unemployment, policy = path["unemployment"], path["policy"]
    spreads = read_quarter_spreads(Path("data") / DATA_FILE)
    latest = QUARTERS - 1
    print(
        "default state: window", quarter_label(latest - WINDOW + 1), "to", quarter_label(latest), "| quarters:", WINDOW
    )
    print("SIMULATED: GDP, price, unemployment, policy rate | REAL: term spread from", DATA_FILE)
    print("quarter | growth % | inflation % | gap % | unemployment % | policy % | Taylor % | policy gap pp | spread pp")
    for t in range(latest - 3, latest + 1):
        label = quarter_label(t)
        growth = growth_annualised(gdp, t)
        inflation = inflation_yoy(price, t)
        gap = output_gap(gdp, t)
        taylor = taylor_value(inflation, gap)
        spread, _ = spreads[label]
        print(
            f"{label} | {growth:.2f} | {inflation:.2f} | {gap:.2f} | {unemployment[t]:.2f} | {policy[t]:.2f}"
            f" | {taylor:.2f} | {policy[t] - taylor:.2f} | {float(spread):.2f}"
        )
    days = [spreads[quarter_label(t)][1] for t in range(latest - 3, latest + 1)]
    print("days averaged for the spread, 2025 Q4 to 2026 Q3:", days)
    growth = growth_annualised(gdp, latest)
    inflation = inflation_yoy(price, latest)
    gap = output_gap(gdp, latest)
    taylor = taylor_value(inflation, gap)
    spread, _ = spreads[quarter_label(latest)]
    print("signal, GDP growth:", sign(growth))
    print("signal, output gap:", sign(gap))
    print("signal, inflation minus target:", sign(inflation - TARGET))
    print("signal, unemployment minus natural rate:", sign(unemployment[latest] - NATURAL_UNEMPLOYMENT))
    print("signal, policy rate minus Taylor value:", sign(policy[latest] - taylor))
    print("signal, term spread:", sign(spread))
    print("cycle flag:", cycle_flag(growth, gap))


main()
