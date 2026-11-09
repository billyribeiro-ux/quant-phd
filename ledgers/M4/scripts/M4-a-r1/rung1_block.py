"""Rung 1 worked example: the 99% loss of a two-asset portfolio, Gaussian and matched Student-t, for one seeded run.

Standard library only. Every input is SIMULATED: the positions and the covariance are illustrative numbers, not market
data. Losses are whole cents, rounded once with round(). The 99% loss is the loss of 1-based rank ceil(0.99 n) in
ascending order, computed in exact integers. The Student-t draws are scaled by sqrt((NU - 2) / W), the square root of
the matched factor (NU - 2) / NU times sqrt(NU / W), where W is the chi-square draw.
"""

import math
import random

POSITIONS = [3_000_000, 2_000_000]  # cents: $30,000.00 and $20,000.00, illustrative
COV = [[0.0004, 0.0001], [0.0001, 0.0009]]  # per-period return covariance: volatilities 2% and 3%, SIMULATED
N_DRAWS = 20_000
SEED = 20261028
NU = 5  # Student-t degrees of freedom


def cholesky_2x2(cov: list[list[float]]) -> list[list[float]]:
    """The lower-triangular L with L L^T = cov, for a 2 x 2 positive definite matrix."""
    l11 = math.sqrt(cov[0][0])
    l21 = cov[1][0] / l11
    l22 = math.sqrt(cov[1][1] - l21 * l21)
    return [[l11, 0.0], [l21, l22]]


def simulate(family: str) -> list[int]:
    """One loss per draw in whole cents, for the gaussian or the student_t family, from the same seed."""
    rng = random.Random(SEED)
    chol = cholesky_2x2(COV)
    losses: list[int] = []
    for _ in range(N_DRAWS):
        # Step 1. Two independent standard normals per draw.
        z1 = rng.gauss(0.0, 1.0)
        z2 = rng.gauss(0.0, 1.0)
        scale = 1.0
        if family == "student_t":
            # Step 2. A chi-square with NU degrees of freedom is a gamma with shape NU / 2 and scale 2. The t draw
            # divides the normal by sqrt(W / NU), so its returns carry the factor sqrt(NU / W), times the square
            # root of the matched factor, sqrt((NU - 2) / NU), which equals sqrt((NU - 2) / W).
            chi_square = rng.gammavariate(NU / 2, 2.0)
            scale = math.sqrt((NU - 2) / chi_square)
        # Step 3. Correlate the normals with the factor L, then scale them to the returns.
        r1 = scale * chol[0][0] * z1
        r2 = scale * (chol[1][0] * z1 + chol[1][1] * z2)
        # Step 4. The loss is minus the position-weighted return, in cents, rounded once.
        losses.append(round(-(POSITIONS[0] * r1 + POSITIONS[1] * r2)))
    return losses


def quantile_99(losses: list[int]) -> int:
    """The ceil(0.99 n)-th smallest loss (1-based rank), computed in exact integers."""
    index = (99 * len(losses) + 99) // 100
    return sorted(losses)[index - 1]


def sample_variance(xs: list[int]) -> float:
    """The unbiased sample variance."""
    mean = sum(xs) / len(xs)
    return sum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def main() -> None:
    # Step 5. The target: the variance of the portfolio loss is w' Sigma w, in cents squared.
    target = sum(POSITIONS[i] * POSITIONS[j] * COV[i][j] for i in range(2) for j in range(2))
    print("portfolio variance w'Sigma w (cents^2):", f"{target:.1f}")
    print("matched factor (NU - 2) / NU:", f"{(NU - 2) / NU:.6f}")
    print("index of the 99% loss, ceil(0.99 n) with n =", N_DRAWS, ":", (99 * N_DRAWS + 99) // 100)
    gaussian = simulate("gaussian")
    print("gaussian 99% loss (cents):", quantile_99(gaussian))
    print("gaussian sample variance / w'Sigma w:", f"{sample_variance(gaussian) / target:.4f}")
    student = simulate("student_t")
    print("student_t 99% loss (cents):", quantile_99(student))
    print("student_t sample variance / w'Sigma w:", f"{sample_variance(student) / target:.4f}")
    print("unmatched t would inflate the variance by NU / (NU - 2):", f"{NU / (NU - 2):.4f}")


main()