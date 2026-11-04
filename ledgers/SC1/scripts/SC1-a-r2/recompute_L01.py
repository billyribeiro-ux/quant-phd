"""Round-2 independent recomputation of the L01 lab numbers and the L01 prose numbers (exact Fractions).

Run: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r2/recompute_L01.py
Written without reading the lab code: the variance sums come from a closed form, and the covariance
is built from an explicit increment-sharing matrix.
"""

from __future__ import annotations

from fractions import Fraction as F


def dyadic_increment_variances(t: F, depth: int) -> list[F]:
    pieces = 2**depth
    return [t / pieces] * pieces


def covariance_matrix(variances: list[F], grid_size: int) -> list[list[F]]:
    # B at grid index i is the sum of the first i increments; increments are independent, so
    # Cov(B_i, B_j) = sum over shared increments = sum of the first min(i, j) variances.
    cov = [[F(0)] * (grid_size + 1) for _ in range(grid_size + 1)]
    for i in range(grid_size + 1):
        for j in range(grid_size + 1):
            shared = min(i, j)
            cov[i][j] = sum((variances[k] for k in range(shared)), F(0))
    return cov


def main() -> None:
    times = [F(1), F(3, 4), F(5, 2)]
    equal = 0
    total_cases = 0
    for t in times:
        for depth in range(5):
            total_cases += 1
            s = sum(dyadic_increment_variances(t, depth), F(0))
            equal += s == t
    print(f"recomputed: dyadic variance sums equal t: {equal} of {total_cases}")

    grid_size = 8
    variances = dyadic_increment_variances(F(1), 3)  # eight increments of length 1/8
    assert len(variances) == grid_size and all(v == F(1, 8) for v in variances)
    cov = covariance_matrix(variances, grid_size)
    times_grid = [F(i, grid_size) for i in range(grid_size + 1)]
    agree = sum(
        1 for i in range(grid_size + 1) for j in range(grid_size + 1) if cov[i][j] == min(times_grid[i], times_grid[j])
    )
    print(f"recomputed: covariance equals min on grid: {agree} of {(grid_size + 1) ** 2}")
    print(f"recomputed: Cov(B_(1/4), B_(5/8)) = {cov[2][5]}; min = {min(times_grid[2], times_grid[5])}")

    # Prose numbers: E1 (t = 3/4, 16 pieces), E2 and the example at h = 1/4 and 1/100.
    piece = F(3, 4) / 16
    print(f"recomputed: E1 piece length {piece}, 16 pieces sum to {16 * piece}")
    print("recomputed: sd(h=1/4) = 1/2 exact since sqrt(1/4) = 1/2:", F(1, 2) * F(1, 2) == F(1, 4))
    print("recomputed: 1/sqrt(1/100) = 10:", 10 * 10 == 100)
    print("recomputed: ratio sqrt(h)/h at h=1/100 is 10 (sd 1/10 over h 1/100):", F(1, 10) / F(1, 100))
    print("recomputed: Var(3B_1 - B_2) = 9*1 + 2 - 6*min(1,2) =", 9 * 1 + 2 - 6 * min(1, 2))
    print("recomputed: M1 Cov(B_1/3, B_2/3) = min =", min(F(1, 3), F(2, 3)), "; Var increment =", F(2, 3) - F(1, 3))


if __name__ == "__main__":
    main()
