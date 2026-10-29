"""d19_m02: An IRR request with a zero first flow is refused, as if the first flow had to be the outlay.

Mutant of the reference solution for the CF1 capital-budgeting engine (capbudget.py).
"""

from __future__ import annotations

import itertools
import math
import random
from collections.abc import Mapping, Sequence
from typing import Any

REQUIRED_FIELDS = ("capex", "life", "revenue", "cash_costs", "tax_rate", "nwc_share", "inflation")

# Search window for irr_roots, in the discount factor x = 1 / (1 + r). x in [1e-4, 1e4] is r in (-0.9999, 9999).
_X_LOW, _X_HIGH = 1e-4, 1e4
_GRID_POINTS = 4001


def _finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _check_rate(rate: float) -> None:
    if not _finite(rate) or rate <= -1.0:
        raise ValueError("rate must be a finite number above -1: a rate of -1 or less makes discount factors undefined")


def _check_project(project: Mapping[str, Any]) -> None:
    missing = [name for name in REQUIRED_FIELDS if name not in project]
    if missing:
        raise ValueError(f"the project is missing {missing}: every field of the specification is required")
    capex, life = project["capex"], project["life"]
    if not isinstance(capex, int) or isinstance(capex, bool) or capex <= 0:
        raise ValueError(
            "capex must be a positive whole number of cents: an investment with no outlay is not a project"
        )
    if not isinstance(life, int) or isinstance(life, bool) or life < 1:
        raise ValueError("life must be a whole number of years, at least 1: depreciation needs a positive life")
    revenue, costs = project["revenue"], project["cash_costs"]
    if len(revenue) != life or len(costs) != life:
        raise ValueError("revenue and cash_costs need exactly one entry per year of life")
    if not all(_finite(x) and x >= 0 for x in revenue):
        raise ValueError("every revenue must be a finite number of cents, zero or more")
    if not all(_finite(x) and x >= 0 for x in costs):
        raise ValueError(
            "every cash cost must be a finite number of cents, zero or more; costs are entered as positives"
        )
    tax_rate, share, inflation = project["tax_rate"], project["nwc_share"], project["inflation"]
    if not _finite(tax_rate) or not 0.0 <= tax_rate < 1.0:
        raise ValueError("tax_rate must be at least 0 and below 1")
    if not _finite(share) or not 0.0 <= share < 1.0:
        raise ValueError("nwc_share must be at least 0 and below 1: working capital is a share of the year's revenue")
    if not _finite(inflation) or inflation <= -1.0:
        raise ValueError("inflation must be a finite rate above -1")


def after_tax_cash_flows(project: Mapping[str, Any], real: bool = False) -> list[float]:
    """Incremental after-tax cash flows in cents, index t = 0 (the outlay) to t = life.

    Year t operating cash flow is (revenue - cash cost) * (1 - tax_rate) + depreciation * tax_rate, with
    straight-line depreciation capex / life. Working capital is nwc_share * revenue at the end of years 1 to life - 1
    and zero at the end of year life, so the year-t working-capital flow is -(nwc_t - nwc_(t-1)). With real=True
    each flow is divided by (1 + inflation) ** t.
    """
    _check_project(project)
    capex, life = int(project["capex"]), int(project["life"])
    tax_rate, share, inflation = float(project["tax_rate"]), float(project["nwc_share"]), float(project["inflation"])
    revenue = [float(x) for x in project["revenue"]]
    costs = [float(x) for x in project["cash_costs"]]
    depreciation = capex / life
    nwc = [0.0] * (life + 1)
    for t in range(1, life):
        nwc[t] = share * revenue[t - 1]
    flows = [-float(capex)]
    for t in range(1, life + 1):
        ebitda = revenue[t - 1] - costs[t - 1]
        tax = tax_rate * (ebitda - depreciation)
        working_capital = -(nwc[t] - nwc[t - 1])
        flows.append(ebitda - tax + working_capital)
    if real:
        flows = [cf / (1.0 + inflation) ** t for t, cf in enumerate(flows)]
    return flows


def npv(rate: float, flows: Sequence[float]) -> float:
    """Net present value in cents: sum of flows[t] / (1 + rate) ** t, index t = 0 first, rate per period."""
    _check_rate(rate)
    if len(flows) == 0:
        raise ValueError("flows is empty: a project with no cash flows has no value to discount")
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))


def irr_roots(flows: Sequence[float]) -> list[float]:
    """Each rate above -1 at which npv changes sign on the grid, ascending.

    The search runs on x = 1 / (1 + r) over [1e-4, 1e4]. Two roots between the same pair of neighbouring grid points
    can both be missed, since the polynomial keeps one sign at both points; the project page states this limit.
    """
    if len(flows) < 2:
        raise ValueError("irr_roots needs at least an outlay and one inflow")
    if flows[0] == 0:
        raise ValueError('a leading zero flow is not allowed')
    if all(cf == 0 for cf in flows):
        raise ValueError("every flow is zero: then every rate is a root, and the question has no answer")

    def poly(x: float) -> float:
        return sum(cf * x**t for t, cf in enumerate(flows))

    # The end samples are the window ends exactly: exp(log(1e4)) is 10000.00000000001, one ulp outside the window.
    xs = [
        math.exp(math.log(_X_LOW) + (math.log(_X_HIGH) - math.log(_X_LOW)) * k / (_GRID_POINTS - 1))
        for k in range(_GRID_POINTS)
    ]
    xs[0], xs[-1] = _X_LOW, _X_HIGH
    values = [poly(x) for x in xs]
    roots_x: list[float] = []
    # A root is reported only where the polynomial changes sign. Zero grid values are skipped, so a tangent zero
    # (the polynomial touches zero without crossing it, as -(x - 1) ** 2 does at x = 1) is never reported.
    nonzero = [k for k in range(_GRID_POINTS) if values[k] != 0.0]
    for k1, k2 in itertools.pairwise(nonzero):
        if values[k1] * values[k2] < 0.0:
            lo, hi, f_lo = xs[k1], xs[k2], values[k1]
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                f_mid = poly(mid)
                if f_mid == 0.0:
                    lo = hi = mid
                    break
                if f_mid * f_lo < 0.0:
                    hi = mid
                else:
                    lo, f_lo = mid, f_mid
                if hi - lo <= 1e-15 * hi:
                    break
            roots_x.append(0.5 * (lo + hi))
    # Only a sign change between two samples inside the window is reported. A zero exactly at an end of the window
    # is not reported, because no sample lies beyond it to show a sign change.
    return sorted(1.0 / x - 1.0 for x in roots_x)


def payback_period(flows: Sequence[float], rate: float = 0.0) -> float:
    """Payback in fractional years. rate = 0 is simple payback; rate > 0 discounts each flow first.

    The first year t with cumulative (discounted) flow >= 0 gives (t - 1) + (-cumulative at t - 1) / flow at t.
    Returns math.inf when the outlay is never recovered within the horizon.
    """
    _check_rate(rate)
    if len(flows) < 2:
        raise ValueError("payback needs an outlay and at least one inflow")
    if not flows[0] < 0:
        raise ValueError("flows[0] must be a negative outlay: payback measures the time to recover an investment")
    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]
    cumulative = discounted[0]
    for t in range(1, len(discounted)):
        if cumulative + discounted[t] >= 0.0:
            return (t - 1) + (-cumulative) / discounted[t]
        cumulative += discounted[t]
    return math.inf


def fisher_nominal(real: float, inflation: float) -> float:
    """Nominal rate from the exact Fisher form: (1 + nominal) = (1 + real) * (1 + inflation)."""
    _check_rate(real)
    _check_rate(inflation)
    return (1.0 + real) * (1.0 + inflation) - 1.0


def npv_monte_carlo(project: Mapping[str, Any], rate: float, n_draws: int, seed: int, volatility: float) -> list[float]:
    """Nominal NPVs in cents of n_draws simulated projects, one per draw, in draw order.

    Draw k takes one standard normal z from random.Random(seed).gauss(0, 1), in order, and scales every revenue by
    m = exp(volatility * z - volatility ** 2 / 2), so E[m] = 1. Cash costs are unchanged. NPV is affine in m, so the
    mean of the draws estimates the deterministic NPV with volatility zero.
    """
    _check_project(project)
    _check_rate(rate)
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError("seed must be a whole number")
    if not isinstance(n_draws, int) or isinstance(n_draws, bool) or n_draws < 2:
        raise ValueError("n_draws must be a whole number of at least 2: a standard error needs two draws")
    if not _finite(volatility) or volatility < 0.0:
        raise ValueError("volatility must be a finite number, zero or more")
    rng = random.Random(seed)
    out: list[float] = []
    for _ in range(n_draws):
        z = rng.gauss(0.0, 1.0)
        m = math.exp(volatility * z - volatility * volatility / 2.0)
        scaled = dict(project)
        scaled["revenue"] = [m * float(x) for x in project["revenue"]]
        out.append(npv(rate, after_tax_cash_flows(scaled)))
    return out
