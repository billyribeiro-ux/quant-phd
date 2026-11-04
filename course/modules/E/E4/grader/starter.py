"""Starter for the E4 project: solver.py, the solver for the price-informativeness model.

Implement the function in project.html, section "Rung 3 · Specification", then run the autograder there, or locally
with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Use the standard library only. Raise ValueError for the two named conditions, and return the three named keys. No
function may print or warn.
"""

from __future__ import annotations


def solve_model(noise_sd: float, info_cost: float) -> dict[str, float]:
    """The informed fraction, the price informativeness and the indifference gap at a noise volume and a cost."""
    raise NotImplementedError("solve_model is not written yet")
