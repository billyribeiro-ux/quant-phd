"""Starter for the SC1 project: bm_checks.py, the engine that checks the reflection principle on generated instances.

Implement every function to the contract in project.html, section "Rung 3 · Specification", then run the autograder
there, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Use the standard library only. No function prints or warns.
"""

from __future__ import annotations

from typing import Any


def reflection_tail(a: float, t: float) -> float:
    """P(M_t >= a) for a standard Brownian motion on [0, t], for a > 0 and t > 0. Raises ValueError per the spec."""
    raise NotImplementedError("reflection_tail is not written yet")


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    """The estimate and the standard error of P(max over the grid >= a) on the instance's seeded paths."""
    raise NotImplementedError("discrete_max_exceedance is not written yet")


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    """The fine-grid and coarse-grid exceedance counts on the same seeded paths."""
    raise NotImplementedError("nested_grid_counts is not written yet")


def srw_max_count(n: int, a: int) -> int:
    """The number of simple random walk paths of length n whose maximum reaches a, as an exact integer."""
    raise NotImplementedError("srw_max_count is not written yet")


def srw_terminal_count(n: int, a: int) -> int:
    """The number of simple random walk paths of length n whose final value is at least a, as an exact integer."""
    raise NotImplementedError("srw_terminal_count is not written yet")
