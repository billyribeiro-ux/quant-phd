"""M3 L02 lab 1: the matrix of a linear map in a new basis, and the change-of-basis identity.

For 50 seeded pairs (A, C) of 3 by 3 integer matrices and a seeded invertible 3 by 3 integer matrix S
whose columns form a basis of R^3, the lab checks:
  (a) the matrix of x -> A x in the basis of the columns of S, built column by column from coordinates
      (the coordinates y_j solve S y_j = A s_j, by elimination), equals S^-1 A S exactly (Theorem 4.1
      of Lesson 2);
  (b) the matrix of the composition x -> C (A x) in that basis equals the product of the matrix of
      x -> C x and the matrix of x -> A x, both taken in that basis (Proposition 3.1 of Lesson 2);
  (c) a floating-point evaluation of S^-1 A S agrees with the exact matrix to within 1e-12, measured
      relative to max(1, |entry|) for each entry.
Checks (a) and (b) use fractions.Fraction, so they involve no rounding. Check (c) uses floats only.
Candidate matrices S that are singular are rejected and redrawn; the count of rejections is printed.
Draws come from a linear congruential generator with fixed constants, so the output is the same on
every run. The lab checks the listed pairs only. Standard library only.
"""

from __future__ import annotations

from fractions import Fraction

LCG_MULTIPLIER = 1103515245
LCG_INCREMENT = 12345
LCG_MODULUS = 2**31
SEED = 7
PAIRS = 50
SIZE = 3
MATRIX_BOUND = 4
BASIS_BOUND = 3
FLOAT_TOLERANCE = 1e-12


class Lcg:
    """A linear congruential generator with fixed constants, so every run draws the same integers."""

    def __init__(self, seed: int) -> None:
        self.state = seed % LCG_MODULUS

    def entry(self, bound: int) -> int:
        """Return an integer from -bound to bound, inclusive. Each call advances the state once."""
        self.state = (LCG_MULTIPLIER * self.state + LCG_INCREMENT) % LCG_MODULUS
        return (self.state >> 16) % (2 * bound + 1) - bound


Matrix = list[list[Fraction]]


def draw_matrix(gen: Lcg, bound: int) -> Matrix:
    """A SIZE by SIZE matrix of exact fractions with integer entries from -bound to bound."""
    return [[Fraction(gen.entry(bound)) for _ in range(SIZE)] for _ in range(SIZE)]


def mul(a: Matrix, b: Matrix) -> Matrix:
    """The matrix product a b of exact fraction matrices."""
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0)) for j in range(len(b[0]))] for i in range(len(a))
    ]


def solve(m: Matrix, rhs: list[Fraction]) -> list[Fraction]:
    """The solution y of m y = rhs, by Gauss-Jordan elimination with partial pivoting on the largest entry.

    Raises ValueError when m has no pivot in some column, which means m is singular.
    """
    n = len(m)
    aug = [[*m[i], rhs[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(aug[i][c]))
        if aug[p][c] == 0:
            raise ValueError("singular matrix")
        aug[c], aug[p] = aug[p], aug[c]
        for i in range(n):
            if i != c:
                f = aug[i][c] / aug[c][c]
                aug[i] = [x - f * y for x, y in zip(aug[i], aug[c], strict=True)]
    return [aug[i][n] / aug[i][i] for i in range(n)]


def inverse(m: Matrix) -> Matrix:
    """The inverse of m, solving m x_j = e_j for each standard unit vector e_j."""
    n = len(m)
    columns = [solve(m, [Fraction(int(i == j)) for i in range(n)]) for j in range(n)]
    return [[columns[j][i] for j in range(n)] for i in range(n)]


def solve_float(m: list[list[float]], rhs: list[float]) -> list[float]:
    """The floating-point counterpart of solve, with the same pivoting rule (used only in the float check)."""
    n = len(m)
    aug = [[*m[i], rhs[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(aug[i][c]))
        if aug[p][c] == 0.0:
            raise ValueError("singular matrix")
        aug[c], aug[p] = aug[p], aug[c]
        for i in range(n):
            if i != c:
                f = aug[i][c] / aug[c][c]
                aug[i] = [x - f * y for x, y in zip(aug[i], aug[c], strict=True)]
    return [aug[i][n] / aug[i][i] for i in range(n)]


def inverse_float(m: list[list[float]]) -> list[list[float]]:
    """The floating-point inverse of m, solving m x_j = e_j for each unit vector."""
    n = len(m)
    columns = [solve_float(m, [float(i == j) for i in range(n)]) for j in range(n)]
    return [[columns[j][i] for j in range(n)] for i in range(n)]


def mul_float(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """The matrix product a b of float matrices."""
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def main() -> None:
    gen = Lcg(SEED)
    rejected = 0
    coordinates_ok = 0
    composition_ok = 0
    float_ok = 0
    first_basis_matrix: Matrix = []
    for pair in range(PAIRS):
        a = draw_matrix(gen, MATRIX_BOUND)
        c = draw_matrix(gen, MATRIX_BOUND)
        while True:
            s = draw_matrix(gen, BASIS_BOUND)
            try:
                s_inv = inverse(s)
                break
            except ValueError:
                rejected += 1

        formula = mul(mul(s_inv, a), s)
        coordinates = [
            solve(s, [sum((a[i][k] * s[k][j] for k in range(SIZE)), Fraction(0)) for i in range(SIZE)])
            for j in range(SIZE)
        ]
        built = [list(row) for row in zip(*coordinates, strict=True)]
        coordinates_ok += built == formula

        in_basis_a = formula
        in_basis_c = mul(mul(s_inv, c), s)
        composed = mul(mul(s_inv, c), mul(a, s))
        composition_ok += composed == mul(in_basis_c, in_basis_a)

        float_s = [[float(x) for x in row] for row in s]
        float_a = [[float(x) for x in row] for row in a]
        float_formula = mul_float(mul_float(inverse_float(float_s), float_a), float_s)
        within = all(
            abs(float_formula[i][j] - float(formula[i][j])) <= FLOAT_TOLERANCE * max(1.0, abs(float(formula[i][j])))
            for i in range(SIZE)
            for j in range(SIZE)
        )
        float_ok += within
        if pair == 0:
            first_basis_matrix = formula
    print(f"pairs (A, C) and invertible S tested: {PAIRS}")
    print(f"singular draws of S rejected before an invertible S was found: {rejected}")
    print(f"coordinates of A s_j equal S^-1 A S in {coordinates_ok} of {PAIRS} pairs")
    print(f"composition matrix equals the product of matrices in {composition_ok} of {PAIRS} pairs")
    print(f"float evaluation of S^-1 A S within 1e-12 of the exact matrix in {float_ok} of {PAIRS} pairs")
    print("first pair, matrix of A in the basis of S, row by row:")
    for row in first_basis_matrix:
        print(" ".join(str(x) for x in row))


main()
