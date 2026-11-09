"""Lab FC2-L06-1: one-period replication, risk-neutral pricing and a two-step binomial tree.

Every number is exact. Shares, bond positions, stock prices, payoffs and values are Fraction
values. Stock prices, payoffs and values after one move are printed in currency units; shares
and bond positions are printed as exact fractions, because they are positions. Only the time-0
values are also printed in integer cents: the one-period cost V0, the one-period discounted
expectation and the two-period V0 (half up, which changes nothing here because each is already
a whole number of cents). The parameters are model inputs chosen for exact arithmetic, not
market data and not a forecast: spot 100 currency units, strike 100, up factor 3/2, down
factor 1/2, and gross riskless return 5/4 per period. The claim is a European call paid at
expiry, with payoff max(S - K, 0). No input is random and no data file is read.
"""

from __future__ import annotations

import math
from fractions import Fraction

SPOT = Fraction(100)
STRIKE = Fraction(100)
UP = Fraction(3, 2)  # gross move on an up step
DOWN = Fraction(1, 2)  # gross move on a down step
RETURN = Fraction(5, 4)  # gross riskless return per period, R_f = 1 + r_1 (r_1 is the one-period rate)


def cents(amount: Fraction) -> int:
    """Integer cents of a currency amount, rounded half up (0.5 cent goes up)."""
    return math.floor(amount * 100 + Fraction(1, 2))


def payoff(price: Fraction) -> Fraction:
    """Payoff at expiry of the European call with the strike above, in currency units."""
    return max(price - STRIKE, Fraction(0))


def replicate(
    up_value: Fraction, down_value: Fraction, spot: Fraction, up: Fraction, down: Fraction
) -> tuple[Fraction, Fraction]:
    """Shares and bond position that give the two next-date values, from one node.

    The bond position is the cash lent (positive) or borrowed (negative) at the node, repaid at
    RETURN per period. The two equations are solved exactly; up differs from down, so the solution is unique.
    """
    shares = (up_value - down_value) / ((up - down) * spot)
    bond = (up * down_value - down * up_value) / ((up - down) * RETURN)
    return shares, bond


def main() -> None:
    """Price one period two ways, price two periods by backward induction, and check the replication."""
    q = (RETURN - DOWN) / (UP - DOWN)
    print(f"parameters: spot={SPOT} strike={STRIKE} up={UP} down={DOWN} gross return per period={RETURN}")
    print(f"risk-neutral up probability q=(R-d)/(u-d) = {q}")

    print("one period")
    up_value, down_value = payoff(SPOT * UP), payoff(SPOT * DOWN)
    shares, bond = replicate(up_value, down_value, SPOT, UP, DOWN)
    price = shares * SPOT + bond
    print(f"  payoff after an up move = {up_value}; after a down move = {down_value}")
    print(f"  replicating shares = {shares}; bond position = {bond}")
    print(f"  replicating cost V0 = {price} = {cents(price)} cents")
    expected_value = (q * up_value + (1 - q) * down_value) / RETURN
    print(f"  discounted risk-neutral expectation = {expected_value} = {cents(expected_value)} cents")
    replicated_up = shares * SPOT * UP + bond * RETURN
    replicated_down = shares * SPOT * DOWN + bond * RETURN
    one_period_ok = replicated_up == up_value and replicated_down == down_value and price == expected_value
    print(f"  portfolio matches the payoff in both states and equals the expectation: {one_period_ok}")

    print("two periods")
    uu, ud, dd = SPOT * UP * UP, SPOT * UP * DOWN, SPOT * DOWN * DOWN
    terminal = {"uu": payoff(uu), "ud": payoff(ud), "dd": payoff(dd)}
    print(f"  stock at expiry: uu={uu} ud={ud} dd={dd}")
    print(f"  payoff at expiry: uu={terminal['uu']} ud={terminal['ud']} dd={terminal['dd']}")
    # Backward induction: each node's value is the risk-neutral discounted expectation of its two successors.
    value_after_up = (q * terminal["uu"] + (1 - q) * terminal["ud"]) / RETURN
    value_after_down = (q * terminal["ud"] + (1 - q) * terminal["dd"]) / RETURN
    value_today = (q * value_after_up + (1 - q) * value_after_down) / RETURN
    print(f"  backward induction: value after an up move = {value_after_up}; after a down move = {value_after_down}")
    print(f"  backward induction: V0 = {value_today} = {cents(value_today)} cents")

    # Closed form: discount the q-weighted sum over the paths of the tree.
    closed = (
        sum(math.comb(2, k) * q**k * (1 - q) ** (2 - k) * payoff(SPOT * UP**k * DOWN ** (2 - k)) for k in range(3))
        / RETURN**2
    )
    print(f"  closed form over paths: V0 = {closed} = {cents(closed)} cents")

    # Direct replication: hold the time-0 portfolio, rebalance at the node reached, and check the payoff.
    shares0, bond0 = replicate(value_after_up, value_after_down, SPOT, UP, DOWN)
    wealth_up = shares0 * SPOT * UP + bond0 * RETURN
    wealth_down = shares0 * SPOT * DOWN + bond0 * RETURN
    print(f"  time-0 holdings: shares {shares0}, bond {bond0}, cost {shares0 * SPOT + bond0}")
    print(
        f"  wealth after an up move = {wealth_up} (value_after_up {value_after_up}); after a down move = {wealth_down}"
    )
    shares_u, bond_u = replicate(terminal["uu"], terminal["ud"], SPOT * UP, UP, DOWN)
    shares_d, bond_d = replicate(terminal["ud"], terminal["dd"], SPOT * DOWN, UP, DOWN)
    print(f"  holdings after an up move: shares {shares_u}, bond {bond_u}")
    print(f"  holdings after a down move: shares {shares_d}, bond {bond_d}")
    # (path, terminal wealth of the strategy, payoff of the claim on that path)
    paths = [
        ("uu", shares_u * uu + bond_u * RETURN, terminal["uu"]),
        ("ud", shares_u * ud + bond_u * RETURN, terminal["ud"]),
        ("du", shares_d * ud + bond_d * RETURN, terminal["ud"]),
        ("dd", shares_d * dd + bond_d * RETURN, terminal["dd"]),
    ]
    for label, wealth_end, target in paths:
        print(f"  path {label}: terminal wealth {wealth_end} = payoff {target}: {wealth_end == target}")
    # Self-financing: the holdings chosen at each node cost exactly the wealth carried to that node.
    rebalance_up_ok = shares_u * SPOT * UP + bond_u == wealth_up
    rebalance_down_ok = shares_d * SPOT * DOWN + bond_d == wealth_down
    self_financing = (
        all(wealth_end == target for _, wealth_end, target in paths) and rebalance_up_ok and rebalance_down_ok
    )
    matches_induction = (
        wealth_up == value_after_up and wealth_down == value_after_down and shares0 * SPOT + bond0 == value_today
    )
    reproduced = self_financing and matches_induction
    print(f"  self-financing strategy reproduces every node value and every payoff: {reproduced}")

    assert one_period_ok
    assert value_today == closed == Fraction(45)
    assert self_financing and matches_induction


main()
