"""E4 L04 lab 1: rank of a payoff matrix by exact Gaussian elimination, and the completeness test.

Inputs are illustrative numbers, not data. A payoff matrix has one row per traded security and one column per state.
Entry (j, s) is the payoff of security j in state s, in whole units of the numeraire. Two matrices are used: an
incomplete market with two securities in three states, and a complete market with four securities in three states,
one of which is a redundant combination of the other three.

The rank of a matrix is the number of pivots that exact Gaussian elimination produces. The market is complete when the
rank equals the number of states S. A payoff vector x in the states is attainable when some portfolio theta reproduces
it, that is, when x lies in the row space of the matrix. That holds exactly when the rank of the matrix with x appended
as one more row equals the rank of the matrix.

Part A: the rank of each matrix, computed in exact Fractions.
Part B: the completeness test, rank equal to the number of states, for each matrix.
Part C: attainability of three payoff vectors in the incomplete market, tested by the augmented rank.
Part D: attainability of the same three payoff vectors in the complete market.
Part E: a redundant security leaves the rank unchanged.

No random draws are used, so every run prints the same lines.
"""

from __future__ import annotations

from fractions import Fraction

Row = list[Fraction]
Matrix = list[Row]


def vec(*values: int) -> Row:
    """A row of exact Fractions from integers, one entry per state."""
    return [Fraction(v) for v in values]


INCOMPLETE: Matrix = [vec(1, 1, 1), vec(0, 1, 2)]
COMPLETE: Matrix = [vec(1, 0, 0), vec(0, 1, 0), vec(0, 0, 1), vec(1, 2, 3)]
CLAIMS: tuple[tuple[str, Row], ...] = (
    ("(1,2,3)", vec(1, 2, 3)),
    ("(0,0,1)", vec(0, 0, 1)),
    ("(5,0,0)", vec(5, 0, 0)),
)


def check_matrix(matrix: Matrix) -> int:
    """Return the number of states (the number of columns), or raise ValueError if the matrix is not rectangular."""
    if not matrix or not matrix[0]:
        raise ValueError("payoff matrix must have at least one security and one state")
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("every security must pay in the same states")
    return width


def rank(matrix: Matrix) -> int:
    """The rank of a rectangular matrix of exact Fractions, the number of pivots found by Gaussian elimination.

    Each pivot is the first nonzero entry in its column among the rows not yet used. Rows are eliminated below and
    above each pivot, so the arithmetic stays exact and the rank is an integer, with no tolerance.
    """
    rows = [list(row) for row in matrix]
    n_rows = len(rows)
    n_cols = len(rows[0]) if rows else 0
    used = 0
    for col in range(n_cols):
        pivot = next((i for i in range(used, n_rows) if rows[i][col] != 0), None)
        if pivot is None:
            continue
        rows[used], rows[pivot] = rows[pivot], rows[used]
        for i in range(n_rows):
            if i != used and rows[i][col] != 0:
                factor = rows[i][col] / rows[used][col]
                rows[i] = [a - factor * b for a, b in zip(rows[i], rows[used], strict=True)]
        used += 1
        if used == n_rows:
            break
    return used


def attainable(payoff: Row, matrix: Matrix) -> bool:
    """True when the payoff lies in the row space of the matrix, tested by rank(matrix with payoff appended) == rank."""
    if len(payoff) != check_matrix(matrix):
        raise ValueError("a payoff must have one entry per state")
    return rank([*matrix, payoff]) == rank(matrix)


def tup(row: Row) -> str:
    """The row as a printable tuple of exact Fractions."""
    return "(" + ",".join(str(z) for z in row) + ")"


def main() -> None:
    """Print Parts A to E. Every value is an exact integer or Fraction, so the output is reproducible."""
    states = check_matrix(INCOMPLETE)
    check_matrix(COMPLETE)

    print("Part A: rank of each payoff matrix by exact Gaussian elimination")
    print(f"incomplete securities {len(INCOMPLETE)} states {states} rank {rank(INCOMPLETE)}")
    print(f"complete securities {len(COMPLETE)} states {check_matrix(COMPLETE)} rank {rank(COMPLETE)}")

    print("Part B: complete if and only if rank equals the number of states")
    for name, matrix in (("incomplete", INCOMPLETE), ("complete", COMPLETE)):
        n_states = check_matrix(matrix)
        r = rank(matrix)
        print(f"{name} rank {r} states {n_states} complete {r == n_states} rank_minus_states {r - n_states}")

    print("Part C: attainability in the incomplete market, tested by rank of the matrix with the payoff appended")
    for label, claim in CLAIMS:
        augmented = rank([*INCOMPLETE, claim])
        print(f"claim {label} attainable {attainable(claim, INCOMPLETE)} augmented_rank {augmented}")

    print("Part D: the same three payoffs in the complete market")
    for label, claim in CLAIMS:
        print(f"claim {label} attainable {attainable(claim, COMPLETE)} augmented_rank {rank([*COMPLETE, claim])}")

    print("Part E: the redundant fourth security leaves the rank unchanged")
    print(f"first_three_rows_rank {rank(COMPLETE[:3])} all_four_rows_rank {rank(COMPLETE)}")
    weights = (Fraction(1), Fraction(2), Fraction(3))
    combo = [sum((w * COMPLETE[j][s] for j, w in enumerate(weights)), Fraction(0)) for s in range(states)]
    print(f"weighted_sum_of_first_three_rows {tup(combo)} equals_fourth_row {combo == COMPLETE[3]}")


main()
