"""PC3 lab L04: the market-making game on seed 0, one fixed quoting rule, and two exact checks.

SIMULATED. The fair path and the arrivals are model inputs drawn from random.Random(0). No data file is read and there
is no network access. Standard library only. Money is an integer number of cents. Expectations and variances are
fractions.Fraction, so every printed value is exact; a printed fraction such as 5/2 is 2.5 cents.

Part 1 plays the 20-turn game on seed 0 with the lesson's rule: quote symmetrically on the last filled price, or
at 10000 cents before any fill, with a half-spread of 10 cents and a size of 1. It prints the turn log and the
settlement, then checks the identity P&L = cash flow + inventory x settlement exactly for this run. It also prints the
number of informed arrivals on seed 0, and a one-line summary of the same rule played on seed 1.

Part 2 enumerates the three arrival outcomes of one turn, for a grid of fair values, from inventory 0 and with the quote
fixed at 9990 and 10010 cents. Its exact expectation of the one-turn change in cash plus inventory times the fair value
is compared with the closed form h/2 - (1/2)[(v - a)^+ + (b - v)^+], where h is the half-spread,
a the ask and b the bid.

Part 3 computes the exact mean and variance of the mark change caused by one fair-value move, for several inventories.

The checks test this one seed and this one grid. They are not a proof for other seeds or other fair values; the lesson
proves the closed form of Part 2 for every fair value, from inventory zero and with the quote held fixed at 9990 and
10010 cents.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from fractions import Fraction

HORIZON = 20  # turns
START_CENTS = 10_000  # v_0, in cents
MOVE_CENTS = 5  # the fair value moves by +5 or -5 cents each turn
MAX_SIZE = 5  # largest quoted size
LIMIT = 10  # inventory limit: a fill is refused when |inventory| would exceed it
HALF_SPREAD = 10  # half-spread of the quoting rule, in cents
SEED = 0
ARRIVAL_PROBABILITY = {"uninformed-buy": Fraction(1, 4), "uninformed-sell": Fraction(1, 4), "informed": Fraction(1, 2)}


@dataclass(frozen=True)
class Turn:
    """One turn of the log. Money is in cents, inventory in units. side is +1 when the maker buys, -1 when it sells."""

    turn: int
    bid_cents: int
    ask_cents: int
    size: int
    arrival: str
    filled: bool
    fill_price_cents: int | None
    side: int
    cash_flow_cents: int
    inventory_after: int
    cash_after_cents: int


def draw_game(seed: int) -> tuple[list[int], list[str]]:
    """The fair path v_0 .. v_HORIZON (cents) and the arrival of each turn, drawn from random.Random(seed).

    Turn t uses two draws in this order. The first sets the move: +5 cents if the draw is below 0.5, otherwise -5 cents.
    The second sets the arrival: uninformed buy below 0.25, uninformed sell below 0.5, otherwise informed.
    """
    rng = random.Random(seed)
    path = [START_CENTS]
    arrivals: list[str] = []
    for _ in range(HORIZON):
        move = MOVE_CENTS if rng.random() < 0.5 else -MOVE_CENTS
        path.append(path[-1] + move)
        draw = rng.random()
        if draw < 0.25:
            arrivals.append("uninformed-buy")
        elif draw < 0.5:
            arrivals.append("uninformed-sell")
        else:
            arrivals.append("informed")
    return path, arrivals


def quote(last_fill_cents: int | None) -> tuple[int, int, int]:
    """The lesson's rule: mid = last filled price, or 10000 before any fill; bid = mid - 10; ask = mid + 10; size 1."""
    mid = START_CENTS if last_fill_cents is None else last_fill_cents
    return mid - HALF_SPREAD, mid + HALF_SPREAD, 1


def customer_side(arrival: str, fair_cents: int, bid_cents: int, ask_cents: int) -> int:
    """Return +1 if the customer sells to the maker at the bid, -1 if the customer buys at the ask, 0 for no trade.

    An uninformed order names its direction; whether it fills is decided in play(). An informed trader buys at the ask
    when the fair value is above the ask, sells at the bid when the fair value is below the bid, and otherwise does not
    trade.
    """
    if arrival == "uninformed-buy":
        return -1
    if arrival == "uninformed-sell":
        return 1
    if fair_cents > ask_cents:
        return -1
    if fair_cents < bid_cents:
        return 1
    return 0


def play(seed: int) -> tuple[list[int], list[Turn]]:
    """Play the 20 turns. A fill needs size >= 1, a trade on the arrival, and |inventory| within the limit after it."""
    path, arrivals = draw_game(seed)
    inventory = 0
    cash = 0
    last_fill: int | None = None
    turns: list[Turn] = []
    for t in range(1, HORIZON + 1):
        bid, ask, size = quote(last_fill)
        arrival = arrivals[t - 1]
        side = customer_side(arrival, path[t], bid, ask)
        filled = side != 0 and size >= 1 and abs(inventory + side) <= LIMIT
        price: int | None = None
        cash_flow = 0
        if filled:
            price = ask if side < 0 else bid
            cash_flow = -side * price
            inventory += side
            cash += cash_flow
            last_fill = price
        turns.append(
            Turn(
                turn=t,
                bid_cents=bid,
                ask_cents=ask,
                size=size,
                arrival=arrival,
                filled=filled,
                fill_price_cents=price,
                side=side if filled else 0,
                cash_flow_cents=cash_flow,
                inventory_after=inventory,
                cash_after_cents=cash,
            )
        )
    return path, turns


def part_one() -> None:
    print("Part 1 · seed 0, 20 turns, SIMULATED fair path and arrivals")
    path, turns = play(SEED)
    print("turn  bid    ask    size  arrival           filled  fill    inv  cash_after")
    for r in turns:
        fill = "-" if r.fill_price_cents is None else str(r.fill_price_cents)
        print(
            f"{r.turn:>4}  {r.bid_cents:>5}  {r.ask_cents:>5}  {r.size:>4}  {r.arrival:<16}  "
            f"{r.filled!s:<6}  {fill:>6}  {r.inventory_after:>3}  {r.cash_after_cents:>10}"
        )
    settlement = path[HORIZON]
    fills = [r for r in turns if r.filled]
    cash_flow = sum(r.cash_flow_cents for r in fills)
    inventory_end = turns[-1].inventory_after
    mark = inventory_end * settlement
    pnl = turns[-1].cash_after_cents + mark
    print(f"fills {len(fills)} of {HORIZON} turns")
    print(f"cash flow, sum of the fill cash flows = {cash_flow} cents")
    print(f"inventory at the end = {inventory_end} units")
    print(f"settlement fair value v_{HORIZON} = {settlement} cents")
    print(f"inventory mark = inventory x settlement = {mark} cents")
    print(f"P&L = cash + inventory mark = {pnl} cents")
    print(f"identity P&L = cash flow + inventory x settlement: {pnl == cash_flow + inventory_end * settlement}")
    print(f"cash after the last turn equals the cash flow sum: {turns[-1].cash_after_cents == cash_flow}")
    print(f"largest |inventory| over the run = {max(abs(r.inventory_after) for r in turns)} (limit {LIMIT})")
    quotes_valid = all(r.bid_cents < r.ask_cents and 0 <= r.size <= MAX_SIZE for r in turns)
    print(f"every quote has bid < ask and 0 <= size <= {MAX_SIZE}: {quotes_valid}")
    fills_at_quote = all(r.fill_price_cents in (r.bid_cents, r.ask_cents) for r in fills)
    print(f"every fill price is the bid or the ask of its own turn: {fills_at_quote}")
    informed = sum(1 for r in turns if r.arrival == "informed")
    print(f"informed arrivals on seed 0 = {informed} of {HORIZON} turns")
    path_one, turns_one = play(1)
    fills_one = [r for r in turns_one if r.filled]
    cash_flow_one = sum(r.cash_flow_cents for r in fills_one)
    inventory_one = turns_one[-1].inventory_after
    settlement_one = path_one[HORIZON]
    pnl_one = turns_one[-1].cash_after_cents + inventory_one * settlement_one
    print(
        f"seed 1, same rule: fills {len(fills_one)} of {HORIZON} turns, cash flow {cash_flow_one} cents, "
        f"inventory at the end {inventory_one} units, settlement {settlement_one} cents, P&L {pnl_one} cents"
    )


def one_turn_change(fair_cents: int, bid_cents: int, ask_cents: int) -> Fraction:
    """Exact expectation of the one-turn change in cash + inventory x fair value, from inventory 0 and size 1."""
    total = Fraction(0)
    for arrival, probability in ARRIVAL_PROBABILITY.items():
        side = customer_side(arrival, fair_cents, bid_cents, ask_cents)
        if side == 0:
            continue
        price = ask_cents if side < 0 else bid_cents
        total += probability * (-side * price + side * fair_cents)
    return total


def closed_form(fair_cents: int, bid_cents: int, ask_cents: int) -> Fraction:
    """h/2 - (1/2)[(v - a)^+ + (b - v)^+] with h = (a - b)/2: the same quantity in closed form."""
    h = Fraction(ask_cents - bid_cents, 2)
    above = max(fair_cents - ask_cents, 0)
    below = max(bid_cents - fair_cents, 0)
    return h / 2 - Fraction(above + below, 2)


def part_two() -> None:
    print("Part 2 · one turn from inventory 0, quote 9990 bid and 10010 ask, exact expectation by enumeration")
    bid, ask = START_CENTS - HALF_SPREAD, START_CENTS + HALF_SPREAD
    agree = True
    for fair in range(9980, 10025, 5):
        exact = one_turn_change(fair, bid, ask)
        formula = closed_form(fair, bid, ask)
        agree = agree and exact == formula
        same = exact == formula
        print(f"fair value v = {fair}: E[change] = {exact} cents, closed form = {formula} cents, equal: {same}")
    print(f"enumeration equals the closed form on every grid point: {agree}")


def fair_move_mark_change(inventory: int) -> tuple[Fraction, Fraction]:
    """Mean and variance of the mark change I x (v_t - v_{t-1}) from one fair-value move of +5 or -5 cents."""
    moves = [Fraction(MOVE_CENTS), Fraction(-MOVE_CENTS)]
    changes = [inventory * m for m in moves]
    mean = sum(changes, Fraction(0)) / len(changes)
    variance = sum(((c - mean) ** 2 for c in changes), Fraction(0)) / len(changes)
    return mean, variance


def part_three() -> None:
    print("Part 3 · mark change from one fair-value move, exact mean and variance over the two equally likely moves")
    for inventory in (0, 1, 3, -3, LIMIT):
        mean, variance = fair_move_mark_change(inventory)
        print(
            f"inventory {inventory:>3}: mean = {mean} cents, variance = {variance} cents^2, "
            f"variance equals 25 x inventory^2: {variance == MOVE_CENTS**2 * inventory**2}"
        )


def main() -> None:
    part_one()
    part_two()
    part_three()


main()
