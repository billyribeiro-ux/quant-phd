"""Starter for the M4 project: tail_risk.py, the tail-risk simulator. All inputs are SIMULATED.

Implement every function to the specification in project.html, Rung 3 · Specification, then run the autograder there,
or locally with the flags the page shows:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Use the standard library only. Every function validates its inputs and raises ValueError for the conditions the
specification names. No function prints or warns.
"""

from __future__ import annotations


def matched_scale(nu: int) -> float:
    """The factor (nu - 2) / nu that matches a Student-t draw's covariance to the target. Requires nu > 2."""
    raise NotImplementedError("matched_scale is not written yet")


def simulate_losses(
    position_cents: list[int],
    cov: list[list[float]],
    n_draws: int,
    seed: int,
    family: str,
    nu: int | None,
) -> list[int]:
    """One portfolio loss per draw, in integer cents: loss = -sum_i w_i r_i, rounded once with round()."""
    raise NotImplementedError("simulate_losses is not written yet")


def quantile_99(losses_cents: list[int]) -> int:
    """The 99% loss: the order statistic with 1-based index ceil(0.99 n), computed in exact integers."""
    raise NotImplementedError("quantile_99 is not written yet")
