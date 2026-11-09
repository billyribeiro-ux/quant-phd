"""Acceptance suite for the FC2 project: the arbitrage scanner (scanner.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your scanner.py next to this file. Warnings are failures, as in the browser.

Each test checks a property or a number against the definitions of the FC2 lessons and the project specification.
Money is integer cents and every money value is compared exactly. The specification fixes two tie rules, each applied
once to an exact value: a signed parity gap rounds a tie toward plus infinity, and a gross amount (the magnitude of the
gap) rounds a tie up in magnitude. A correct implementation therefore returns the same integers.
A failing test names the property it checks and never prints the value it expected.
"""

from __future__ import annotations

import ast
import copy
import itertools
import math
import os
import re
import sys
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
import scanner as sol
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
INST2: dict[str, Any] = make_instance(SEED + 7_919)  # a second chain: a fixed answer for one seed must match this too
PPM = 1_000_000
FINDING_KEYS = {"kind", "strike_cents", "gross_cents", "net_cents", "explanation"}
# The labels each kind of finding depends on, as the specification states them (the conventions, P1 to P6).
PARITY_LABELS = ("P1", "P2", "P3", "P4", "P6")
CONVEXITY_LABELS = ("P1", "P2", "P5", "P6")


def chain_of(inst: dict[str, Any]) -> dict[str, Any]:
    """The chain in the shape the specification defines, built from an instance's quotes."""
    return {
        "spot_cents": inst["spot_cents"],
        "df_ppm": inst["df_ppm"],
        "strikes_cents": list(inst["strikes_cents"]),
        "call_cents": list(inst["call_cents"]),
        "put_cents": list(inst["put_cents"]),
        "cost": {
            "fee_cents_per_contract": inst["fee_cents_per_contract"],
            "half_spread_cents": inst["half_spread_cents"],
        },
    }


def hand_chain(
    strikes: list[int],
    calls: list[int],
    puts: list[int],
    spot: int = 10_000,
    df: int = PPM,
    fee: int = 0,
    spread: int = 0,
) -> dict[str, Any]:
    """A chain written by hand, with the cost model given as two integers."""
    return {
        "spot_cents": spot,
        "df_ppm": df,
        "strikes_cents": strikes,
        "call_cents": calls,
        "put_cents": puts,
        "cost": {"fee_cents_per_contract": fee, "half_spread_cents": spread},
    }


def names_number(message: str, number: int) -> bool:
    """True when the message contains the integer as a standalone number (not a part of a longer one)."""
    return re.search(rf"(?<![\d.]){number}(?![\d.])", message) is not None


def names_df_range(message: str) -> bool:
    """True when the message names df_ppm and the upper bound 1000000, in any case, with or without commas."""
    return "df_ppm" in message.lower() and "1000000" in message.replace(",", "")


def oracle_round(x: Fraction) -> int:
    """The test's own rounding of an exact amount: floor(x + 1/2), a tie going toward plus infinity."""
    return math.floor(x + Fraction(1, 2))


def oracle_gap(call: int, put: int, spot: int, strike: int, df: int) -> Fraction:
    """C - P - (S - K df) as an exact fraction, with df = df_ppm / 1e6."""
    return Fraction(call) - Fraction(put) - (Fraction(spot) - Fraction(strike) * Fraction(df, PPM))


def oracle_convexity(strikes: list[int], calls: list[int]) -> list[int]:
    """Every interior index whose call lies strictly above the line through its two neighbours, at its own strike."""
    flagged = []
    for j in range(1, len(strikes) - 1):
        k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
        c0, c1, c2 = calls[j - 1], calls[j], calls[j + 1]
        line_at_k1 = Fraction(c0) + Fraction(c2 - c0) * Fraction(k1 - k0, k2 - k0)
        if Fraction(c1) > line_at_k1:
            flagged.append(j)
    return flagged


def oracle_findings(chain: dict[str, Any]) -> list[tuple[str, int, int, int]]:
    """The expected (kind, strike, gross, net) records of a chain, parity first by strike, then convexity."""
    strikes, calls, puts = chain["strikes_cents"], chain["call_cents"], chain["put_cents"]
    per_finding = 3 * (chain["cost"]["fee_cents_per_contract"] + chain["cost"]["half_spread_cents"])
    rows: list[tuple[str, int, int, int]] = []
    for k, strike in enumerate(strikes):
        gap = oracle_gap(calls[k], puts[k], chain["spot_cents"], strike, chain["df_ppm"])
        gross = oracle_round(abs(gap))
        if gross - per_finding > 0:
            rows.append(("parity", strike, gross, gross - per_finding))
    for j in oracle_convexity(strikes, calls):
        k0, k2 = strikes[j - 1], strikes[j + 1]
        line = Fraction(calls[j - 1]) + Fraction(calls[j + 1] - calls[j - 1]) * Fraction(strikes[j] - k0, k2 - k0)
        gross = oracle_round(Fraction(calls[j]) - line)
        if gross - per_finding > 0:
            rows.append(("convexity", strikes[j], gross, gross - per_finding))
    return rows


def rows_of(findings: list[dict[str, Any]]) -> list[tuple[str, int, int, int]]:
    return [(f["kind"], f["strike_cents"], f["gross_cents"], f["net_cents"]) for f in findings]


def consistent_chain(strikes: list[int], spot: int, df: int, calls: list[int]) -> dict[str, Any]:
    """A chain whose puts make every parity gap exactly zero. Strikes must make K df an integer number of cents."""
    puts = []
    for strike, call in zip(strikes, calls, strict=True):
        exact = Fraction(call) - Fraction(spot) + Fraction(strike * df, PPM)
        assert exact.denominator == 1, "the hand-built chain must have integer puts"
        puts.append(int(exact))
    return hand_chain(strikes, calls, puts, spot=spot, df=df, fee=10, spread=20)


# ---------------------------------------------------------------------------
# The module as a module: surface, purity, imports
# ---------------------------------------------------------------------------


def test_three_functions_are_defined() -> None:
    __tracebackhide__ = True
    for name in ("parity_gap_cents", "convexity_violations", "scan"):
        assert callable(getattr(sol, name, None)), f"scanner.py must define the function {name}"


def test_module_imports_standard_library_only() -> None:
    __tracebackhide__ = True
    source = Path(sol.__file__).read_text(encoding="utf-8")
    names: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module.split(".")[0])
    outside = {n for n in names if n not in sys.stdlib_module_names}
    assert not outside, "scanner.py may import the standard library only"


def test_module_does_not_import_grader_files() -> None:
    __tracebackhide__ = True
    source = Path(sol.__file__).read_text(encoding="utf-8")
    grader_names = {"instance", "reference", "test_project"}
    imported: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert not (imported & grader_names), "scanner.py must run on its own, without the grader's files"


def test_functions_do_not_print(capsys: pytest.CaptureFixture[str]) -> None:
    __tracebackhide__ = True
    sol.scan(chain_of(INST))
    sol.convexity_violations(INST["strikes_cents"], INST["call_cents"], INST["df_ppm"])
    sol.parity_gap_cents(10, 0, 10, 10, PPM)
    assert capsys.readouterr().out == "", "the functions must not print"


def test_scan_does_not_change_its_argument() -> None:
    __tracebackhide__ = True
    chain = chain_of(INST)
    before = copy.deepcopy(chain)
    sol.scan(chain)
    assert chain == before, "scan must not change the chain it is given"


def test_scan_is_repeatable_on_the_same_chain() -> None:
    __tracebackhide__ = True
    chain = chain_of(INST)
    first = sol.scan(chain)
    second = sol.scan(chain)
    assert rows_of(first) == rows_of(second), "scan must give the same findings on the same chain"


# ---------------------------------------------------------------------------
# Parity: the gap and its rounding
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("index", range(6))
def test_parity_gap_matches_exact_rounding_seed(index: int) -> None:
    __tracebackhide__ = True
    inst = INST
    got = sol.parity_gap_cents(
        inst["call_cents"][index],
        inst["put_cents"][index],
        inst["spot_cents"],
        inst["strikes_cents"][index],
        inst["df_ppm"],
    )
    want = oracle_round(
        oracle_gap(
            inst["call_cents"][index],
            inst["put_cents"][index],
            inst["spot_cents"],
            inst["strikes_cents"][index],
            inst["df_ppm"],
        )
    )
    assert got == want, "the parity gap must be the exact C - P - (S - K df), rounded once to whole cents"


@pytest.mark.parametrize("index", range(6))
def test_parity_gap_matches_exact_rounding_second_chain(index: int) -> None:
    __tracebackhide__ = True
    inst = INST2
    got = sol.parity_gap_cents(
        inst["call_cents"][index],
        inst["put_cents"][index],
        inst["spot_cents"],
        inst["strikes_cents"][index],
        inst["df_ppm"],
    )
    want = oracle_round(
        oracle_gap(
            inst["call_cents"][index],
            inst["put_cents"][index],
            inst["spot_cents"],
            inst["strikes_cents"][index],
            inst["df_ppm"],
        )
    )
    assert got == want, "the parity gap must be the exact C - P - (S - K df), rounded once to whole cents"


def test_parity_gap_returns_an_integer_not_a_bool() -> None:
    __tracebackhide__ = True
    value = sol.parity_gap_cents(100, 40, 70, 30, 990_000)
    assert type(value) is int, "the parity gap is an integer number of cents"


def test_parity_gap_with_zero_rate_is_c_minus_p_minus_s_plus_k() -> None:
    __tracebackhide__ = True
    assert sol.parity_gap_cents(1000, 300, 900, 200, PPM) == 0, "at df = 1 the gap is C - P - S + K"
    assert sol.parity_gap_cents(1001, 300, 900, 200, PPM) == 1, "at df = 1 the gap is C - P - S + K"
    assert sol.parity_gap_cents(1000, 301, 900, 200, PPM) == -1, "at df = 1 the gap is C - P - S + K"


def test_parity_tie_of_one_half_goes_up() -> None:
    __tracebackhide__ = True
    # gap = 11 - 0 - (10 - 3 * 0.5) = 2.5 exactly: an exact tie, which rounds up to 3
    assert sol.parity_gap_cents(11, 0, 10, 3, 500_000) == 3, "an exact tie of 2.5 cents must round up, not down"


def test_parity_negative_tie_of_one_half_goes_toward_plus_infinity() -> None:
    __tracebackhide__ = True
    assert sol.parity_gap_cents(0, 1, 2, 3, 500_000) == -1, "an exact tie of -1.5 cents must round toward plus infinity"
    assert sol.parity_gap_cents(0, 0, 2, 3, 500_000) == 0, (
        "an exact tie of -0.5 cents must round toward plus infinity, not away from it"
    )
    assert sol.parity_gap_cents(5, 0, 5, 3, 500_000) == 2, "an exact tie of 1.5 cents must round up, not down"


def test_parity_exact_tie_at_a_non_dyadic_discount_factor() -> None:
    __tracebackhide__ = True
    # df = 0.58 is not exact in binary floating point: gap = 0 - 0 - (0 - 25 * 0.58) = 14.5 exactly, rounds up
    assert sol.parity_gap_cents(0, 0, 0, 25, 580_000) == 15, "an exact tie of 14.5 cents must round up, not down"
    # gap = 0 - 29 - (0 - 14.5) = -14.5 exactly: the tie goes toward plus infinity, to -14
    assert sol.parity_gap_cents(0, 29, 0, 25, 580_000) == -14, "an exact tie of -14.5 cents must round toward +infinity"


def test_parity_gap_df_range_lower_boundary() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="df_ppm"):
        sol.parity_gap_cents(10, 0, 10, 10, 0)
    assert isinstance(sol.parity_gap_cents(10, 0, 10, 10, 1), int), "df_ppm = 1 is inside the range"


def test_parity_gap_rejects_a_negative_df() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="df_ppm"):
        sol.parity_gap_cents(10, 0, 10, 10, -1)


def test_parity_gap_df_range_upper_boundary() -> None:
    __tracebackhide__ = True
    assert isinstance(sol.parity_gap_cents(10, 0, 10, 10, PPM), int), "df_ppm = 1000000 is inside the range"
    with pytest.raises(ValueError, match="df_ppm"):
        sol.parity_gap_cents(10, 0, 10, 10, PPM + 1)


def test_parity_gap_rejects_a_nonpositive_strike_and_accepts_one() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="strictly increasing") as caught:
        sol.parity_gap_cents(10, 0, 10, 0, PPM)
    assert "positive" in str(caught.value).lower(), "the message names the positive-strike condition"
    with pytest.raises(ValueError, match="strictly increasing") as caught_negative:
        sol.parity_gap_cents(10, 0, 10, -5, PPM)
    assert "positive" in str(caught_negative.value).lower(), "the message names the positive-strike condition"
    assert isinstance(sol.parity_gap_cents(10, 0, 10, 1, PPM), int), "a strike of 1 cent is positive"


# ---------------------------------------------------------------------------
# Convexity in strike
# ---------------------------------------------------------------------------


def test_convexity_matches_exhaustive_oracle_seed() -> None:
    __tracebackhide__ = True
    got = sol.convexity_violations(INST["strikes_cents"], INST["call_cents"], INST["df_ppm"])
    assert got == oracle_convexity(INST["strikes_cents"], INST["call_cents"]), (
        "the list must hold every interior strike whose call lies above the chord of its neighbours"
    )


def test_convexity_matches_exhaustive_oracle_second_chain() -> None:
    __tracebackhide__ = True
    got = sol.convexity_violations(INST2["strikes_cents"], INST2["call_cents"], INST2["df_ppm"])
    assert got == oracle_convexity(INST2["strikes_cents"], INST2["call_cents"]), (
        "the list must hold every interior strike whose call lies above the chord of its neighbours"
    )


def test_planted_convexity_index_is_found() -> None:
    __tracebackhide__ = True
    if INST["planted_kind"] == "convexity":
        got = sol.convexity_violations(INST["strikes_cents"], INST["call_cents"], INST["df_ppm"])
        assert INST["planted_index"] in got, "the planted convexity violation at this strike must be listed"


def test_planted_convexity_index_is_found_second_chain() -> None:
    __tracebackhide__ = True
    if INST2["planted_kind"] == "convexity":
        got = sol.convexity_violations(INST2["strikes_cents"], INST2["call_cents"], INST2["df_ppm"])
        assert INST2["planted_index"] in got, "the planted convexity violation at this strike must be listed"


def test_clean_calls_give_no_convexity_violation() -> None:
    __tracebackhide__ = True
    if INST["planted_kind"] != "convexity":
        got = sol.convexity_violations(INST["strikes_cents"], INST["call_cents"], INST["df_ppm"])
        assert got == [], "a chain whose calls are convex in strike has no convexity violation"


def test_unequal_grid_violation_is_found() -> None:
    __tracebackhide__ = True
    # chord at strike 110 through (100, 50) and (150, 10): weights 0.8 and 0.2, value 42; the call 43 sits above it
    assert sol.convexity_violations([100, 110, 150], [50, 43, 10], PPM) == [1], (
        "the neighbours must be weighted by their distances to the middle strike, not by equal weights"
    )


def test_unequal_grid_no_false_positive() -> None:
    __tracebackhide__ = True
    # same strikes, call 41 is below the chord value 42, so the strike is not a violation
    assert sol.convexity_violations([100, 110, 150], [50, 41, 10], PPM) == [], (
        "a call below the chord of its neighbours, weighted by distance, is not a violation"
    )


def test_convexity_matches_oracle_on_an_uneven_grid() -> None:
    __tracebackhide__ = True
    # strike 110 is flagged (chord 42, call 43); 150 is not (chord 32.6, call 10); 160 is flagged (chord 65/7, call 30)
    strikes, calls = [100, 110, 150, 160, 220], [50, 43, 10, 30, 5]
    got = sol.convexity_violations(strikes, calls, PPM)
    assert got == oracle_convexity(strikes, calls) == [1, 3], (
        "every interior strike on an uneven grid is checked against the chord weighted by distance"
    )


def test_convexity_boundary_equal_to_chord_is_not_flagged() -> None:
    __tracebackhide__ = True
    assert sol.convexity_violations([100, 110, 120], [50, 30, 10], PPM) == [], (
        "a call exactly on the chord is not a violation"
    )


def test_convexity_boundary_one_cent_above_chord_is_flagged() -> None:
    __tracebackhide__ = True
    assert sol.convexity_violations([100, 110, 120], [50, 31, 10], PPM) == [1], (
        "a call one cent above the chord is a violation"
    )


def test_convexity_flags_the_last_interior_index() -> None:
    __tracebackhide__ = True
    # strike 3 sits between (2, 10) and (4, 1): the chord at strike 3 is 5.5, and the call 10 is above it
    assert sol.convexity_violations([1, 2, 3, 4], [10, 10, 10, 1], PPM) == [2], (
        "a violation at the last interior index must be reported"
    )
    # strike 2 sits between (1, 10) and (3, 10): the chord is 10, the call is on it, so index 1 is not flagged
    assert 1 not in sol.convexity_violations([1, 2, 3, 4], [10, 10, 10, 1], PPM), (
        "a call exactly on the chord is not flagged"
    )


def test_convexity_has_no_interior_index_for_short_chains() -> None:
    __tracebackhide__ = True
    assert sol.convexity_violations([100], [5], PPM) == [], "a one-strike chain has no interior strike"
    assert sol.convexity_violations([100, 110], [5, 4], PPM) == [], "a two-strike chain has no interior strike"


def test_convexity_does_not_depend_on_the_discount_factor() -> None:
    __tracebackhide__ = True
    strikes, calls = INST["strikes_cents"], INST["call_cents"]
    results = [sol.convexity_violations(strikes, calls, df) for df in (1, 500_000, PPM)]
    assert results[0] == results[1] == results[2], "quotes are present values, so the sign does not depend on df_ppm"


def test_convexity_returns_integer_indices() -> None:
    __tracebackhide__ = True
    got = sol.convexity_violations([100, 110, 150], [50, 43, 10], PPM)
    assert all(type(j) is int for j in got), "the indices are integers"


def test_convexity_does_not_change_its_inputs() -> None:
    __tracebackhide__ = True
    strikes, calls = [100, 110, 150], [50, 43, 10]
    sol.convexity_violations(strikes, calls, PPM)
    assert strikes == [100, 110, 150] and calls == [50, 43, 10], "convexity_violations must not change its inputs"


# ---------------------------------------------------------------------------
# Named conditions: each in both directions, with its message
# ---------------------------------------------------------------------------


def test_strikes_equal_neighbours_are_rejected_by_scan() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="strictly increasing"):
        sol.scan(hand_chain([100, 100, 110], [5, 5, 4], [1, 1, 1]))


def test_strikes_decreasing_are_rejected_by_scan_and_convexity() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="strictly increasing"):
        sol.scan(hand_chain([110, 100, 120], [5, 5, 4], [1, 1, 1]))
    with pytest.raises(ValueError, match="strictly increasing"):
        sol.convexity_violations([110, 100, 120], [5, 5, 4], PPM)


def test_shuffled_strikes_are_rejected_not_reordered() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="strictly increasing"):
        sol.convexity_violations([110, 100, 120, 130], [4, 9, 4, 1], PPM)


def test_strictly_increasing_strikes_are_accepted() -> None:
    __tracebackhide__ = True
    got = sol.scan(hand_chain([100, 101, 102], [5, 5, 5], [1, 1, 1]))
    assert isinstance(got, list), "strictly increasing strikes are valid input"
    assert sol.convexity_violations([100, 101, 102], [5, 5, 5], PPM) == [], "equal calls are on the chord"


def test_strike_zero_is_rejected_by_scan_and_convexity() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="strictly increasing") as caught_scan:
        sol.scan(hand_chain([0, 1, 2], [5, 5, 5], [1, 1, 1]))
    assert "positive" in str(caught_scan.value).lower(), "the scan message names the positive-strike condition"
    with pytest.raises(ValueError, match="strictly increasing") as caught_convexity:
        sol.convexity_violations([0, 1, 2], [5, 5, 5], PPM)
    assert "positive" in str(caught_convexity.value).lower(), "the convexity message names the positive condition"


def test_negative_strike_is_rejected_by_scan_and_convexity() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="strictly increasing") as caught_scan:
        sol.scan(hand_chain([-5, 1, 2], [5, 5, 5], [1, 1, 1]))
    assert "positive" in str(caught_scan.value).lower(), "the scan message names the positive-strike condition"
    with pytest.raises(ValueError, match="strictly increasing") as caught_convexity:
        sol.convexity_violations([-5, 1, 2], [5, 5, 5], PPM)
    assert "positive" in str(caught_convexity.value).lower(), "the convexity message names the positive condition"


def test_equal_strikes_are_rejected_by_convexity() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="strictly increasing"):
        sol.convexity_violations([100, 100, 110], [5, 5, 4], PPM)


def test_strike_one_cent_is_the_lowest_positive_strike_accepted() -> None:
    __tracebackhide__ = True
    assert sol.convexity_violations([1, 2, 3], [5, 5, 5], PPM) == [], "a strike of 1 cent is positive and valid"


@pytest.mark.parametrize("bad_df", [0, -1, PPM + 1])
def test_df_outside_range_is_rejected(bad_df: int) -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="df_ppm"):
        sol.scan(hand_chain([100, 110, 120], [5, 5, 5], [1, 1, 1], df=bad_df))
    with pytest.raises(ValueError, match="df_ppm"):
        sol.convexity_violations([100, 110, 120], [5, 5, 5], bad_df)


@pytest.mark.parametrize("bad_df", [0, -1, PPM + 1])
def test_df_message_names_df_ppm_and_the_range_in_each_function(bad_df: int) -> None:
    __tracebackhide__ = True
    attempts: list[Callable[[], object]] = [
        lambda: sol.parity_gap_cents(10, 0, 10, 10, bad_df),
        lambda: sol.convexity_violations([100, 110, 120], [5, 5, 5], bad_df),
        lambda: sol.scan(hand_chain([100, 110, 120], [5, 5, 5], [1, 1, 1], df=bad_df)),
    ]
    for attempt in attempts:
        with pytest.raises(ValueError) as caught:
            attempt()
        assert names_df_range(str(caught.value)), "the df_ppm message names df_ppm and the range 1 to 1000000"


@pytest.mark.parametrize("good_df", [1, PPM])
def test_df_at_the_range_ends_is_accepted(good_df: int) -> None:
    __tracebackhide__ = True
    assert isinstance(sol.scan(hand_chain([100, 110, 120], [5, 5, 5], [1, 1, 1], df=good_df)), list), (
        "df_ppm at the ends of 1..1000000 is valid"
    )
    assert sol.convexity_violations([100, 110, 120], [5, 5, 5], good_df) == []


def test_calls_shorter_than_strikes_is_rejected() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError):
        sol.scan(hand_chain([100, 110, 120], [5, 5], [1, 1, 1]))
    with pytest.raises(ValueError):
        sol.convexity_violations([100, 110, 120], [5, 5], PPM)


def test_puts_shorter_than_strikes_is_rejected() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError):
        sol.scan(hand_chain([100, 110, 120], [5, 5, 5], [1, 1]))


def test_calls_longer_than_strikes_is_rejected() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError):
        sol.scan(hand_chain([100, 110, 120], [5, 5, 5, 5], [1, 1, 1]))
    with pytest.raises(ValueError):
        sol.convexity_violations([100, 110, 120], [5, 5, 5, 5], PPM)


def test_puts_longer_than_strikes_is_rejected() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError):
        sol.scan(hand_chain([100, 110, 120], [5, 5, 5], [1, 1, 1, 1]))


def test_lengths_equal_is_accepted() -> None:
    __tracebackhide__ = True
    assert isinstance(sol.scan(hand_chain([100, 110, 120], [5, 5, 5], [1, 1, 1])), list), (
        "equal lengths are valid input"
    )


def test_length_message_names_both_lengths() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError) as caught:
        sol.scan(hand_chain([100, 110, 120], [5, 5], [1, 1, 1]))
    message = str(caught.value)
    assert names_number(message, 3) and names_number(message, 2), "the message must name the two lengths that differ"


def test_convexity_length_message_names_both_lengths() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError) as shorter:
        sol.convexity_violations([100, 110, 120], [5, 5], PPM)
    assert names_number(str(shorter.value), 3) and names_number(str(shorter.value), 2), (
        "the message must name the strike count and the call count when calls are short"
    )
    with pytest.raises(ValueError) as longer:
        sol.convexity_violations([100, 110, 120], [5, 5, 5, 5], PPM)
    assert names_number(str(longer.value), 3) and names_number(str(longer.value), 4), (
        "the message must name the strike count and the call count when calls are long"
    )


def test_negative_fee_is_rejected_and_zero_is_accepted() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="non-negative"):
        sol.scan(hand_chain([100], [5], [1], fee=-1))
    assert isinstance(sol.scan(hand_chain([100], [5], [1], fee=0)), list), "a fee of zero is valid"


def test_negative_half_spread_is_rejected_and_zero_is_accepted() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="non-negative"):
        sol.scan(hand_chain([100], [5], [1], spread=-1))
    assert isinstance(sol.scan(hand_chain([100], [5], [1], spread=0)), list), "a half-spread of zero is valid"


def test_negative_cost_is_rejected_even_when_no_finding_is_kept() -> None:
    __tracebackhide__ = True
    # gap 0, so the gross is 0 and the net is -9 at a fee of -1 and a half-spread of 4: no finding is kept,
    # and the cost terms are still checked
    with pytest.raises(ValueError, match="non-negative"):
        sol.scan(hand_chain([100], [0], [0], spot=100, df=PPM, fee=-1, spread=4))
    # the same chain with the half-spread negative and the fee zero or more
    with pytest.raises(ValueError, match="non-negative"):
        sol.scan(hand_chain([100], [0], [0], spot=100, df=PPM, fee=0, spread=-4))


def test_two_strike_chain_still_checks_df_and_strikes_for_convexity() -> None:
    __tracebackhide__ = True
    # a two-strike chain has no interior index, but the named conditions apply to its inputs all the same
    with pytest.raises(ValueError, match="df_ppm"):
        sol.convexity_violations([100, 110], [5, 5], 0)
    with pytest.raises(ValueError, match="df_ppm"):
        sol.convexity_violations([100, 110], [5, 5], PPM + 1)
    with pytest.raises(ValueError, match="strictly increasing"):
        sol.convexity_violations([110, 100], [5, 5], PPM)


def test_two_strike_chain_still_checks_the_call_count_for_convexity() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError):
        sol.convexity_violations([100, 110], [5], PPM)
    with pytest.raises(ValueError):
        sol.convexity_violations([100, 110], [5, 5, 5], PPM)


def test_one_strike_chain_checks_the_quote_lengths() -> None:
    __tracebackhide__ = True
    # one strike with two puts: the message names the lengths, so it names the two puts
    with pytest.raises(ValueError) as caught:
        sol.scan(hand_chain([100], [5], [0, 0]))
    assert "2" in str(caught.value), "the message must name the two puts"
    with pytest.raises(ValueError):
        sol.scan(hand_chain([100], [5, 5], [0]))


# ---------------------------------------------------------------------------
# scan: findings, the cost rule and the record contract
# ---------------------------------------------------------------------------


def test_scan_records_have_the_contract_keys_and_types() -> None:
    __tracebackhide__ = True
    findings = sol.scan(chain_of(INST))
    assert isinstance(findings, list), "scan returns a list"
    for record in findings:
        assert set(record) == FINDING_KEYS, "each finding has exactly the five keys of the contract"
        assert record["kind"] in ("parity", "convexity"), "kind is parity or convexity"
        for key in ("strike_cents", "gross_cents", "net_cents"):
            assert type(record[key]) is int, "every money value is an integer number of cents"


def test_scan_money_outputs_are_integers_on_second_chain() -> None:
    __tracebackhide__ = True
    for record in sol.scan(chain_of(INST2)):
        for key in ("strike_cents", "gross_cents", "net_cents"):
            assert type(record[key]) is int, "every money value is an integer number of cents"


def test_scan_explanations_are_nonempty_and_name_the_rule() -> None:
    __tracebackhide__ = True
    for inst in (INST, INST2):
        for record in sol.scan(chain_of(inst)):
            text = record["explanation"]
            assert isinstance(text, str) and text.strip(), "each finding needs an explanation"
            rule = "parity" if record["kind"] == "parity" else "convex"
            assert re.search(rf"\b{rule}", text, re.IGNORECASE), (
                "the explanation names the rule that the finding breaks"
            )
            labels = PARITY_LABELS if record["kind"] == "parity" else CONVEXITY_LABELS
            named = set(re.findall(r"\bP[1-6]\b", text))
            assert named == set(labels), "the explanation names exactly the assumptions its kind depends on"


def test_scan_matches_exhaustive_oracle_seed() -> None:
    __tracebackhide__ = True
    assert rows_of(sol.scan(chain_of(INST))) == oracle_findings(chain_of(INST)), (
        "the findings must be the exact parity and convexity findings whose net amount is positive"
    )


def test_scan_matches_exhaustive_oracle_second_chain() -> None:
    __tracebackhide__ = True
    assert rows_of(sol.scan(chain_of(INST2))) == oracle_findings(chain_of(INST2)), (
        "the findings must be the exact parity and convexity findings whose net amount is positive"
    )


def test_planted_parity_violation_is_found_with_its_planted_gross() -> None:
    __tracebackhide__ = True
    inst = INST
    if inst["planted_kind"] != "parity":
        return
    fee_and_spread = 3 * (inst["fee_cents_per_contract"] + inst["half_spread_cents"])
    rows = {(kind, strike): (gross, net) for kind, strike, gross, net in rows_of(sol.scan(chain_of(inst)))}
    key = ("parity", inst["strikes_cents"][inst["planted_index"]])
    if inst["planted_amount_cents"] - fee_and_spread > 0:
        assert key in rows, "a planted parity violation whose net amount is positive must be reported"
        assert rows[key][0] == inst["planted_amount_cents"], "the reported gross must be the planted amount"
    else:
        assert key not in rows, "a planted parity violation whose net amount is not positive must not be reported"


def test_planted_convexity_violation_is_found_with_its_planted_gross() -> None:
    __tracebackhide__ = True
    inst = INST2
    if inst["planted_kind"] != "convexity":
        return
    fee_and_spread = 3 * (inst["fee_cents_per_contract"] + inst["half_spread_cents"])
    rows = {(kind, strike): (gross, net) for kind, strike, gross, net in rows_of(sol.scan(chain_of(inst)))}
    key = ("convexity", inst["strikes_cents"][inst["planted_index"]])
    if inst["planted_amount_cents"] - fee_and_spread > 0:
        assert key in rows, "a planted convexity violation whose net amount is positive must be reported"
        assert rows[key][0] == inst["planted_amount_cents"], "the reported gross must be the planted amount"
    else:
        assert key not in rows, "a planted convexity violation whose net amount is not positive must not be reported"


def test_clean_chain_has_no_findings() -> None:
    __tracebackhide__ = True
    strikes = [9_000, 9_500, 10_000, 10_500, 11_000, 11_500]
    calls = [1_500, 1_100, 800, 600, 450, 350]
    chain = consistent_chain(strikes, 10_000, 990_000, calls)
    assert all(
        sol.parity_gap_cents(c, p, 10_000, k, 990_000) == 0
        for c, p, k in zip(calls, chain["put_cents"], strikes, strict=True)
    ), "the hand-built chain must have zero parity gaps"
    assert sol.scan(chain) == [], "a chain with zero parity gaps and convex calls has no findings"


def test_cost_is_charged_per_leg_not_once() -> None:
    __tracebackhide__ = True
    # per finding: 3 legs at fee 10 plus half-spread 20 = 90 cents. Gross 100 leaves net 10, not 100 minus 30.
    chain = hand_chain([100], [100], [0], spot=100, df=PPM, fee=10, spread=20)
    findings = sol.scan(chain)
    assert rows_of(findings) == [("parity", 100, 100, 10)], "each finding pays three legs of fee plus half-spread"


def test_finding_with_net_exactly_zero_is_not_returned() -> None:
    __tracebackhide__ = True
    # gross 45 equals 3 legs times (fee 10 + half-spread 5): net is 0, and only a strictly positive net is a finding
    chain = hand_chain([100], [45], [0], spot=100, df=PPM, fee=10, spread=5)
    assert sol.scan(chain) == [], "a finding whose net amount is exactly zero is not returned"


def test_finding_with_net_one_cent_is_returned() -> None:
    __tracebackhide__ = True
    chain = hand_chain([100], [46], [0], spot=100, df=PPM, fee=10, spread=5)
    assert rows_of(sol.scan(chain)) == [("parity", 100, 46, 1)], "a positive net amount is returned, however small"


def test_convexity_finding_with_net_exactly_zero_is_not_returned() -> None:
    __tracebackhide__ = True
    # chord at 110 = 30, call 75: chord less call = -45, gross 45 = 3 legs x (fee 10 + half-spread 5), net 0.
    # Parity is exact at every strike (put = call - spot + strike), so only the convexity finding is in play.
    chain = hand_chain([100, 110, 120], [50, 75, 10], [50, 85, 30], spot=100, df=PPM, fee=10, spread=5)
    assert sol.scan(chain) == [], "a convexity finding whose net amount is exactly zero is not returned"


def test_convexity_finding_with_net_one_cent_is_returned() -> None:
    __tracebackhide__ = True
    # the same chain with the middle call at 76: chord less call = -46, gross 46, net 1, and parity is still exact
    chain = hand_chain([100, 110, 120], [50, 76, 10], [50, 86, 30], spot=100, df=PPM, fee=10, spread=5)
    assert rows_of(sol.scan(chain)) == [("convexity", 110, 46, 1)], (
        "a convexity finding with a positive net amount is returned, however small"
    )


def test_negative_parity_gap_is_reported_with_positive_gross() -> None:
    __tracebackhide__ = True
    # gap = 0 - 45 - (100 - 100) = -45: the gross is 45, equal to the cost, so the net is 0 and nothing is returned
    chain = hand_chain([100], [0], [45], spot=100, df=PPM, fee=10, spread=5)
    assert sol.scan(chain) == [], "a gap whose gross equals the cost has net zero and is not returned"
    # gap = -46: the gross is 46 and the net is 1, returned with a positive gross whichever way the gap points
    chain_wide = hand_chain([100], [0], [46], spot=100, df=PPM, fee=10, spread=5)
    assert rows_of(sol.scan(chain_wide)) == [("parity", 100, 46, 1)], (
        "a put priced above the synthetic forward is a finding of the same size"
    )


def test_half_cent_gross_rounds_once_up() -> None:
    __tracebackhide__ = True
    # gap = 11 - 0 - (10 - 1.5) = 2.5 exactly: the gross is 3 cents, rounded once (not truncated to 2)
    chain = hand_chain([3], [11], [0], spot=10, df=500_000, fee=0, spread=0)
    assert rows_of(sol.scan(chain)) == [("parity", 3, 3, 3)], "an exact half-cent gross rounds up once"


def test_half_cent_tie_at_a_non_dyadic_discount_factor_rounds_once_up() -> None:
    __tracebackhide__ = True
    # df = 0.58: gap = 0 - 0 - (0 - 25 * 0.58) = 14.5 exactly, so the gross is 15 cents (a float computation gives 14)
    chain = hand_chain([25], [0], [0], spot=0, df=580_000, fee=0, spread=0)
    assert rows_of(sol.scan(chain)) == [("parity", 25, 15, 15)], "an exact 14.5-cent gross at df 0.58 rounds up once"


def test_convexity_half_cent_tie_rounds_once_up_at_any_discount_factor() -> None:
    __tracebackhide__ = True
    # the chord at 110 is (50 + 51) / 2 = 50.5 and the call is 53: the violation is exactly 2.5 cents, rounded up to 3.
    # Convexity uses no discounting, so df = 0.95 must not change the gross.
    chain = hand_chain([100, 110, 120], [50, 53, 51], [0, 0, 0], spot=0, df=950_000, fee=0, spread=0)
    convexity = [row for row in rows_of(sol.scan(chain)) if row[0] == "convexity"]
    assert convexity == [("convexity", 110, 3, 3)], "an exact 2.5-cent convexity violation rounds up once"


def test_negative_half_cent_gross_rounds_once_up_in_magnitude() -> None:
    __tracebackhide__ = True
    # gap = 6 - 0 - (10 - 1.5) = -2.5 exactly: the gross is the magnitude 2.5, rounded half up to 3
    chain = hand_chain([3], [6], [0], spot=10, df=500_000, fee=0, spread=0)
    assert rows_of(sol.scan(chain)) == [("parity", 3, 3, 3)], "the gross is the rounded magnitude of the gap"


def test_parity_findings_come_in_strike_order() -> None:
    __tracebackhide__ = True
    # spot 100 and df 1: the gap is C - P - (100 - K) = 50, 10 and 70 at strikes 100, 110 and 120; no convexity finding
    chain = hand_chain([100, 110, 120], [50, 5, 50], [0, 5, 0], spot=100, df=PPM, fee=0, spread=0)
    assert rows_of(sol.scan(chain)) == [("parity", 100, 50, 50), ("parity", 110, 10, 10), ("parity", 120, 70, 70)], (
        "parity findings are listed in increasing strike order"
    )


def test_convexity_findings_come_in_strike_order() -> None:
    __tracebackhide__ = True
    # two convexity violations, at 9500 (chord 1500, call 1700) and 10500 (chord 700, call 900); parity gaps are zero
    chain = consistent_chain([9_000, 9_500, 10_000, 10_500, 11_000], 10_000, PPM, [2_000, 1_700, 1_000, 900, 400])
    assert rows_of(sol.scan(chain)) == [("convexity", 9_500, 200, 110), ("convexity", 10_500, 200, 110)], (
        "convexity findings are listed in increasing strike order"
    )


def test_convexity_half_cent_gross_rounds_once_up() -> None:
    __tracebackhide__ = True
    # chord at 10100 = (5001 + 2700) / 2 = 3850.5; the call 3851 is half a cent above it, so the gross is 1 cent
    strikes, calls, puts = [10_000, 10_100, 10_200], [5_001, 3_851, 2_700], [5_001, 3_951, 2_900]
    chain = hand_chain(strikes, calls, puts, spot=10_000, df=PPM, fee=0, spread=0)
    assert rows_of(sol.scan(chain)) == [("convexity", 10_100, 1, 1)], (
        "an exact half-cent convexity gross rounds up once"
    )


def test_findings_are_in_parity_then_convexity_order() -> None:
    __tracebackhide__ = True
    chain = hand_chain([100, 110, 150], [50, 43, 10], [0, 0, 0], spot=10_000, df=PPM, fee=0, spread=0)
    kinds = [record["kind"] for record in sol.scan(chain)]
    assert kinds == sorted(kinds, key=lambda kind: kind != "parity"), (
        "parity findings come first, then convexity findings"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_one_strike_chain_scans_without_convexity() -> None:
    __tracebackhide__ = True
    chain = hand_chain([100], [60], [0], spot=100, df=PPM, fee=0, spread=0)
    assert rows_of(sol.scan(chain)) == [("parity", 100, 60, 60)], "one strike gives a parity finding only"


def test_zero_rate_parity_matches_on_the_seeded_chain() -> None:
    __tracebackhide__ = True
    inst = INST
    for k, strike in enumerate(inst["strikes_cents"]):
        got = sol.parity_gap_cents(inst["call_cents"][k], inst["put_cents"][k], inst["spot_cents"], strike, PPM)
        want = inst["call_cents"][k] - inst["put_cents"][k] - inst["spot_cents"] + strike
        assert got == want, "at df = 1 the parity gap is C - P - S + K, exactly"


def test_instance_is_labelled_simulated() -> None:
    __tracebackhide__ = True
    assert INST["label"] == "SIMULATED" and INST2["label"] == "SIMULATED", "every instance is labelled SIMULATED"


def test_generated_chains_satisfy_the_model_free_bounds_of_theorem_2_2() -> None:
    __tracebackhide__ = True
    half = Fraction(1, 2)
    for seed in range(50):
        inst = make_instance(seed)
        spot, df = inst["spot_cents"], inst["df_ppm"]
        for strike, call, put in zip(inst["strikes_cents"], inst["call_cents"], inst["put_cents"], strict=True):
            discounted = Fraction(strike * df, PPM)
            assert call <= spot + half, "a call is at most the spot"
            assert call >= max(spot - discounted, Fraction(0)) - half, (
                "a call is at least the spot less the discounted strike"
            )
            assert put >= -half, "a put is not negative"
            assert put <= discounted + half, "a put is at most the discounted strike"
            assert put >= max(discounted - spot, Fraction(0)) - half, (
                "a put is at least the discounted strike less the spot"
            )


def test_instance_chains_are_valid_under_the_contract() -> None:
    __tracebackhide__ = True
    for inst in (INST, INST2):
        strikes = inst["strikes_cents"]
        assert all(a < b for a, b in itertools.pairwise(strikes)), "the generated strikes are increasing"
        assert strikes[0] > 0 and 1 <= inst["df_ppm"] <= PPM, "the generated strikes and df_ppm are in range"
        assert inst["fee_cents_per_contract"] >= 0 and inst["half_spread_cents"] >= 0, "the cost terms are non-negative"
        assert len(inst["call_cents"]) == len(strikes) == len(inst["put_cents"]), "one quote per strike"
