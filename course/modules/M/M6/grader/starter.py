"""Starter for the M6 project: martingale_checks.py, the engine that checks the three martingale results.

Implement every function to the contract in project.html, section "Rung 3 · Specification", then run the autograder
there, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Use the standard library only. Every probability is an exact fractions.Fraction. Every money amount is an integer
number of cents, rounded once, half up. No function prints or warns.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any


def stopped_value_expectation(instance: dict[str, Any]) -> Fraction:
    """E[S_tau] for the fair or biased walk and the stopping rule of the instance; raises ValueError per the spec."""
    raise NotImplementedError("stopped_value_expectation is not written yet")


def doob_max_probability(instance: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    """The probability that max |S_k| reaches lam up to the horizon, and the bound E|S_N| / lam."""
    raise NotImplementedError("doob_max_probability is not written yet")


def doubling_outcome(instance: dict[str, Any]) -> dict[str, int | Fraction]:
    """The doubling strategy with finite capital: the bets allowed, the probabilities, the wealths and E[final]."""
    raise NotImplementedError("doubling_outcome is not written yet")


def dyadic_martingale_error(instance: dict[str, Any], n: int) -> Fraction:
    """E[(M_n - Y)^2] for the dyadic martingale of Y(x) = x on [0, 1], exact."""
    raise NotImplementedError("dyadic_martingale_error is not written yet")


def dyadic_martingale_value(instance: dict[str, Any], n: int, x: Fraction) -> Fraction:
    """M_n(x): the midpoint of the level-n dyadic cell that contains x, for x in [0, 1]."""
    raise NotImplementedError("dyadic_martingale_value is not written yet")
