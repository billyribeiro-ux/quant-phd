"""Lab E6-L02-1: Log-linearization and Taylor approximation error.

Compares the exact nonlinear aggregate resource constraint and the exact nonlinear Euler equation
with their first-order log-linearizations across geometric refinements of deviation size.
Verifies that the approximation error decays quadratically (ratio ~4 when step size halves),
confirming Taylor's remainder theorem.
"""

from __future__ import annotations

import math


def evaluate_resource_error(c_hat: float, s_c: float, s_i: float) -> tuple[float, float, float]:
    """Compute the exact vs log-linearized output gap for a given consumption perturbation."""
    # Choose i_hat such that linear output gap is zero to isolate residual
    i_hat = -c_hat * (s_c / s_i)
    linear_y_hat = s_c * c_hat + s_i * i_hat  # exactly 0.0

    # Exact nonlinear expenditure ratio: Y / Y* = s_c * exp(c_hat) + s_i * exp(i_hat)
    expenditure_ratio = s_c * math.exp(c_hat) + s_i * math.exp(i_hat)
    exact_y_hat = math.log(expenditure_ratio)

    error = abs(exact_y_hat - linear_y_hat)
    return linear_y_hat, exact_y_hat, error


def evaluate_euler_log_error(r_deviation: float) -> tuple[float, float, float]:
    """Compute the error in the log-linear real return approximation ln(1 + r) ~= r."""
    linear_r = r_deviation
    exact_log_r = math.log(1.0 + r_deviation)
    error = abs(exact_log_r - linear_r)
    return linear_r, exact_log_r, error


def main() -> None:
    s_c = 0.75
    s_i = 0.25
    steps = [0.10, 0.05, 0.025, 0.0125]

    print("Part 1: Log-linear aggregate resource constraint (s_c=0.75, s_i=0.25):")
    res_errors: list[float] = []
    for eps in steps:
        _, exact_val, err = evaluate_resource_error(eps, s_c, s_i)
        res_errors.append(err)
        print(f"  c_hat = {eps:7.4f}: exact y_hat = {exact_val:10.6e}, error = {err:10.6e}")

    print("\nError reduction ratios for resource constraint (target 4.00):")
    for i in range(len(res_errors) - 1):
        ratio = res_errors[i] / res_errors[i + 1]
        print(f"  ratio {steps[i]:.4f} -> {steps[i + 1]:.4f}: {ratio:.2f}")

    print("\nPart 2: Return log-approximation ln(1 + r) ~= r:")
    return_errors: list[float] = []
    for eps in steps:
        _, exact_val, err = evaluate_euler_log_error(eps)
        return_errors.append(err)
        print(f"  r = {eps:7.4f}: exact ln(1+r) = {exact_val:10.6e}, error = {err:10.6e}")

    print("\nError reduction ratios for return log-approximation (target 4.00):")
    for i in range(len(return_errors) - 1):
        ratio = return_errors[i] / return_errors[i + 1]
        print(f"  ratio {steps[i]:.4f} -> {steps[i + 1]:.4f}: {ratio:.2f}")


main()
