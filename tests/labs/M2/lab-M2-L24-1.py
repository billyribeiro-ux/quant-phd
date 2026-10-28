"""M2 lab L24: where finite-difference derivatives fail, a kink and a cancellation, on decade step sizes.

SIMULATED: the two functions are test functions chosen for this lab, not market data.
Part A is a kink. f(x) = |x| is not differentiable at 0. The forward quotient, the backward quotient and the central
quotient are computed at h = 10**-1 to 10**-6. They are exact in float arithmetic here, and they show that the
quotients converge to different limits (+1 and -1 for the one-sided quotients, 0 for the central quotient) instead of
to one derivative.
Part B is a smooth function with cancellation. f(x) = exp(x) at x0 = 1, whose derivative is e. The forward and central
quotients are computed at h = 10**-k for k = 1 to 15. Their errors fall while the truncation error dominates, then
rise again as the subtraction of nearly equal function values loses digits. The lab prints the decade with the smallest
error for each quotient. The grid is decades only, so the printed minimum is a grid result, not the exact optimum.
Standard library only; no randomness and no network access.
"""

from __future__ import annotations

import math
from collections.abc import Callable

KINK_EXPONENTS: tuple[int, ...] = (1, 2, 3, 4, 5, 6)
SMOOTH_EXPONENTS: tuple[int, ...] = tuple(range(1, 16))
X0 = 1.0


def absolute(x: float) -> float:
    """f(x) = |x|."""
    return abs(x)


def smooth(x: float) -> float:
    """f(x) = exp(x), with f'(x) = exp(x)."""
    return math.exp(x)


def forward(fun: Callable[[float], float], x: float, h: float) -> float:
    """The forward quotient (fun(x + h) - fun(x)) / h. The step h must be positive."""
    if h <= 0.0:
        raise ValueError(f"the step must be positive, got {h}")
    return (fun(x + h) - fun(x)) / h


def backward(fun: Callable[[float], float], x: float, h: float) -> float:
    """The backward quotient (fun(x) - fun(x - h)) / h. The step h must be positive."""
    if h <= 0.0:
        raise ValueError(f"the step must be positive, got {h}")
    return (fun(x) - fun(x - h)) / h


def central(fun: Callable[[float], float], x: float, h: float) -> float:
    """The central quotient (fun(x + h) - fun(x - h)) / (2 h). The step h must be positive."""
    if h <= 0.0:
        raise ValueError(f"the step must be positive, got {h}")
    return (fun(x + h) - fun(x - h)) / (2.0 * h)


def main() -> None:
    print("Part A: f(x) = |x| at x = 0, quotients at h = 10^-k")
    for k in KINK_EXPONENTS:
        h = 10.0**-k
        print(
            f"k = {k}: forward {forward(absolute, 0.0, h):+.6f} "
            f"backward {backward(absolute, 0.0, h):+.6f} central {central(absolute, 0.0, h):+.6f}"
        )

    target = math.e
    print(f"Part B: f(x) = exp(x) at x0 = 1, true derivative e = {target:.10f}")
    best_forward = best_central = (0, math.inf)
    for k in SMOOTH_EXPONENTS:
        h = 10.0**-k
        ef = abs(forward(smooth, X0, h) - target)
        ec = abs(central(smooth, X0, h) - target)
        print(f"k = {k:>2}: h = {h:.0e} forward error {ef:.3e} central error {ec:.3e}")
        if ef < best_forward[1]:
            best_forward = (k, ef)
        if ec < best_central[1]:
            best_central = (k, ec)
    print(f"smallest forward error at h = 10^-{best_forward[0]}: {best_forward[1]:.3e}")
    print(f"smallest central error at h = 10^-{best_central[0]}: {best_central[1]:.3e}")


main()
