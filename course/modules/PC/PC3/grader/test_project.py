"""Acceptance suite for the PC3 project: the quoting rule and the replay of a game log (market_maker.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your market_maker.py, engine.py and instance.py next to this file. Warnings are failures, as in the browser.

Each test checks a property or a number of the game defined in Lesson 4 and in the project specification. Two instances
are used, seed SEED and seed SEED + 7919, so a fixed answer for one seed must also match the other. Every expected value
is computed here, from the log's own fields and this file's own oracle, never from the student's module. A failing test
names the property it checks and the idea to revisit; it never prints the value the property should have.

A test expects an exception only for the conditions the specification names as invalid: a crossed or locked quote, a
size outside 0..5, a log that is not 20 turns long, and a filled turn with no fill price. Every other failure is a plain
property check.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any

import engine
import market_maker as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
SEEDS = (SEED, SEED + 7_919)
HORIZON = 20
MONEY_AND_UNITS = ("cash_flow_cents", "inventory_end", "inventory_mark_cents", "pnl_cents")
FLAT_PATH = [10_000] * (HORIZON + 1)
ARRIVAL_NAMES = {"uninformed-buy", "uninformed-sell", "informed"}


def expect(condition: bool, message: str) -> None:
    """Fail with the property's message. The message never contains a computed value."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(message)


def must_refuse(call: Callable[[], object], phrase: str) -> None:
    """Fail unless call() raises ValueError and the message names ``phrase``. Only for the named invalid inputs."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError as error:
        expect(phrase in str(error), f"the refusal must name the condition {phrase!r}")
        return
    pytest.fail(f"the specification requires a ValueError naming {phrase!r}, and none was raised")


def fixed_quote(state: dict[str, object]) -> tuple[int, int, int]:
    """A quote the suite owns: bid 9990, ask 10010, size 1 on every turn. It makes logs the student does not write."""
    return 9_990, 10_010, 1


def fixed_log(seed: int) -> dict[str, Any]:
    """The log of the suite's own fixed quote on ``seed``."""
    return engine.play(fixed_quote, seed)


def oracle(log: dict[str, Any]) -> dict[str, int]:
    """The accounts of a log, from its fills alone. A fill at the bid is a maker purchase, at the ask a maker sale."""
    cash = 0
    inventory = 0
    for turn in log["turns"]:
        if turn["filled"]:
            price = turn["fill_price_cents"]
            side = 1 if price == turn["bid_cents"] else -1
            cash += -side * price
            inventory += side
    mark = inventory * log["settlement_cents"]
    return {"cash_flow_cents": cash, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash + mark}


def turn_record(
    turn: int,
    *,
    bid: int = 9_990,
    ask: int = 10_010,
    size: int = 1,
    arrival: str = "uninformed-sell",
    filled: bool = False,
    price: int | None = None,
    inventory: int = 0,
    cash: int = 0,
) -> dict[str, Any]:
    """A hand-built turn record with the keys the engine writes."""
    return {
        "turn": turn,
        "bid_cents": bid,
        "ask_cents": ask,
        "size": size,
        "arrival": arrival,
        "filled": filled,
        "fill_price_cents": price,
        "inventory_after": inventory,
        "cash_after_cents": cash,
    }


def hand_log(turns: list[dict[str, Any]], settlement: int) -> dict[str, Any]:
    """A hand-built log: the seed, the settlement value and the turn records."""
    return {"seed": SEED, "settlement_cents": settlement, "turns": turns}


def custom_instance(path: list[int], arrivals: list[str]) -> dict[str, Any]:
    """An instance the suite writes out in full, for the rules of the engine. It replaces make_instance in one test."""
    return {
        "seed": SEED,
        "label": "SIMULATED",
        "start_cents": 10_000,
        "fair_path_cents": path,
        "arrivals": arrivals,
        "settlement_cents": path[-1],
    }


def play_custom(
    monkeypatch: pytest.MonkeyPatch,
    path: list[int],
    arrivals: list[str],
    quote: Callable[[dict[str, object]], tuple[int, int, int]],
) -> dict[str, Any]:
    """Play the engine on the custom instance. Only the engine's own instance source is replaced."""
    monkeypatch.setattr(engine, "make_instance", lambda seed: custom_instance(path, arrivals))
    return engine.play(quote, SEED)


# Legality of the student's quote, on every turn of both instances.


@pytest.mark.parametrize("seed", SEEDS)
def test_quotes_are_legal_on_every_turn(seed: int) -> None:
    """The quote returns (bid, ask, size) as three integers on each of the 20 turns: bid below ask, size 0..5."""
    quotes: list[object] = []

    def spy(state: dict[str, object]) -> tuple[int, int, int]:
        out = sol.quote(state)
        quotes.append(out)
        return out

    engine.play(spy, seed)  # the engine raises ValueError for a crossed quote or an oversized quote
    expect(len(quotes) == HORIZON, "the policy must return one quote for each of the 20 turns")
    for out in quotes:
        expect(
            isinstance(out, tuple) and len(out) == 3,
            "quote must return a tuple of three values: (bid_cents, ask_cents, size)",
        )
        expect(
            all(type(x) is int for x in out),
            "every value a quote returns must be an integer: cents for prices, units for size",
        )
        bid, ask, size = out
        expect(bid < ask, "every quote needs a bid below its ask")
        expect(0 <= size <= 5, "a quoted size must lie in 0..5")


# The named refusals of an illegal quote. Each is hand-built, and each condition gets its own test.


def test_crossed_quote_is_refused() -> None:
    """A quote with bid equal to ask is locked, and the engine refuses it, naming the condition."""
    must_refuse(lambda: engine.play(lambda state: (10_000, 10_000, 1), SEED), "bid must be below ask")


def test_bid_above_ask_is_refused() -> None:
    """A quote with bid above ask is crossed, and the engine refuses it, naming the condition."""
    must_refuse(lambda: engine.play(lambda state: (10_010, 9_990, 1), SEED), "bid must be below ask")


def test_bid_one_cent_below_ask_is_accepted() -> None:
    """The boundary of the bid rule: a bid one cent below the ask is legal, and the game runs its 20 turns."""
    log = engine.play(lambda state: (9_999, 10_000, 1), SEED)
    expect(len(log["turns"]) == HORIZON, "a legal quote must let the game run its 20 turns")


def test_size_six_is_refused() -> None:
    """A size of 6 is above the largest quoted size, and the engine refuses it, naming the condition."""
    must_refuse(lambda: engine.play(lambda state: (9_990, 10_010, 6), SEED), "size must lie in 0..5")


def test_size_minus_one_is_refused() -> None:
    """A size of -1 is below the smallest quoted size, and the engine refuses it, naming the condition."""
    must_refuse(lambda: engine.play(lambda state: (9_990, 10_010, -1), SEED), "size must lie in 0..5")


@pytest.mark.parametrize("size", [0, 5])
def test_sizes_at_the_edges_of_the_range_are_accepted(size: int) -> None:
    """The boundary of the size rule: 0 and 5 are both legal quoted sizes."""
    log = engine.play(lambda state: (9_990, 10_010, size), SEED)
    expect(len(log["turns"]) == HORIZON, "a size of 0 or 5 is legal and must let the game run its 20 turns")


# The shape of a log, and the replay's refusals.


@pytest.mark.parametrize("length", [19, 21])
def test_replay_refuses_a_log_that_is_not_twenty_turns(length: int) -> None:
    """A log of 19 turns and a log of 21 turns are both refused, naming the condition (exactly 20 turns)."""
    turns = fixed_log(SEED)["turns"]
    short = turns[:-1] if length == 19 else [*turns, turns[-1]]
    must_refuse(lambda: sol.replay(hand_log(short, 10_000)), "a log has exactly 20 turns")


def test_filled_turn_without_a_price_is_refused() -> None:
    """A turn marked filled with no fill price is refused, naming the condition."""
    turns = [turn_record(1, filled=True, arrival="uninformed-buy", price=None, inventory=-1, cash=0)]
    turns += [turn_record(t, size=0, inventory=-1, cash=0) for t in range(2, HORIZON + 1)]
    must_refuse(lambda: sol.replay(hand_log(turns, 10_000)), "a filled turn needs a fill price")


# The replay's numbers, against the fills of the log.


@pytest.mark.parametrize("seed", SEEDS)
def test_replay_returns_the_fills_cash_flow_inventory_and_pnl(seed: int) -> None:
    """replay returns exactly the four keys, and their values equal the fills of the log, for the suite's fixed quote
    and for the student's own quote."""
    for log in (fixed_log(seed), engine.play(sol.quote, seed)):
        out = sol.replay(log)
        expect(
            set(out) == set(MONEY_AND_UNITS),
            "replay must return exactly the keys cash_flow_cents, inventory_end, inventory_mark_cents and pnl_cents",
        )
        expect(
            out == oracle(log),
            "replay must give the cash flow of the fills, the ending inventory, the mark at the settlement value, "
            "and the P&L as their sum",
        )


@pytest.mark.parametrize("seed", SEEDS)
def test_replay_agrees_with_the_engine_final_cash_and_inventory(seed: int) -> None:
    """The cash flow of the fills is the cash the engine holds after the last turn, and the ending inventory is the
    inventory the engine holds after the last turn (cash starts at zero)."""
    log = engine.play(sol.quote, seed)
    out = sol.replay(log)
    last = log["turns"][-1]
    expect(
        out["cash_flow_cents"] == last["cash_after_cents"],
        "the cash flow of the fills must equal the cash after the last turn",
    )
    expect(
        out["inventory_end"] == last["inventory_after"],
        "the ending inventory must equal the inventory after the last turn",
    )


@pytest.mark.parametrize("seed", SEEDS)
def test_pnl_is_cash_flow_plus_inventory_times_settlement(seed: int) -> None:
    """The P&L identity holds exactly, in integer cents: P&L = cash flow + ending inventory x settlement value."""
    log = engine.play(sol.quote, seed)
    out = sol.replay(log)
    settlement = log["settlement_cents"]
    expect(
        out["inventory_mark_cents"] == out["inventory_end"] * settlement,
        "the inventory mark must be the ending inventory times the settlement value",
    )
    expect(
        out["pnl_cents"] == out["cash_flow_cents"] + out["inventory_end"] * settlement,
        "the P&L must equal the cash flow plus the ending inventory times the settlement value, exactly",
    )


@pytest.mark.parametrize("seed", SEEDS)
def test_money_and_units_are_integers(seed: int) -> None:
    """Every value replay returns is an int: money in cents, inventory in units."""
    out = sol.replay(engine.play(sol.quote, seed))
    expect(all(type(out[key]) is int for key in MONEY_AND_UNITS), "every value replay returns must be an integer")


@pytest.mark.parametrize("seed", SEEDS)
def test_cash_moves_by_the_fill_price_on_each_turn(seed: int) -> None:
    """The cash identity: a sale at the ask raises cash by the ask, a purchase at the bid lowers it by the bid, and cash
    does not move on a turn without a fill."""
    log = engine.play(sol.quote, seed)
    previous = 0
    for turn in log["turns"]:
        change = turn["cash_after_cents"] - previous
        if not turn["filled"]:
            expect(change == 0, "cash must not move on a turn without a fill")
        elif turn["fill_price_cents"] == turn["ask_cents"]:
            expect(change == turn["ask_cents"], "a sale at the ask must raise cash by the ask")
        else:
            expect(change == -turn["bid_cents"], "a purchase at the bid must lower cash by the bid")
        previous = turn["cash_after_cents"]


def test_inventory_is_marked_at_the_settlement_value_not_the_quote_mid() -> None:
    """A hand-built log whose last quote mid (10000 cents) differs from its settlement (10003 cents). The mark must use
    the settlement, so the P&L is 10010 - 10003 = 7 cents, not 10010 - 10000."""
    turns = [turn_record(1, filled=True, arrival="uninformed-buy", price=10_010, inventory=-1, cash=10_010)]
    turns += [turn_record(t, size=0, inventory=-1, cash=10_010) for t in range(2, HORIZON + 1)]
    log = hand_log(turns, 10_003)
    expect(
        sol.replay(log) == oracle(log),
        "the inventory must be marked at the settlement value, not at the last quoted mid: "
        "the P&L identity uses the settlement",
    )


@pytest.mark.parametrize("seed", SEEDS)
def test_a_log_carries_its_own_seed_and_settlement(seed: int) -> None:
    """A log names the seed it was played on, and its settlement is the last fair value of that seed's instance."""
    log = engine.play(sol.quote, seed)
    expect(log["seed"] == seed, "a log must name the seed it was played on")
    expect(
        log["settlement_cents"] == make_instance(seed)["settlement_cents"],
        "the settlement of a log must be the last fair value of its own instance",
    )


# The instance: deterministic, valid, and different across seeds.


@pytest.mark.parametrize("seed", SEEDS)
def test_instance_is_deterministic_and_well_formed(seed: int) -> None:
    """make_instance returns the same instance for a seed, with 21 positive fair values that move 5 cents a turn."""
    first = make_instance(seed)
    expect(first == make_instance(seed), "make_instance must return the same instance for the same seed")
    path = first["fair_path_cents"]
    expect(len(path) == HORIZON + 1 and path[0] == 10_000, "the fair path must hold 21 values, starting at 10000 cents")
    expect(all(type(v) is int and v > 0 for v in path), "every fair value must be a positive integer number of cents")
    expect(
        all(abs(path[i + 1] - path[i]) == 5 for i in range(HORIZON)),
        "each turn the fair value must move by exactly 5 cents",
    )
    expect(
        len(first["arrivals"]) == HORIZON and set(first["arrivals"]) <= ARRIVAL_NAMES,
        "each turn has one arrival, named uninformed-buy, uninformed-sell or informed",
    )
    expect(first["settlement_cents"] == path[HORIZON], "the settlement value is the last fair value")


def test_twenty_consecutive_seeds_give_twenty_different_paths() -> None:
    """The fair paths differ across seeds, so a policy tuned to one path does not pass every instance."""
    paths = {tuple(make_instance(s)["fair_path_cents"]) for s in range(SEED, SEED + 20)}
    expect(len(paths) == 20, "twenty consecutive seeds must give twenty different fair paths")


# The engine's rules for the arrivals, checked on hand-built instances (the engine's instance source is replaced).


@pytest.mark.parametrize(("arrival", "limit"), [("uninformed-buy", -10), ("uninformed-sell", 10)])
def test_fills_stop_at_the_inventory_limit_in_each_direction(
    monkeypatch: pytest.MonkeyPatch, arrival: str, limit: int
) -> None:
    """Ten fills take |inventory| to 10. The eleventh would reach 11, so it is not filled, and inventory stays there."""
    log = play_custom(monkeypatch, FLAT_PATH, [arrival] * HORIZON, lambda state: (9_990, 10_010, 1))
    filled = [turn["filled"] for turn in log["turns"]]
    expect(
        filled == [True] * 10 + [False] * 10,
        "a fill must be refused exactly when it would take |inventory| above 10",
    )
    expect(log["turns"][-1]["inventory_after"] == limit, "the inventory after the run must sit at the inventory limit")


def test_a_size_of_zero_never_fills(monkeypatch: pytest.MonkeyPatch) -> None:
    """A fill needs a quoted size of at least 1: with size 0 the buy arrivals never fill."""
    log = play_custom(monkeypatch, FLAT_PATH, ["uninformed-buy"] * HORIZON, lambda state: (9_990, 10_010, 0))
    expect(not any(turn["filled"] for turn in log["turns"]), "a fill needs a quoted size of at least 1")


@pytest.mark.parametrize(
    ("fair", "filled", "side", "price"),
    [
        (10_011, True, -1, 10_010),  # above the ask: the informed trader buys at the ask, the maker sells
        (10_010, False, 0, None),  # equal to the ask: no trade
        (9_990, False, 0, None),  # equal to the bid: no trade
        (9_989, True, 1, 9_990),  # below the bid: the informed trader sells at the bid, the maker buys
    ],
)
def test_informed_trader_trades_only_strictly_outside_the_quote(
    monkeypatch: pytest.MonkeyPatch, fair: int, filled: bool, side: int, price: int | None
) -> None:
    """The informed rule on the first turn, at both sides of the quote and on each boundary: a trade needs a fair value
    strictly above the ask or strictly below the bid."""
    log = play_custom(monkeypatch, [fair] * (HORIZON + 1), ["informed"] * HORIZON, lambda state: (9_990, 10_010, 1))
    first = log["turns"][0]
    expect(
        first["filled"] is filled,
        "an informed trader trades only when the fair value is strictly outside the quote",
    )
    if filled:
        expect(first["fill_price_cents"] == price, "the informed trader trades at the quote on the side it prefers")
        expect(
            first["inventory_after"] == side,
            "the maker's inventory moves by one unit in the direction of the trade",
        )
