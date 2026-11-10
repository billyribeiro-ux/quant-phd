"""Lab S3-L07-1: Vector Autoregression estimation and companion eigenvalues.

SIMULATED: generates a bivariate VAR(1) process, estimates coefficient matrices
by equation-by-equation OLS, and computes companion eigenvalues for stability check.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    # True VAR(1) parameters: Y_t = A * Y_{t-1} + U_t
    a11, a12 = 0.50, 0.20
    a21, a22 = 0.10, 0.60

    # Companion eigenvalues analytically:
    # lambda^2 - (a11+a22)*lambda + (a11*a22 - a12*a21) = 0
    # lambda^2 - 1.1*lambda + 0.28 = 0 -> (lambda - 0.7)*(lambda - 0.4) = 0
    true_eig1 = 0.70
    true_eig2 = 0.40

    rng = random.Random(42)
    n = 1500
    y1 = [0.0]
    y2 = [0.0]

    for _ in range(n - 1):
        u1 = rng.gauss(0.0, 1.0)
        u2 = rng.gauss(0.0, 1.0)
        next_y1 = a11 * y1[-1] + a12 * y2[-1] + u1
        next_y2 = a21 * y1[-1] + a22 * y2[-1] + u2
        y1.append(next_y1)
        y2.append(next_y2)

    # OLS estimation equation-by-equation
    y1_dep = y1[1:]
    y2_dep = y2[1:]
    x1 = y1[:-1]
    x2 = y2[:-1]
    m = len(y1_dep)

    s11 = sum(x1[i] * x1[i] for i in range(m))
    s12 = sum(x1[i] * x2[i] for i in range(m))
    s22 = sum(x2[i] * x2[i] for i in range(m))
    det = s11 * s22 - s12 * s12

    inv11 = s22 / det
    inv12 = -s12 / det
    inv22 = s11 / det

    # Equation 1: y1_t on y1_{t-1}, y2_{t-1}
    sy1_1 = sum(x1[i] * y1_dep[i] for i in range(m))
    sy2_1 = sum(x2[i] * y1_dep[i] for i in range(m))
    hat_a11 = inv11 * sy1_1 + inv12 * sy2_1
    hat_a12 = inv12 * sy1_1 + inv22 * sy2_1

    # Equation 2: y2_t on y1_{t-1}, y2_{t-1}
    sy1_2 = sum(x1[i] * y2_dep[i] for i in range(m))
    sy2_2 = sum(x2[i] * y2_dep[i] for i in range(m))
    hat_a21 = inv11 * sy1_2 + inv12 * sy2_2
    hat_a22 = inv12 * sy1_2 + inv22 * sy2_2

    # Estimated companion eigenvalues
    tr = hat_a11 + hat_a22
    det_hat = hat_a11 * hat_a22 - hat_a12 * hat_a21
    disc = tr * tr - 4.0 * det_hat
    hat_eig1 = (tr + math.sqrt(disc)) / 2.0
    hat_eig2 = (tr - math.sqrt(disc)) / 2.0

    print("Bivariate VAR(1) Estimation (T=1500, seed=42):")
    print(f"True Matrix A:       [[{a11:.2f}, {a12:.2f}], [{a21:.2f}, {a22:.2f}]]")
    print(f"Estimated Matrix A:  [[{hat_a11:.4f}, {hat_a12:.4f}], [{hat_a21:.4f}, {hat_a22:.4f}]]")
    print("\nCompanion Eigenvalue Analysis:")
    print(f"  True Eigenvalues:      [{true_eig1:.4f}, {true_eig2:.4f}]")
    print(f"  Estimated Eigenvalues: [{hat_eig1:.4f}, {hat_eig2:.4f}]")
    is_stable = abs(hat_eig1) < 1.0 and abs(hat_eig2) < 1.0
    print(f"  VAR Stability Check (max |lambda| < 1): {is_stable}")


main()
