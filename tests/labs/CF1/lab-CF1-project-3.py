"""CF1 project lab 3 (rung 3, sanity run): reference numbers the engine must reproduce.

SIMULATED: the rung-1 project and the two-root flow below are written here. Neither is any company's project.
Money is in integer cents on input; the printed values are dollars or decimal rates. Standard library only. The random
draws use random.Random(42), in order, one gauss(0, 1) per draw, as the specification of npv_monte_carlo.

Run it once and compare each printed line with the engine on the same inputs. A line that differs is a defect in
one of the two. The printed numbers are a check, not a target to copy.
"""

from __future__ import annotations

import itertools
import math
import random

CAPEX = 900_000  # cents
LIFE = 3
REVENUE = [600_000, 650_000, 700_000]  # cents, years 1 to 3
CASH_COSTS = [200_000, 210_000, 220_000]  # cents, years 1 to 3
TAX_RATE = 0.25
NWC_SHARE = 0.10
RATE = 0.10
TWO_ROOT_FLOWS = [-100.0, 230.0, -132.0]  # dollars; the NPV has two sign changes and roots 0.1 and 0.2


def project_flows(revenue_scale: float) -> list[float]:
    """After-tax flows in dollars, t = 0 to 3, with every revenue multiplied by revenue_scale (the rung-1 rules)."""
    depreciation = CAPEX / LIFE
    revenue = [revenue_scale * x for x in REVENUE]
    nwc = [0.0] + [NWC_SHARE * revenue[t - 1] for t in range(1, LIFE)] + [0.0]
    flows = [-CAPEX / 100.0]
    for t in range(1, LIFE + 1):
        ebitda = revenue[t - 1] - CASH_COSTS[t - 1]
        tax = TAX_RATE * (ebitda - depreciation)
        flows.append((ebitda - tax - (nwc[t] - nwc[t - 1])) / 100.0)
    return flows


def npv(rate: float, flows: list[float]) -> float:
    """Net present value: sum of flows[t] / (1 + rate) ** t, t = 0 first."""
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))


def roots(flows: list[float]) -> list[float]:
    """Sign changes of the NPV on the grid -0.5 to 1.0, each bracket bisected to about 1e-12."""
    grid = [-0.5 + 0.0005 * k for k in range(3001)]
    found: list[float] = []
    for lo, hi in itertools.pairwise(grid):
        if npv(lo, flows) * npv(hi, flows) < 0.0:
            a, b = lo, hi
            for _ in range(60):
                mid = 0.5 * (a + b)
                if npv(a, flows) * npv(mid, flows) <= 0.0:
                    b = mid
                else:
                    a = mid
            found.append(0.5 * (a + b))
    return found


def payback(flows: list[float], rate: float = 0.0) -> float:
    """Payback in fractional years on flows discounted at rate: (t - 1) + (-cumulative at t - 1) / flow at t."""
    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]
    cumulative = discounted[0]
    for t in range(1, len(discounted)):
        if cumulative + discounted[t] >= 0.0:
            return (t - 1) + (-cumulative) / discounted[t]
        cumulative += discounted[t]
    return math.inf


def monte_carlo_draws(volatility: float, draws: int, seed: int) -> list[float]:
    """NPV in dollars of each draw, each scaling all revenue by m = exp(volatility * z - volatility ** 2 / 2)."""
    rng = random.Random(seed)
    out: list[float] = []
    for _ in range(draws):
        m = math.exp(volatility * rng.gauss(0.0, 1.0) - volatility * volatility / 2.0)
        out.append(npv(RATE, project_flows(m)))
    return out


def main() -> None:
    base = project_flows(1.0)
    print("rung-1 flows at t = 0 to 3, dollars:", ", ".join(f"{cf:.2f}" for cf in base))
    print(f"NPV of the rung-1 project at {RATE:.2f}: {npv(RATE, base):.2f} dollars")
    print("IRR roots of the two-root flow, to 6 decimals:", [round(r, 6) for r in roots(TWO_ROOT_FLOWS)])
    print("IRR roots of the rung-1 project, to 6 decimals:", [round(r, 6) for r in roots(base)])
    print(f"simple payback of the rung-1 project: {payback(base):.6f} years")
    print(f"discounted payback of the rung-1 project at {RATE:.2f}: {payback(base, RATE):.6f} years")
    print(f"simple payback of [-100, 60, 60]: {payback([-100.0, 60.0, 60.0]):.6f} years")
    nominal = (1.0 + 0.05) * (1.0 + 0.03) - 1.0
    print(f"Fisher nominal rate for real 0.05 and inflation 0.03: {nominal:.10f}")
    zero = monte_carlo_draws(0.0, 10, 42)
    print(f"Monte Carlo mean with zero volatility, 10 draws: {sum(zero) / len(zero):.2f} dollars")
    draws = monte_carlo_draws(0.2, 2000, 42)
    n = len(draws)
    mean = sum(draws) / n
    sd = math.sqrt(sum((d - mean) ** 2 for d in draws) / (n - 1))
    print(f"Monte Carlo with volatility 0.2, 2000 draws, seed 42: mean {mean:.2f} dollars")
    print(f"standard deviation {sd:.2f} dollars, standard error of the mean {sd / math.sqrt(n):.2f} dollars")
    negative = sum(1 for d in draws if d < 0.0)
    print(f"draws with a negative NPV: {negative} of {n}")
    print(f"lowest draw {min(draws):.2f} dollars, highest draw {max(draws):.2f} dollars")


main()
