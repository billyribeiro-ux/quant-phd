"""E4 L05 lab 1: the coefficient fixed point of a linear rational-expectations model, solved exactly and iterated.

Inputs are illustrative numbers, not data. The equilibrium price is affine in a public signal z, p = c0 + c1 z + noise,
and the traders' forecast of the price given z is the affine function m(z) = c0 + c1 z. The coefficient map sends a
forecast (c0, c1) to the forecast the market produces:

    c0' = (alpha - gamma * c0) / beta,    c1' = -(gamma * c1 + delta) / beta.

A rational-expectations equilibrium in this family is a fixed point of the map. The fixed point is
c0* = alpha / (beta + gamma) and c1* = -delta / (beta + gamma), which is unique in the family because beta + gamma > 0.
The error e_k = c_k - c* obeys e_{k+1} = -(gamma / beta) * e_k exactly, so iteration converges from any start when
gamma < beta and fails to converge when gamma >= beta and the start is off the fixed point.

Parameters are checked as beta > 0 and gamma >= 0; otherwise the lab raises ValueError.

Part A: the closed-form fixed point, and the residual of the map at it, which is exactly zero.
Part B: iteration from (0, 0) at the base parameters; the ratio of successive errors is -gamma / beta at every step.
Part C: the same ratio when gamma equals beta: the iteration does not converge.
Part D: the same ratio when gamma exceeds beta: the error grows.
Part E: a damped step with weight beta / (beta + gamma) reaches the fixed point in one step.
Part F: the fixed-point identity m(z) = (alpha - gamma m(z) - delta z) / beta on a five-point grid of z, exact.

All values are exact Fractions, and no random draws are used, so every run prints the same lines.
"""

from __future__ import annotations

from fractions import Fraction

Coeffs = tuple[Fraction, Fraction]
Params = tuple[Fraction, Fraction, Fraction, Fraction]

BASE: Params = (Fraction(10), Fraction(2), Fraction(1, 2), Fraction(3, 4))
EQUAL: Params = (Fraction(10), Fraction(2), Fraction(2), Fraction(3, 4))
LARGE: Params = (Fraction(10), Fraction(2), Fraction(3), Fraction(3, 4))
Z_GRID: tuple[Fraction, ...] = tuple(Fraction(z) for z in (-2, -1, 0, 1, 2))


def check_params(params: Params) -> None:
    """Raise ValueError unless beta is positive and gamma is nonnegative."""
    _, beta, gamma, _ = params
    if beta <= 0:
        raise ValueError("demand slope beta must be positive")
    if gamma < 0:
        raise ValueError("supply response gamma must be nonnegative")


def coefficient_map(c: Coeffs, params: Params) -> Coeffs:
    """One step of the map from a forecast (c0, c1) to the forecast the market produces, exact in Fractions."""
    alpha, beta, gamma, delta = params
    c0, c1 = c
    return ((alpha - gamma * c0) / beta, -(gamma * c1 + delta) / beta)


def fixed_point(params: Params) -> Coeffs:
    """The closed-form fixed point (alpha / (beta + gamma), -delta / (beta + gamma))."""
    alpha, beta, gamma, delta = params
    return (alpha / (beta + gamma), -delta / (beta + gamma))


def iterate(start: Coeffs, params: Params, steps: int) -> list[Coeffs]:
    """The path of the map from the start: the start, then steps further iterates."""
    path = [start]
    for _ in range(steps):
        path.append(coefficient_map(path[-1], params))
    return path


def error_ratios(path: list[Coeffs], target: Coeffs, index: int) -> list[str]:
    """The ratio of successive errors in coefficient index (0 for c0, 1 for c1), printed exactly.

    A zero error is reported as such, because the ratio is then undefined.
    """
    errors = [c[index] - target[index] for c in path]
    out: list[str] = []
    for k in range(len(errors) - 1):
        if errors[k] == 0:
            out.append("zero-error")
        else:
            out.append(str(errors[k + 1] / errors[k]))
    return out


def show(label: str, params: Params, steps: int) -> None:
    """Print the fixed point, the iterates from (0, 0) and the exact ratio of successive errors in each coefficient."""
    check_params(params)
    target = fixed_point(params)
    path = iterate((Fraction(0), Fraction(0)), params, steps)
    print(f"{label} fixed_point c0 {target[0]} c1 {target[1]}")
    print(f"{label} c0_path {[str(c[0]) for c in path]}")
    print(f"{label} c1_path {[str(c[1]) for c in path]}")
    print(f"{label} c0_error_ratios {error_ratios(path, target, 0)}")
    print(f"{label} c1_error_ratios {error_ratios(path, target, 1)}")


def main() -> None:
    """Print Parts A to F. Every value is an exact Fraction, so the output is reproducible."""
    alpha, beta, gamma, delta = BASE
    print("Part A: closed-form fixed point and residual of the map")
    target = fixed_point(BASE)
    residual = coefficient_map(target, BASE)
    print(f"base alpha {alpha} beta {beta} gamma {gamma} delta {delta}")
    print(f"fixed_point c0 {target[0]} c1 {target[1]}")
    print(f"residual_c0 {residual[0] - target[0]} residual_c1 {residual[1] - target[1]}")

    print("Part B: iteration at the base parameters from (0, 0)")
    show("base", BASE, 8)

    print("Part C: gamma equal to beta, the iteration does not converge")
    show("equal", EQUAL, 6)

    print("Part D: gamma above beta, the error grows")
    show("large", LARGE, 6)

    print("Part E: damped step with weight beta / (beta + gamma) at the base parameters")
    weight = beta / (beta + gamma)
    start = (Fraction(0), Fraction(0))
    image = coefficient_map(start, BASE)
    damped = ((1 - weight) * start[0] + weight * image[0], (1 - weight) * start[1] + weight * image[1])
    print(f"weight {weight} damped_step c0 {damped[0]} c1 {damped[1]} equals_fixed_point {damped == target}")

    print("Part F: fixed-point identity on the five-point grid of z, exact")
    c0, c1 = target
    checks: list[bool] = []
    for z in Z_GRID:
        m_z = c0 + c1 * z
        checks.append(m_z == (alpha - gamma * m_z - delta * z) / beta)
    print(f"z_grid {[str(z) for z in Z_GRID]} identity_holds {checks}")


main()
