"""Print the estimate and the Hessian pivots for the fixed 26-response participant of test_project.py.

Run from a directory holding elicit.py (= grader/reference.py), test_project.py and instance.py.
"""

from __future__ import annotations

import math
import sys
from typing import Any

import elicit as sol  # type: ignore[import-not-found]
import test_project as tp  # type: ignore[import-not-found]

responses: list[dict[str, Any]] = [
    {"pair_id": i, "choice": c, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb}
    for i, c, pa, qa, pb, qb in tp.FIXED_26_ANSWERS
]
parsed = [sol._parse(r) for r in responses]
xi = sol._maximise(parsed)
print("xi", [repr(x) for x in xi])
print("gamma_hat", 1.0 / (1.0 + math.exp(-xi[0])), "lambda_hat", math.exp(xi[1]), "kappa_hat", math.exp(xi[2]))


def f(t: list[float]) -> float:
    return sol._objective(t, parsed)


grad, hess = sol._gradient_and_hessian(f, xi)
print("grad", [f"{g:.3e}" for g in grad])
print("hess", [[f"{h:.6e}" for h in row] for row in hess])
neg = [[-h for h in row] for row in hess]
# leading principal minors and the Cholesky pivots of -Hessian
for k in range(1, 4):
    sub = [row[:k] for row in neg[:k]]
    print(f"leading minor {k}:", f"{sol._cholesky(sub) is not None=}")
import itertools

ok = sol._cholesky(neg)
print("cholesky of -H:", "None (not PD)" if ok is None else [[f"{v:.6e}" for v in row] for row in ok])
