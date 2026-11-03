"""M7 L05 lab 1: a quadratic program solved from its KKT system in exact arithmetic, and checked by enumeration.

SIMULATED: the inputs are small integers chosen by hand as illustrative values, not data.
No random draws are used, so every run prints the same lines.
Every number is a fractions.Fraction, so each residual is exactly zero or exactly a stated value.

Part A: equality-constrained QP, minimise f(x) = (1/2) x'Qx + c'x subject to Ax = b, with Q symmetric positive
definite (3 by 3) and A of full row rank (2 by 3). The KKT system [[Q, A'], [A, 0]] [x; lambda] = [-c; b] is solved
by Gaussian elimination. The printed checks are the exact residual of both block rows, and the increase of f along
the null direction v of A, which must equal (1/2) t^2 v'Qv for every t on a grid.

Part B: inequality QP, minimise (1/2) x'Qx + c'x subject to x >= 0 in two variables. The four active sets S (the
components fixed at zero) are enumerated. For each S the free components solve Q_FF x_F = -c_F, the multipliers on
S are mu_i = (Qx + c)_i, and the candidate is kept only if x >= 0 and mu_i >= 0 on S. The printed brute-force check
evaluates f on the grid {k/16 : 0 <= k <= 32}^2 and counts grid points below the candidate's value.

CU is the currency unit. This lab has no money amounts.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

Q_A: list[list[Fraction]] = [
    [Fraction(4), Fraction(1), Fraction(0)],
    [Fraction(1), Fraction(3), Fraction(1)],
    [Fraction(0), Fraction(1), Fraction(2)],
]
C_A: list[Fraction] = [Fraction(-1), Fraction(0), Fraction(2)]
EQ_A: list[list[Fraction]] = [
    [Fraction(1), Fraction(1), Fraction(1)],
    [Fraction(0), Fraction(1), Fraction(-1)],
]
B_A: list[Fraction] = [Fraction(1), Fraction(0)]
NULL_A: list[Fraction] = [Fraction(-2), Fraction(1), Fraction(1)]

Q_B: list[list[Fraction]] = [[Fraction(2), Fraction(1)], [Fraction(1), Fraction(2)]]
C_B: list[Fraction] = [Fraction(-3), Fraction(1)]
GRID_STEPS = 16
GRID_MAX = 2


def solve(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    """Solve matrix x = rhs exactly by Gaussian elimination with row pivoting; raise ValueError if singular."""
    n = len(rhs)
    rows = [[*row, rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if rows[r][col] != 0), None)
        if pivot is None:
            raise ValueError("the matrix is singular")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(n):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[col], strict=True)]
    return [rows[i][n] / rows[i][i] for i in range(n)]


def quad(q: list[list[Fraction]], c: list[Fraction], x: list[Fraction]) -> Fraction:
    """f(x) = (1/2) x'Qx + c'x, exact."""
    qx = [sum((q[i][j] * x[j] for j in range(len(x))), Fraction(0)) for i in range(len(x))]
    return Fraction(1, 2) * sum((x[i] * qx[i] for i in range(len(x))), Fraction(0)) + sum(
        (c[i] * x[i] for i in range(len(x))), Fraction(0)
    )


def gradient(q: list[list[Fraction]], c: list[Fraction], x: list[Fraction]) -> list[Fraction]:
    """The gradient Qx + c of f, exact."""
    return [sum((q[i][j] * x[j] for j in range(len(x))), Fraction(0)) + c[i] for i in range(len(x))]


def leading_minors_positive(q: list[list[Fraction]]) -> bool:
    """Leading principal minors test: every leading principal minor is positive.

    An exact test for this Q. Remark 2.4 proves positive definiteness by completing the square.
    """
    for k in range(1, len(q) + 1):
        sub = [row[:k] for row in q[:k]]
        if det(sub) <= 0:
            return False
    return True


def det(m: list[list[Fraction]]) -> Fraction:
    """Determinant by cofactor expansion; the matrices here are at most 3 by 3."""
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    total = Fraction(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1 :] for row in m[1:]]
        total += (-1) ** j * m[0][j] * det(minor)
    return total


def part_a() -> None:
    """Solve the equality-constrained QP from its KKT system and check it."""
    n, m = len(C_A), len(B_A)
    print(f"part_a_dimensions variables {n} constraints {m} kkt_size {n + m}")
    print(f"q_positive_definite {leading_minors_positive(Q_A)}")
    kkt = [Q_A[i] + [EQ_A[k][i] for k in range(m)] for i in range(n)]
    kkt += [EQ_A[k] + [Fraction(0)] * m for k in range(m)]
    print(f"kkt_determinant {det(kkt)}")
    rhs = [-c for c in C_A] + B_A
    sol = solve(kkt, rhs)
    x, lam = sol[:n], sol[n:]
    print("x " + " ".join(str(v) for v in x))
    print("lambda " + " ".join(str(v) for v in lam))

    grad = gradient(Q_A, C_A, x)
    stationarity = [grad[i] + sum((EQ_A[k][i] * lam[k] for k in range(m)), Fraction(0)) for i in range(n)]
    primal = [sum((EQ_A[k][i] * x[i] for i in range(n)), Fraction(0)) - B_A[k] for k in range(m)]
    print(f"max_abs_stationarity_residual {float(max(abs(v) for v in stationarity)):.1e}")
    print(f"max_abs_constraint_residual {float(max(abs(v) for v in primal)):.1e}")
    print(f"objective {float(quad(Q_A, C_A, x)):.10f}")

    base = quad(Q_A, C_A, x)
    null_ok = True
    worst = Fraction(0)
    for k in range(-8, 9):
        t = Fraction(k, 4)
        point = [x[i] + t * NULL_A[i] for i in range(n)]
        feasible = all(sum((EQ_A[r][i] * point[i] for i in range(n)), Fraction(0)) == B_A[r] for r in range(m))
        predicted = Fraction(1, 2) * t * t * quad_form(Q_A, NULL_A)
        gap = quad(Q_A, C_A, point) - base - predicted
        worst = max(worst, abs(gap))
        null_ok = null_ok and feasible and gap == 0
    print(f"null_line_increase_is_half_t_squared_form {null_ok}")
    print(f"null_line_worst_gap {float(worst):.1e}")


def quad_form(q: list[list[Fraction]], v: list[Fraction]) -> Fraction:
    """The quadratic form v'Qv, exact."""
    return sum((v[i] * q[i][j] * v[j] for i in range(len(v)) for j in range(len(v))), Fraction(0))


def part_b() -> None:
    """Enumerate the four active sets for x >= 0, keep the candidates that pass, and check on a grid."""
    n = len(C_B)
    candidates: list[tuple[tuple[int, ...], list[Fraction]]] = []
    print("part_b_candidates active_set primal_ok dual_ok")
    for mask in product((0, 1), repeat=n):
        fixed = tuple(i for i in range(n) if mask[i])
        free = [i for i in range(n) if not mask[i]]
        x = [Fraction(0)] * n
        if free:
            sub_q = [[Q_B[i][j] for j in free] for i in free]
            sub_c = [-C_B[i] for i in free]
            for pos, value in zip(free, solve(sub_q, sub_c), strict=True):
                x[pos] = value
        grad = gradient(Q_B, C_B, x)
        primal_ok = all(v >= 0 for v in x)
        dual_ok = all(grad[i] >= 0 for i in fixed)
        label = "{" + ",".join(str(i + 1) for i in fixed) + "}"
        print(f"candidate {label} primal {primal_ok} dual {dual_ok}")
        if primal_ok and dual_ok:
            candidates.append((fixed, x))
    print(f"passing_candidates {len(candidates)}")
    fixed, x_hat = candidates[0]
    value = quad(Q_B, C_B, x_hat)
    print("x_hat " + " ".join(str(v) for v in x_hat))
    print(f"objective_hat {value}")
    print("mu_hat " + " ".join(str(v) for v in gradient(Q_B, C_B, x_hat)))
    grid = [Fraction(k, GRID_STEPS) for k in range(GRID_STEPS * GRID_MAX + 1)]
    below = 0
    least = None
    for a in grid:
        for b in grid:
            fv = quad(Q_B, C_B, [a, b])
            below += fv < value
            least = fv if least is None or fv < least else least
    print(f"grid_points {len(grid) ** 2}")
    print(f"grid_points_below_candidate {below}")
    print(f"grid_minimum_equals_candidate {least == value}")


def main() -> None:
    """Run Part A and Part B and print their checks."""
    print("lab M7 L05 1, no random draws")
    part_a()
    part_b()


main()
