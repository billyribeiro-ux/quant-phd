"""Starter for the E3 project: elicit.py, the preference-elicitation engine.

Implement every function to the contract in project.html, section "Rung 3 · Specification", then run the
autograder there, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Use the standard library only. Every money output is an int number of cents. Every function validates its inputs
and raises ValueError for the conditions the specification names. No function may print or warn.
"""

from __future__ import annotations

from fractions import Fraction


def certainty_equivalent_cents(
    model: str,
    prizes_cents: list[int],
    probabilities: list[Fraction],
    params: dict[str, float],
    wealth_cents: int,
) -> int:
    """The certainty equivalent of a lottery, in whole cents, rounded once with an exact half going up."""
    raise NotImplementedError("certainty_equivalent_cents is not written yet")


def log_likelihood(responses: list[dict[str, object]], params: dict[str, float]) -> float:
    """The log-likelihood of the logit choice model for the responses, at the parameters gamma, lambda and kappa."""
    raise NotImplementedError("log_likelihood is not written yet")


def estimate(responses: list[dict[str, object]]) -> dict[str, float]:
    """The maximum-likelihood estimates of gamma, lambda and kappa, with their standard errors."""
    raise NotImplementedError("estimate is not written yet")
