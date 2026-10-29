"""E1 lab L08: Pareto efficiency in a two-consumer exchange economy, with exact arithmetic.

Standard library only (fractions). No randomness and no network. The totals are X_TOTAL = 8 units of good x and
Y_TOTAL = 4 units of good y. Consumer A holds (x, y) and consumer B holds the rest, (X_TOTAL - x, Y_TOTAL - y). Both
consumers have product utilities, u = (units of x) * (units of y).

Part A checks the integer grid of the 9 * 5 = 45 feasible allocations of A: an allocation is grid-efficient when no
other grid allocation weakly raises both utilities and strictly raises one. Part B lists the interior diagonal
allocations, which satisfy y * X_TOTAL = x * Y_TOTAL. Part C takes each interior grid-efficient allocation that is
off the diagonal and exhibits an exact rational allocation that strictly raises both utilities, with a non-integer
amount. Part D shows that two diagonal allocations with unequal utilities are both grid-efficient. Part E checks, in
integers, the bound sqrt(uA) + sqrt(uB) <= sqrt(X_TOTAL * Y_TOTAL) at every grid point, and finds the points
where it holds with equality. The checks are finite and exact; they test these instances only, and the
proof for every economy is on the page.
"""

from __future__ import annotations

from fractions import Fraction

X_TOTAL = 8
Y_TOTAL = 4

Allocation = tuple[Fraction, Fraction]


def utility_a(x: Fraction, y: Fraction) -> Fraction:
    """Consumer A's utility x * y for the units of good x and good y that A holds."""
    return x * y


def utility_b(x: Fraction, y: Fraction) -> Fraction:
    """Consumer B's utility of the rest of the totals, (X_TOTAL - x) * (Y_TOTAL - y)."""
    return (X_TOTAL - x) * (Y_TOTAL - y)


def grid() -> list[tuple[int, int]]:
    """The 9 * 5 feasible integer allocations of A, with 0 <= x <= X_TOTAL and 0 <= y <= Y_TOTAL."""
    return [(x, y) for x in range(X_TOTAL + 1) for y in range(Y_TOTAL + 1)]


def weakly_raises_both_strictly_one(z: Allocation, w: Allocation) -> bool:
    """True when z Pareto-dominates w: no consumer is worse off at z, and at least one is strictly better off."""
    ua_z, ub_z = utility_a(*z), utility_b(*z)
    ua_w, ub_w = utility_a(*w), utility_b(*w)
    return ua_z >= ua_w and ub_z >= ub_w and (ua_z > ua_w or ub_z > ub_w)


def grid_efficient(w: Allocation) -> bool:
    """True when no grid allocation Pareto-dominates w."""
    return not any(weakly_raises_both_strictly_one((Fraction(x), Fraction(y)), w) for x, y in grid())


def on_diagonal(x: int, y: int) -> bool:
    """The diagonal y / x = Y_TOTAL / X_TOTAL, written without division so that x = 0 is allowed."""
    return y * X_TOTAL == x * Y_TOTAL


def interior(x: int, y: int) -> bool:
    """Both consumers hold a positive amount of both goods."""
    return 0 < x < X_TOTAL and 0 < y < Y_TOTAL


def improvement(x: int, y: int) -> Allocation:
    """An exact rational allocation for A that strictly raises both utilities over the interior allocation (x, y).

    The ratio of A's marginal rates is y / x; B's is (Y - y) / (X - x). When they differ, a trade at a rate lambda
    strictly between them, of size h, raises both utilities. The largest admissible h is found from the two
    inequalities, and h is taken as half of it, so both utilities are strictly higher.
    """
    xa, ya = Fraction(x), Fraction(y)
    xb, yb = X_TOTAL - xa, Y_TOTAL - ya
    rate_a, rate_b = ya / xa, yb / xb
    lam = (rate_a + rate_b) / 2
    if rate_b < rate_a:
        # A receives h units of good x from B and gives lam * h units of good y to B.
        h = min((ya - lam * xa) / lam, (lam * xb - yb) / lam) / 2
        new_a = (xa + h, ya - lam * h)
    else:
        # A gives h units of good x to B and receives lam * h units of good y from B.
        h = min((lam * xa - ya) / lam, (yb - lam * xb) / lam) / 2
        new_a = (xa - h, ya + lam * h)
    if not weakly_raises_both_strictly_one(new_a, (xa, ya)):
        raise AssertionError(f"no improvement found over ({x}, {y})")
    if utility_a(*new_a) <= utility_a(xa, ya) or utility_b(*new_a) <= utility_b(xa, ya):
        raise AssertionError(f"the improvement over ({x}, {y}) is not strict for both consumers")
    return new_a


def part_a() -> list[tuple[int, int]]:
    efficient = [(x, y) for x, y in grid() if grid_efficient((Fraction(x), Fraction(y)))]
    print(f"part A: feasible grid allocations = {len(grid())}; grid-efficient allocations = {len(efficient)}")
    interior_efficient = [(x, y) for x, y in efficient if interior(x, y)]
    boundary_efficient = [(x, y) for x, y in efficient if not interior(x, y)]
    print(f"part A: grid-efficient interior allocations (0 < x < {X_TOTAL}, 0 < y < {Y_TOTAL}) = {interior_efficient}")
    print(f"part A: grid-efficient boundary allocations = {boundary_efficient}")
    return interior_efficient


def part_b(interior_efficient: list[tuple[int, int]]) -> None:
    diagonal = [(x, y) for x, y in grid() if interior(x, y) and on_diagonal(x, y)]
    if not all(grid_efficient((Fraction(x), Fraction(y))) for x, y in diagonal):
        raise AssertionError("a diagonal interior allocation is not grid-efficient")
    print(f"part B: interior diagonal allocations = {diagonal}; all grid-efficient: True")
    on_line = [p for p in interior_efficient if on_diagonal(*p)]
    print(f"part B: interior grid-efficient allocations on the diagonal = {on_line}")


def part_c(interior_efficient: list[tuple[int, int]]) -> None:
    off = [(x, y) for x, y in interior_efficient if not on_diagonal(x, y)]
    print(f"part C: interior grid-efficient allocations off the diagonal = {len(off)}")
    for x, y in off:
        new_a = improvement(x, y)
        new_b = (X_TOTAL - new_a[0], Y_TOTAL - new_a[1])
        print(
            f"part C: from ({x}, {y}) (utilities {utility_a(Fraction(x), Fraction(y))} and "
            f"{utility_b(Fraction(x), Fraction(y))}), A and B can move to A = ({new_a[0]}, {new_a[1]}) and "
            f"B = ({new_b[0]}, {new_b[1]}), with utilities {utility_a(*new_a)} and {utility_b(*new_a)}"
        )


def part_d() -> None:
    for held_a, held_b in (((6, 3), (2, 1)), ((2, 1), (6, 3))):
        point = (Fraction(held_a[0]), Fraction(held_a[1]))
        if not grid_efficient(point):
            raise AssertionError(f"the diagonal allocation {held_a} is not grid-efficient")
        print(
            f"part D: A holds {held_a}, B holds {held_b}: utilities {utility_a(*point)} and "
            f"{utility_b(*point)}; grid-efficient: True"
        )


def part_e() -> None:
    equality: list[tuple[int, int]] = []
    for x, y in grid():
        ua, ub = utility_a(Fraction(x), Fraction(y)), utility_b(Fraction(x), Fraction(y))
        slack = X_TOTAL * Y_TOTAL - ua - ub
        if slack < 0 or 4 * ua * ub > slack * slack:
            raise AssertionError(f"the bound fails at ({x}, {y})")
        if 4 * ua * ub == slack * slack:
            equality.append((x, y))
    diagonal = [(x, y) for x, y in grid() if on_diagonal(x, y)]
    print(f"part E: the bound sqrt(uA) + sqrt(uB) <= sqrt({X_TOTAL * Y_TOTAL}) holds at all {len(grid())} grid points")
    print(f"part E: equality at {len(equality)} grid points = {equality}")
    print(f"part E: the equality points are exactly the diagonal allocations: {sorted(equality) == sorted(diagonal)}")


def main() -> None:
    interior_efficient = part_a()
    part_b(interior_efficient)
    part_c(interior_efficient)
    part_d()
    part_e()


main()
