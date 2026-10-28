"""M2 lab L13: forward and central difference approximations to f'(x), and the rounding turn-up.

Standard library only. The function is exp and the point is x = 1, so the exact derivative is e.
The step sizes h = 10^-k for k = 1 to 12 are evaluated in IEEE double precision. Nothing is random
and nothing is fetched, so the output is the same on every run on the same Python build. The
errors are measured against math.e, a value known in closed form, so the lab shows the errors as
they happen and does not assume a shape for them.
"""

from __future__ import annotations

import math
from collections.abc import Callable

X0 = 1.0
EXACT = math.exp(X0)  # the derivative of exp is exp, so f'(1) = e


def forward(f: Callable[[float], float], x: float, h: float) -> float:
    """Forward difference (f(x + h) - f(x)) / h, an approximation to f'(x) with error of order h."""
    return (f(x + h) - f(x)) / h


def central(f: Callable[[float], float], x: float, h: float) -> float:
    """Central difference (f(x + h) - f(x - h)) / (2h), an approximation to f'(x) with error of order h squared."""
    return (f(x + h) - f(x - h)) / (2.0 * h)


def sweep() -> list[tuple[int, float, float]]:
    """For k = 1 to 12, the absolute errors of both approximations at h = 10^-k, as (k, forward, central)."""
    rows: list[tuple[int, float, float]] = []
    for k in range(1, 13):
        h = 10.0 ** (-k)
        fwd = abs(forward(math.exp, X0, h) - EXACT)
        cen = abs(central(math.exp, X0, h) - EXACT)
        rows.append((k, fwd, cen))
    return rows


def main() -> None:
    rows = sweep()
    print("step h, forward error, central error")
    for k, fwd, cen in rows:
        print(f"1e-{k:02d} {fwd:.3e} {cen:.3e}")
    fwd_best = min(rows, key=lambda r: r[1])[0]
    cen_best = min(rows, key=lambda r: r[2])[0]
    print(f"forward error is smallest at h = 1e-{fwd_best:02d}")
    print(f"central error is smallest at h = 1e-{cen_best:02d}")
    f_at = {k: fwd for k, fwd, _ in rows}
    c_at = {k: cen for k, _, cen in rows}
    print(f"forward error ratio, h = 1e-2 over h = 1e-3: {f_at[2] / f_at[3]:.2f}")
    print(f"central error ratio, h = 1e-2 over h = 1e-3: {c_at[2] / c_at[3]:.2f}")


main()
