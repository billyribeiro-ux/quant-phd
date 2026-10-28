"""Starter for the M1 project: annuity_engine.py, the annuity and mortgage engine.

Implement every function to the contract in project.html, section "Rung 3 · Specification", then run the
autograder there, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Use the standard library only. Every function must validate its inputs and raise ValueError for the conditions
the specification names. No function may print or warn.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScheduleRow:
    """One month of an amortization schedule. Every money field is an integer number of cents."""

    period: int
    opening_cents: int
    interest_cents: int
    principal_cents: int
    payment_cents: int
    closing_cents: int


def annuity_factor(rate: float, periods: int) -> float:
    """Present value of 1 paid at the end of each of `periods` periods, at the per-period rate `rate`."""
    raise NotImplementedError("annuity_factor is not written yet")


def annuity_due_factor(rate: float, periods: int) -> float:
    """Present value of 1 paid at the start of each of `periods` periods."""
    raise NotImplementedError("annuity_due_factor is not written yet")


def perpetuity_factor(rate: float) -> float:
    """Present value of 1 paid at the end of every period, forever, at a positive per-period rate."""
    raise NotImplementedError("perpetuity_factor is not written yet")


def growing_perpetuity_factor(rate: float, growth: float) -> float:
    """Present value of a payment of 1 at the end of period 1, growing by (1 + growth) each period, forever."""
    raise NotImplementedError("growing_perpetuity_factor is not written yet")


def level_payment_cents(principal_cents: int, annual_rate: float, months: int) -> int:
    """The level monthly payment, in integer cents, to the nearest cent."""
    raise NotImplementedError("level_payment_cents is not written yet")


def amortization_schedule(principal_cents: int, annual_rate: float, months: int) -> tuple[ScheduleRow, ...]:
    """The full monthly schedule of a level-payment loan, one ScheduleRow per month."""
    raise NotImplementedError("amortization_schedule is not written yet")
