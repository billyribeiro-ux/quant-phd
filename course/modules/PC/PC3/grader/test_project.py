"""Acceptance suite for the PC3 project: the quoting rule and the replay of a game log (market_maker.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your market_maker.py, engine.py and instance.py next to this file. Warnings are failures, as in the browser.

Each test checks a property or a number of the game defined in Lesson 4 and in the project specification. The checks
that depend on the seed run on the fixed seeds 0 to 49, on the learner's seed SEED and on seed SEED + 7919, so a fixed
answer for one seed must also match the others. Every expected value
is computed here, from the log's own fields and this file's own oracle, never from the student's module. A failing test
names the property it checks and the idea to revisit; it never prints the value the property should have.

A test expects an exception only for the conditions the specification names as invalid: a crossed or locked quote, a
size outside 0..5, a log that is not 20 turns long, and a filled turn with no fill price. Every other failure is a plain
property check.
"""

from __future__ import annotations

import importlib
import logging
import os
import warnings
from collections.abc import Callable
from typing import Any, cast

import engine
import market_maker as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
FIXED_SEEDS = tuple(range(50))
SEEDS = tuple(dict.fromkeys((*FIXED_SEEDS, SEED, SEED + 7_919)))
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


FILL_PRICES_CENTS = (9_980, 9_990, 10_000, 10_010, 10_020)


def fill_record(turn: int, price: int, at_ask: bool) -> dict[str, Any]:
    """A hand-built filled turn at ``price``: at the ask (a maker sale) or at the bid (a maker purchase), with the bid
    and the ask of that turn set so that the price is one of its quotes."""
    if at_ask:
        return turn_record(
            turn, bid=price - 20, ask=price, filled=True, arrival="uninformed-buy", price=price, inventory=0, cash=0
        )
    return turn_record(
        turn, bid=price, ask=price + 20, filled=True, arrival="uninformed-sell", price=price, inventory=0, cash=0
    )


def direct_states() -> list[dict[str, object]]:
    """The hand-built states of the direct sweep, at every inventory from -10 to 10. The first family has every turn
    from 1 to 20, and each state holds records of the same shape as the engine passes them: none on turn 1, and
    unfilled records for turns 1 to t-1 on turn t. The second family has every turn from 2 to 20, and each history
    holds unfilled records for turns 1 to t-2 and a fill on turn t-1, at each price of FILL_PRICES_CENTS and at the
    bid and at the ask, so every quote after a fill is checked."""
    states: list[dict[str, object]] = []
    for turn in range(1, HORIZON + 1):
        history = [turn_record(t, size=1, filled=False) for t in range(1, turn)]
        for inventory in range(-10, 11):
            states.append(_state(turn, inventory, history))
    for turn in range(2, HORIZON + 1):
        for price in FILL_PRICES_CENTS:
            for at_ask in (True, False):
                history = [turn_record(t, size=1, filled=False) for t in range(1, turn - 1)]
                history.append(fill_record(turn - 1, price, at_ask))
                for inventory in range(-10, 11):
                    states.append(_state(turn, inventory, history))
    return states


def _state(turn: int, inventory: int, history: list[dict[str, Any]]) -> dict[str, object]:
    """A direct state with its own copy of the history."""
    return {
        "turn": turn,
        "inventory": inventory,
        "cash_cents": 0,
        "max_size": 5,
        "limit": 10,
        "history": list(history),
    }


def custom_instance(path: list[int], arrivals: list[str]) -> dict[str, Any]:
    """An instance the suite writes out in full, for the rules of the engine. It replaces make_instance in each test
    that calls play_custom."""
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


# Legality of the student's quote, on every turn of every seed in SEEDS.


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
        triple = cast(tuple[int, int, int], out)  # narrowed by the check above: a tuple of three values
        expect(
            all(type(x) is int for x in triple),
            "every value a quote returns must be an integer: cents for prices, units for size",
        )
        bid, ask, size = triple
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


def test_replay_sums_the_fills_not_the_running_totals() -> None:
    """A hand-built log: one sale at the ask on turn 1, then running totals that stay at zero cash and zero inventory
    on turns 2 to 20. The cash flow and the inventory must be the sums over the fills, not the last turn's totals."""
    turns = [turn_record(1, filled=True, arrival="uninformed-buy", price=10_010, inventory=-1, cash=10_010)]
    turns += [turn_record(t, size=0, inventory=0, cash=0) for t in range(2, HORIZON + 1)]
    log = hand_log(turns, 10_000)
    expect(
        sol.replay(log) == oracle(log),
        "the cash flow must be the sum of the fill cash flows, and the inventory the sum of the fills, "
        "not the running totals of the last turn",
    )


def test_stale_totals_on_the_last_filled_turn_are_not_used() -> None:
    """A hand-built log with two fills: a sale at the ask on turn 1 and a purchase at the bid on turn 3. The running
    totals recorded on turn 3 are wrong on purpose. The cash flow and the inventory must be the sums over the two fills,
    so the totals of the last filled turn are not the answer."""
    turns = [turn_record(1, filled=True, arrival="uninformed-buy", price=10_010, inventory=-1, cash=10_010)]
    turns += [turn_record(2, size=0, inventory=-1, cash=10_010)]
    turns += [turn_record(3, filled=True, arrival="uninformed-sell", price=9_990, inventory=5, cash=0)]
    turns += [turn_record(t, size=0, inventory=0, cash=20) for t in range(4, HORIZON + 1)]
    log = hand_log(turns, 10_000)
    expect(
        sol.replay(log) == oracle(log),
        "the cash flow and the inventory must be the sums over the fills, "
        "not the totals recorded on the last filled turn",
    )


def test_a_fill_is_one_unit_whatever_its_quoted_size() -> None:
    """A hand-built log: a sale at the ask on turn 1 quoted at size 3. A fill is one unit, so the cash flow is one ask
    and the inventory moves by one unit, not by the quoted size."""
    turns = [turn_record(1, size=3, filled=True, arrival="uninformed-buy", price=10_010, inventory=-1, cash=10_010)]
    turns += [turn_record(t, size=0, inventory=-1, cash=10_010) for t in range(2, HORIZON + 1)]
    log = hand_log(turns, 10_000)
    expect(
        sol.replay(log) == oracle(log),
        "a fill is one unit: the cash flow and the inventory of a fill must not scale with the quoted size",
    )


def test_a_fill_at_price_zero_is_a_legal_fill() -> None:
    """A hand-built log: a purchase at the bid of 0 cents on turn 1. Zero is a whole number of cents, and the only
    named refusal is a fill price of None, so the fill is counted."""
    turns = [turn_record(1, bid=0, ask=10, filled=True, arrival="uninformed-sell", price=0, inventory=1, cash=0)]
    turns += [turn_record(t, bid=0, ask=10, size=0, inventory=1, cash=0) for t in range(2, HORIZON + 1)]
    log = hand_log(turns, 10_000)
    expect(
        sol.replay(log) == oracle(log),
        "a fill at price 0 is a legal fill: it must be counted, with the inventory and the mark it implies",
    )


def test_a_fill_at_any_integer_cent_price_is_booked_exactly() -> None:
    """A hand-built log with two fills at prices that are not multiples of 10 cents: a sale at the ask of 10005 on
    turn 1 and a purchase at the bid of 10003 on turn 2. Money is an integer number of cents, so each fill is booked at
    its own price, with no rounding, and the cash flow is 10005 - 10003 = 2 cents."""
    turns = [
        turn_record(
            1, bid=9_995, ask=10_005, filled=True, arrival="uninformed-buy", price=10_005, inventory=-1, cash=10_005
        )
    ]
    turns += [
        turn_record(
            2, bid=10_003, ask=10_013, filled=True, arrival="uninformed-sell", price=10_003, inventory=0, cash=2
        )
    ]
    turns += [turn_record(t, size=0, inventory=0, cash=2) for t in range(3, HORIZON + 1)]
    log = hand_log(turns, 10_003)
    expect(
        sol.replay(log) == oracle(log),
        "each fill is booked at its own integer cent price, and the cash flow is the sum of the fill cash flows",
    )


def test_a_log_with_no_fill_replays_to_zero() -> None:
    """A hand-built log in which no turn is filled: no cash moves and no inventory is held. No named condition covers
    it, so replay must return zero cash flow, zero inventory, zero mark and zero P&L, without raising."""
    turns = [turn_record(t, size=1, filled=False, inventory=0, cash=0) for t in range(1, HORIZON + 1)]
    log = hand_log(turns, 10_000)
    expect(
        sol.replay(log) == oracle(log),
        "a log with no fill must replay to zero cash flow, zero ending inventory, zero mark and zero P&L",
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


@pytest.mark.parametrize("seed", SEEDS)
def test_no_function_prints_or_warns(
    seed: int, capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture
) -> None:
    """On every seed, the quote and the replay print nothing on stdout or stderr, log no record and raise no warning.
    The checks reach branches that a game of the fixed seeds never takes: a log with no fill, a fill at price 0, logs
    that end at inventory -10 and at inventory +10, and the quotes of the direct states (every turn and inventory, and
    the states after a fill). Each channel is checked on its own, because the specification forbids each of them."""
    caplog.set_level(logging.DEBUG)
    no_fill = hand_log([turn_record(t, size=1, filled=False) for t in range(1, HORIZON + 1)], 10_000)
    zero_fill = hand_log(
        [turn_record(1, bid=0, ask=10, filled=True, arrival="uninformed-sell", price=0, inventory=1, cash=0)]
        + [turn_record(t, bid=0, ask=10, size=0, inventory=1, cash=0) for t in range(2, HORIZON + 1)],
        10_000,
    )
    ends_at_minus_ten = hand_log(
        [
            turn_record(t, filled=True, arrival="uninformed-buy", price=10_010, inventory=-t, cash=10_010 * t)
            for t in range(1, 11)
        ]
        + [turn_record(t, size=0, inventory=-10, cash=100_100) for t in range(11, HORIZON + 1)],
        10_000,
    )
    ends_at_plus_ten = hand_log(
        [
            turn_record(t, filled=True, arrival="uninformed-sell", price=9_990, inventory=t, cash=-9_990 * t)
            for t in range(1, 11)
        ]
        + [turn_record(t, size=0, inventory=10, cash=-99_900) for t in range(11, HORIZON + 1)],
        10_000,
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        log = engine.play(sol.quote, seed)
        for built in (log, no_fill, zero_fill, ends_at_minus_ten, ends_at_plus_ten):
            sol.replay(built)
        for state in direct_states():
            sol.quote(state)
    captured = capsys.readouterr()
    expect(captured.out == "" and captured.err == "", "neither quote nor replay may print or write to stderr")
    expect(not caplog.records, "neither quote nor replay may log a message")
    expect(not caught, "neither quote nor replay may warn")


def test_the_quote_depends_only_on_the_state_it_is_given() -> None:
    """Playing another game between two games on SEED must not change the second log. The module is reloaded before
    the first game, so a value kept at module level by an earlier test or game is cleared, and again before the other
    game, so the first log is played from a fresh module. A quote that keeps a value between calls, for example the
    last fill in a module global or the mid of each turn in a module dict, starts the second game from the state the
    other game left, so the two logs differ."""
    other = next(seed for seed in FIXED_SEEDS if seed != SEED)
    importlib.reload(sol)
    alone = engine.play(sol.quote, SEED)
    importlib.reload(sol)
    engine.play(sol.quote, other)
    after = engine.play(sol.quote, SEED)
    expect(
        alone == after,
        "a quote must depend only on the state it is given: after another game, the same seed must give the same log",
    )


def test_a_direct_call_on_a_hand_built_state_ignores_an_earlier_game() -> None:
    """A direct call on a hand-built state; the engine plays one other game in between. The state is at turn 5: the
    history holds a fill at 10020 on turn 2 and no fill on turns 3 and 4, so a quote that reads only the last turn
    record (turn 4) has no fill to read. The module is reloaded and the state is quoted on the fresh module; then one
    other game is played and the same state is quoted again. A quote that keeps a value between calls, for example the
    last fill in a module global, answers the second time from what that game left, so the two answers differ."""
    history = [
        turn_record(1, bid=9_990, ask=10_010, size=1, inventory=0, cash=0),
        turn_record(
            2, bid=10_010, ask=10_020, filled=True, arrival="uninformed-buy", price=10_020, inventory=-1, cash=10_020
        ),
        turn_record(3, bid=10_010, ask=10_030, size=1, inventory=-1, cash=10_020),
        turn_record(4, bid=10_010, ask=10_030, size=1, inventory=-1, cash=10_020),
    ]
    state: dict[str, object] = {
        "turn": 5,
        "inventory": -1,
        "cash_cents": 10_020,
        "max_size": 5,
        "limit": 10,
        "history": history,
    }
    importlib.reload(sol)
    fresh = sol.quote(state)
    engine.play(sol.quote, 0)  # a fixed game, whatever the learner's seed, leaves its own state in the module if any
    after = sol.quote(state)
    expect(
        fresh == after,
        "a quote on a given state must not depend on an earlier game: the same state must give the same quote",
    )


def test_a_direct_quote_is_legal_at_every_inventory_within_the_limit() -> None:
    """A direct call on hand-built states, on every turn from 1 to 20 (turn 1 with no earlier record, turn t with the
    unfilled records of turns 1 to t-1), at every inventory from -10 to 10, and on turns 2 to 20 with a fill on the
    turn before, at prices from 9980 to 10020 cents: each quote has its bid below its ask and its size in 0..5, whatever
    the inventory and whatever the last fill."""
    for state in direct_states():
        turn = state["turn"]
        inventory = state["inventory"]
        bid, ask, size = sol.quote(state)
        expect(bid < ask, f"turn {turn}, inventory {inventory}: every quote needs a bid below its ask")
        expect(0 <= size <= 5, f"turn {turn}, inventory {inventory}: a quoted size must lie in 0..5")


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


def test_fixed_seeds_0_to_49_give_fifty_different_paths() -> None:
    """The fair paths differ across the fixed seeds 0 to 49, so a policy tuned to one path does not pass every instance.
    The seeds are fixed, not the learner's, so the result is the same for every learner."""
    paths = {tuple(make_instance(s)["fair_path_cents"]) for s in range(50)}
    expect(len(paths) == 50, "fifty fixed seeds must give fifty different fair paths")


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
