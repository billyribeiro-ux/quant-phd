"""M5 L09 lab 1: value-function iteration on a finite grid, stopped by an a posteriori bound.

Generated model parameters, not data. The state k is capital on the grid GRID = (0.25, 0.5, 0.75, 1.0). Output is
k ** ALPHA with ALPHA = 0.5. The planner chooses next-period capital k' in GRID with k' <= k ** ALPHA, so the
consumption c = k ** ALPHA - k' is nonnegative, and the utility is u(c) = sqrt(c). The discount factor is
BETA = 0.9. The discounted Bellman operator is

    (B V)(k) = max over k' in F(k) of [ sqrt(k ** ALPHA - k') + BETA * V(k') ],
    where F(k) = {k' in GRID : k' <= k ** ALPHA} is the feasible set from k.

Each F(k) contains 0.25, because 0.25 <= k ** ALPHA for every k in GRID, so each maximum is over a nonempty finite set.
This is the operator of Lesson 8 of this unit, with the same grid and parameters as its Lab 1.

The iteration starts from V_0 = 0 and sets V_{n+1} = B V_n. For n >= 1 the certified error is
cert_n = BETA/(1 - BETA) * max_k |V_n(k) - V_{n-1}(k)|. For each certified stop the lab prints whether
max_k |V_n(k) - V*(k)| <= cert_n (field bound_holds), where V* is the fixed point of B on GRID. The reference V* is
the iterate at which cert_n <= 1e-12, so it is within 1e-12 of V*. The bound_holds field compares the actual error
with cert_n + 1e-12 to allow for that reference error.

Floats are used throughout, so a printed value is correct only as far as double-precision arithmetic allows.
No random draws. Standard library only.
"""

from __future__ import annotations

import math
from collections.abc import Callable

ALPHA = 0.5
BETA = 0.9
GRID = (0.25, 0.5, 0.75, 1.0)
TOLERANCES = (1e-2, 1e-4, 1e-6)
NAIVE_TOL = 1e-6
FIXED_COUNT = 10
REFERENCE_TOL = 1e-12
SLACK = 1e-12


def feasible(k: float) -> list[int]:
    """Indices j of the grid points k' with k' <= k ** ALPHA, the feasible next states from k."""
    output = k**ALPHA
    return [j for j, kp in enumerate(GRID) if kp <= output]


def bellman(values: list[float]) -> list[float]:
    """Apply the discounted Bellman operator to a value vector indexed like GRID."""
    out: list[float] = []
    for k in GRID:
        output = k**ALPHA
        best = max(math.sqrt(output - GRID[j]) + BETA * values[j] for j in feasible(k))
        out.append(best)
    return out


def sup_distance(a: list[float], b: list[float]) -> float:
    """The sup norm of the difference of two vectors on GRID."""
    return max(abs(x - y) for x, y in zip(a, b, strict=True))


def certified(prev: list[float], cur: list[float]) -> float:
    """The a posteriori bound beta/(1 - beta) times the last step, from V_{n-1} and V_n."""
    return BETA / (1 - BETA) * sup_distance(prev, cur)


def iterate_until(stop: Callable[[list[float], list[float]], bool]) -> tuple[int, list[float], list[float]]:
    """Iterate V_{n+1} = B V_n from V_0 = 0. Return (n, V_n, V_{n-1}) at the first n >= 1 where stop holds."""
    prev = [0.0] * len(GRID)
    cur = bellman(prev)
    n = 1
    while not stop(prev, cur):
        prev, cur = cur, bellman(cur)
        n += 1
    return n, cur, prev


def iterate_count(count: int) -> tuple[list[float], list[float]]:
    """Return (V_count, V_{count-1}) from V_0 = 0 after a fixed number of steps, for count >= 1."""
    prev = [0.0] * len(GRID)
    cur = bellman(prev)
    for _ in range(count - 1):
        prev, cur = cur, bellman(cur)
    return cur, prev


def certified_stop(tol: float) -> Callable[[list[float], list[float]], bool]:
    """The stopping rule: stop when the certified error is at most tol."""

    def stop(prev: list[float], cur: list[float]) -> bool:
        return certified(prev, cur) <= tol

    return stop


def main() -> None:
    """Print the reference solve, the policy, the certified stops, a fixed count, and the naive step rule."""
    ref_n, v_ref, ref_prev = iterate_until(lambda p, c: certified(p, c) <= REFERENCE_TOL)
    print(f"factor beta/(1-beta) {BETA / (1 - BETA):.6f}")
    print(f"reference_iterations {ref_n} reference_certified {certified(ref_prev, v_ref):.3e}")
    print("reference_values " + " ".join(f"k{k}:{v:.10f}" for k, v in zip(GRID, v_ref, strict=True)))
    policy: list[float] = []
    for k in GRID:
        options = [(math.sqrt(k**ALPHA - GRID[j]) + BETA * v_ref[j], GRID[j]) for j in feasible(k)]
        policy.append(max(options, key=lambda pair: (pair[0], -pair[1]))[1])
    print("reference_policy_saved " + " ".join(f"k{k}:{kp}" for k, kp in zip(GRID, policy, strict=True)))
    for tol in TOLERANCES:
        n, v, prev = iterate_until(certified_stop(tol))
        cert = certified(prev, v)
        err = sup_distance(v, v_ref)
        steps = [c - p for c, p in zip(v, prev, strict=True)]
        spread = max(steps) - min(steps)
        print(
            f"certified_stop tol {tol:g} n {n} cert {cert:.10f} actual_error {err:.10f} "
            f"bound_holds {err <= cert + SLACK} cert_within_tol {cert <= tol} step_spread {spread:.3e}"
        )
    v10, prev10 = iterate_count(FIXED_COUNT)
    cert10 = certified(prev10, v10)
    err10 = sup_distance(v10, v_ref)
    print(
        f"fixed_count_stop n {FIXED_COUNT} cert {cert10:.10f} actual_error {err10:.10f} "
        f"bound_holds {err10 <= cert10 + SLACK}"
    )
    n, v, prev = iterate_until(lambda p, c: sup_distance(p, c) <= NAIVE_TOL)
    step = sup_distance(prev, v)
    err = sup_distance(v, v_ref)
    print(
        f"naive_step_stop tol {NAIVE_TOL:g} n {n} step {step:.10f} actual_error {err:.10f} "
        f"error_exceeds_step {err > step} naive_factor_times_step {BETA / (1 - BETA) * step:.10f}"
    )


main()
