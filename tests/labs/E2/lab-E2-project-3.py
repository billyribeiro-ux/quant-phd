"""Rung 3 check: the reference engine on a reference case, and the exact single-unit checks.

Standard library only. Model: n bidders with independent private values, each uniform on [0, 10000] cents, a
continuous model as in Assumption 2 of the project page. Each bidder is risk neutral and wants one unit. The bids and
values of the reference case are typed in for this check. They are illustrative, not generated and not data.

Copy this file into run_report.py beside auction_sim.py, then replace the calls to these functions with calls
to auction_sim.
"""

from fractions import Fraction
from math import comb, factorial

CAP = 10000  # the value cap, in cents: a value is uniform on [0, CAP]


def ranking(bids: list[int]) -> list[int]:
    """Bidder indices from the highest bid to the lowest; a tie goes to the lower index."""
    return sorted(range(len(bids)), key=lambda i: (-bids[i], i))


def allocate(bids: list[int], units: int) -> list[bool]:
    """True for each of the `units` highest bidders."""
    winners = set(ranking(bids)[:units])
    return [i in winners for i in range(len(bids))]


def payments(format_name: str, bids: list[int], units: int) -> list[int]:
    """Cents paid by each bidder: a winner pays the uniform price or its own bid; a loser pays 0."""
    won = allocate(bids, units)
    clearing = bids[ranking(bids)[units]]
    if format_name == "uniform":
        return [clearing if w else 0 for w in won]
    return [bid if w else 0 for bid, w in zip(bids, won, strict=True)]


def revenue(format_name: str, bids: list[int], units: int) -> int:
    """The sum of the payments, in cents."""
    return sum(payments(format_name, bids, units))


def efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]:
    """The value of the winners, and the value of the `units` highest values, in cents."""
    won = allocate(bids, units)
    achieved = sum(v for v, w in zip(values, won, strict=True) if w)
    best = sum(sorted(values, reverse=True)[:units])
    return achieved, best


def symmetric_bid_single_unit(format_name: str, n: int, value: int) -> int:
    """The symmetric equilibrium bid with one unit, in cents: (n-1)/n of the value, or the value under uniform."""
    if format_name == "uniform":
        return value
    return (2 * (n - 1) * value + n) // (2 * n)  # (n-1)*value/n rounded half up, in integers


def beta_integral(a: int, b: int) -> Fraction:
    """The exact integral of x**a * (1-x)**b over [0, 1], which is a! b! / (a+b+1)!."""
    return Fraction(factorial(a) * factorial(b), factorial(a + b + 1))


def expected_order_statistic(n: int, j: int) -> Fraction:
    """E[V_(j)] for the j-th highest of n independent uniform[0,1] values, as the integral of P(V_(j) > x) over [0, 1].

    V_(j) exceeds x when at least j values exceed x, and m values exceed x with probability C(n,m) (1-x)^m x^(n-m).
    """
    return sum((comb(n, m) * beta_integral(n - m, m) for m in range(j, n + 1)), Fraction(0))


def first_price_payoff(n: int, value: int, bid: int) -> Fraction:
    """Expected payoff of a bid against n-1 rivals who bid (n-1)/n of their values, with values uniform on [0, CAP].

    A rival's bid is below `bid` when its value is below bid*n/(n-1), so the bid wins with that
    probability to the power n-1.
    """
    cutoff = min(Fraction(bid * n, n - 1), Fraction(CAP))
    return (value - bid) * (cutoff / CAP) ** (n - 1)


def main() -> None:
    bids = [7400, 6200, 8100, 6200, 5300]  # cents; the tie at 6200 is between bidders 1 and 3
    values = [6000, 7800, 9000, 6900, 5000]  # cents, the values behind the bids
    units = 3
    won = allocate(bids, units)
    print("ranking (bidder indices):", ranking(bids))
    print("winners (bidder indices):", [i for i, w in enumerate(won) if w])
    uniform_revenue = revenue("uniform", bids, units)
    print("uniform payments (cents):", payments("uniform", bids, units), "| revenue:", uniform_revenue)
    print(
        "discriminatory payments (cents):",
        payments("discriminatory", bids, units),
        "| revenue:",
        revenue("discriminatory", bids, units),
    )
    gap = revenue("discriminatory", bids, units) - uniform_revenue
    print(
        f"discriminatory minus uniform (cents): {gap} | share of the uniform revenue: "
        f"{100 * gap / uniform_revenue:.1f} %"
    )
    achieved, best = efficiency(values, bids, units)
    print("value of the winners (cents):", achieved, "| value of the 3 highest values (cents):", best)
    print(f"allocative efficiency, winners' value as a share of the best: {100 * achieved / best:.1f} %")
    print("single unit, first price, value 7300 cents: closed form, grid best bid, agree")
    for n in range(2, 6):
        closed = symmetric_bid_single_unit("discriminatory", n, 7300)
        grid = max(range(CAP + 1), key=lambda b: first_price_payoff(n, 7300, b))
        print(f"n = {n}: bid {closed} | grid best bid {grid} | agree: {closed == grid}")
    print("one unit, exact expected revenue as a share of the value cap (values uniform on [0, 1]):")
    for n in range(2, 6):
        first = Fraction(n - 1, n) * expected_order_statistic(n, 1)
        second = expected_order_statistic(n, 2)
        print(f"n = {n}: first price {first} | second price {second} | equal: {first == second}")


main()
