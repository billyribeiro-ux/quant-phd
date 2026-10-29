"""Starter for the M7 project: constrained_allocator.py.

Implement allocate() to the specification on the project page (section "Rung 3"), then run the autograder there, or
locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

The argument is the decoded case: the mapping that the payload of make_instance(seed) holds as JSON. Money does not
appear in this unit. Every function call validates its input and raises an exception for a case it cannot use. The
function must not print, warn or change its argument. Use the standard library only.
"""

from __future__ import annotations

from typing import Any


def allocate(instance: dict[str, Any]) -> dict[str, Any]:
    """Solve the constrained problem of the page and return the weights, the multipliers and the certificate."""
    raise NotImplementedError("allocate")
