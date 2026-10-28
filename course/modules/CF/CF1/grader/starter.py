"""Starter for the CF1 project: capbudget.py.

Implement every function so that it matches the specification on the project page, then run the autograder, or
locally, with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Every function validates its inputs and raises ValueError with a message that names the rule that failed. None may
print or warn, none may change its arguments, and each returns fresh objects. Money is whole cents on input; derived
cash flows are floats in cents and are not rounded.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


def after_tax_cash_flows(project: Mapping[str, Any], real: bool = False) -> list[float]:
    """Incremental after-tax cash flows in cents, index t = 0 (outlay) to t = life. See the specification."""
    raise NotImplementedError("after_tax_cash_flows")


def npv(rate: float, flows: Sequence[float]) -> float:
    """Net present value in cents: sum of flows[t] / (1 + rate) ** t. rate must be finite and above -1."""
    raise NotImplementedError("npv")


def irr_roots(flows: Sequence[float]) -> list[float]:
    """Every rate above -1 at which npv(rate, flows) is zero, ascending, each to within 1e-7."""
    raise NotImplementedError("irr_roots")


def payback_period(flows: Sequence[float], rate: float = 0.0) -> float:
    """Fractional years to recover the outlay; rate > 0 discounts first; math.inf if never recovered."""
    raise NotImplementedError("payback_period")


def fisher_nominal(real: float, inflation: float) -> float:
    """Nominal rate n with (1 + n) = (1 + real) * (1 + inflation)."""
    raise NotImplementedError("fisher_nominal")


def npv_monte_carlo(project: Mapping[str, Any], rate: float, n_draws: int, seed: int, volatility: float) -> list[float]:
    """Nominal NPV in cents of each of n_draws draws, in order, from the seeded revenue shocks in the specification."""
    raise NotImplementedError("npv_monte_carlo")
