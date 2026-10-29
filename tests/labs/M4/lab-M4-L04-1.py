"""M4 L04 lab 1: independence and conditional expectation on finite joint tables.

Inputs are exact rational tables written in this file, not data. Every probability is a Fraction, so every
comparison is exact. Decimals are printed only at 6 places, for reading.

Part A: two joint tables on X in {0, 1, 2} and Y in {0, 1}. The first is a product table, so it is independent by
construction. The second is a dependent table. For each, the test P(X=x, Y=y) = P(X=x) P(Y=y) is applied to every
cell, and the verdict is printed with the cell (0, 0).
Part B: X uniform on {-1, 0, 1} and Y = X squared. Prints E[X], E[Y], E[XY], the covariance E[XY] - E[X] E[Y], and
the cell (0, 0) against the product of its marginals.
Part C: conditional expectations E[X | Y = y] for the dependent table of Part A, the unconditional E[X], the
total-expectation sum over y of E[X | Y = y] P(Y = y), and a check that a product table gives E[X | Y = y] = E[X].
"""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction

Table = dict[tuple[int, int], Fraction]

DEPENDENT: Table = {
    (0, 0): Fraction(1, 10),
    (0, 1): Fraction(3, 10),
    (1, 0): Fraction(2, 10),
    (1, 1): Fraction(2, 10),
    (2, 0): Fraction(1, 10),
    (2, 1): Fraction(1, 10),
}
PX: dict[int, Fraction] = {0: Fraction(1, 5), 1: Fraction(2, 5), 2: Fraction(2, 5)}
PY: dict[int, Fraction] = {0: Fraction(3, 10), 1: Fraction(7, 10)}
PRODUCT: Table = {(x, y): PX[x] * PY[y] for x in PX for y in PY}


def marginals(table: Table) -> tuple[dict[int, Fraction], dict[int, Fraction]]:
    """Return the marginal pmfs of X (first coordinate) and Y (second coordinate) of a joint table."""
    px: dict[int, Fraction] = {}
    py: dict[int, Fraction] = {}
    for (x, y), p in table.items():
        px[x] = px.get(x, Fraction(0)) + p
        py[y] = py.get(y, Fraction(0)) + p
    return px, py


def is_independent(table: Table) -> bool:
    """True when every cell equals the product of the two marginals of that cell, compared exactly."""
    px, py = marginals(table)
    return all(p == px[x] * py[y] for (x, y), p in table.items())


def expectation_of(table: Table, g: Callable[[int, int], int]) -> Fraction:
    """E[g(X, Y)] for a finite joint table: the sum of g(x, y) times P(X=x, Y=y), exactly."""
    return sum((g(x, y) * p for (x, y), p in table.items()), Fraction(0))


def conditional_expectation_x(table: Table, y: int) -> Fraction:
    """E[X | Y = y] = sum over x of x P(X=x, Y=y) divided by P(Y=y). Fails loudly when P(Y=y) is zero."""
    _, py = marginals(table)
    if py.get(y, Fraction(0)) == 0:
        raise ValueError(f"P(Y = {y}) is zero, so E[X | Y = {y}] is not defined")
    numerator = sum((x * p for (x, yy), p in table.items() if yy == y), Fraction(0))
    return numerator / py[y]


def show(q: Fraction) -> str:
    """An exact fraction, then its value to 6 places in brackets."""
    return f"{q} [{float(q):.6f}]"


def main() -> None:
    """Print Parts A, B and C. The tables are fixed, so every run prints the same lines."""
    print("Part A: independence of the joint table, cell by cell")
    for name, table in (("product", PRODUCT), ("dependent", DEPENDENT)):
        px, py = marginals(table)
        print(f"table {name} independent {is_independent(table)}")
        print(f"table {name} cell_0_0 joint {show(table[(0, 0)])} product_of_marginals {show(px[0] * py[0])}")

    print("Part B: X uniform on {-1, 0, 1} and Y = X squared")
    uniform = {(x, x * x): Fraction(1, 3) for x in (-1, 0, 1)}
    px, py = marginals(uniform)
    ex = expectation_of(uniform, lambda x, y: x)
    ey = expectation_of(uniform, lambda x, y: y)
    exy = expectation_of(uniform, lambda x, y: x * y)
    print(f"E[X] {show(ex)}")
    print(f"E[Y] {show(ey)}")
    print(f"E[XY] {show(exy)}")
    print(f"covariance {show(exy - ex * ey)}")
    print(f"cell_0_0 joint {show(uniform[(0, 0)])} product_of_marginals {show(px[0] * py[0])}")
    print(f"independent {is_independent(uniform)}")

    print("Part C: conditional expectations on the dependent table")
    ex_dep = expectation_of(DEPENDENT, lambda x, y: x)
    print(f"E[X] {show(ex_dep)}")
    total = Fraction(0)
    for y in sorted(PY):
        cond = conditional_expectation_x(DEPENDENT, y)
        _, py_dep = marginals(DEPENDENT)
        total += cond * py_dep[y]
        print(f"E[X | Y = {y}] {show(cond)} P(Y = {y}) {show(py_dep[y])}")
    print(f"total_expectation_sum {show(total)} equals_E[X] {total == ex_dep}")
    product_gaps = []
    for y in sorted(PY):
        product_gaps.append(conditional_expectation_x(PRODUCT, y) == expectation_of(PRODUCT, lambda x, yy: x))
    print(f"product_table_conditional_equals_E[X] {all(product_gaps)}")


main()
