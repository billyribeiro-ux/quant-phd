"""Acceptance test suite for MS2 project: Batch-auction counterfactual (counterfactual.py).

Dual-mode: runs identically in the browser (Pyodide) and locally:
    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error grader/test_project.py
"""

from __future__ import annotations

import importlib
import os
from collections.abc import Callable
from typing import Any

import pytest

sol: Any = importlib.import_module("counterfactual")
make_instance: Callable[[int], dict[str, Any]] = importlib.import_module("instance").make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
INST2 = make_instance(SEED + 9973)


def expect(condition: bool, hint: str) -> None:
    """Fail with a descriptive hint if condition is false."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(hint, pytrace=False)


def must_raise(call: Callable[[], object], condition: str, *, substring: str = "") -> None:
    """Check that call() raises ValueError with optional required substring."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError as err:
        if substring and substring not in str(err):
            pytest.fail(
                f"{condition}: ValueError message must contain '{substring}' (got: {err})",
                pytrace=False,
            )
        return
    except Exception as exc:
        pytest.fail(f"{condition}: expected ValueError, got {type(exc).__name__}: {exc}", pytrace=False)
    pytest.fail(f"{condition}: expected ValueError, none was raised", pytrace=False)


def _parse_ev(e: Any) -> tuple[float, str, float, int]:
    if isinstance(e, dict):
        return float(e["time"]), str(e["type"]), float(e.get("price_delta", 0.0)), int(e["size"])
    return float(e[0]), str(e[1]), float(e[2]), int(e[3])


def oracle_clob(
    events: list[Any],
    initial_price: float,
    half_spread: float,
    mm_latency: float,
    sniper_latencies: list[float],
) -> dict[str, Any]:
    """Independent oracle for continuous limit order book."""
    mid = float(initial_price)
    fastest = min(sniper_latencies)
    rents = 0.0
    count = 0
    vol = 0
    inv_vol = 0
    mm_cash = 0.0
    mm_inv = 0
    for e in events:
        _t, etype, delta, sz = _parse_ev(e)
        if etype == "jump":
            if fastest < mm_latency:
                if delta > half_spread:
                    p = mid + half_spread
                    new_m = mid + delta
                    r = (new_m - p) * sz
                    rents += r
                    count += 1
                    vol += sz
                    mm_cash += p * sz
                    mm_inv -= sz
                elif delta < -half_spread:
                    p = mid - half_spread
                    new_m = mid + delta
                    r = (p - new_m) * sz
                    rents += r
                    count += 1
                    vol += sz
                    mm_cash -= p * sz
                    mm_inv += sz
            mid += delta
        elif etype == "investor_buy":
            p = mid + half_spread
            mm_cash += p * sz
            mm_inv -= sz
            inv_vol += sz
        elif etype == "investor_sell":
            p = mid - half_spread
            mm_cash -= p * sz
            mm_inv += sz
            inv_vol += sz
    return {
        "rents": rents,
        "count": count,
        "vol": vol,
        "inv_vol": inv_vol,
        "mm_pnl": mm_cash + mm_inv * mid,
        "final_price": mid,
    }


def test_contract() -> None:
    """Verify solver exports required functions with correct signatures."""
    for name in ("simulate_continuous_book", "simulate_batch_auction", "run_counterfactual"):
        expect(hasattr(sol, name), f"counterfactual module must export {name}")
        expect(callable(getattr(sol, name)), f"{name} must be callable")


def test_input_validation() -> None:
    """Verify input validation and informative ValueError exceptions."""
    ev = INST["events"]
    p0 = INST["initial_price"]
    hs = INST["half_spread"]
    mml = INST["mm_latency"]
    snipers = INST["sniper_latencies"]

    must_raise(lambda: sol.simulate_continuous_book(ev, -10.0, hs, mml, snipers), "negative initial_price")
    must_raise(lambda: sol.simulate_continuous_book(ev, p0, -0.05, mml, snipers), "negative half_spread")
    must_raise(lambda: sol.simulate_continuous_book(ev, p0, hs, -1.0, snipers), "negative mm_latency")
    must_raise(lambda: sol.simulate_continuous_book(ev, p0, hs, mml, []), "empty sniper_latencies")
    must_raise(lambda: sol.simulate_continuous_book(ev, p0, hs, mml, [-0.5]), "negative sniper latency")
    must_raise(lambda: sol.simulate_continuous_book([], p0, hs, mml, snipers), "empty events")

    # Unsorted events should raise ValueError
    unsorted = [ev[1], ev[0], *list(ev[2:])]
    must_raise(lambda: sol.simulate_continuous_book(unsorted, p0, hs, mml, snipers), "unsorted events")

    must_raise(lambda: sol.simulate_batch_auction(ev, p0, hs, -10.0, mml, snipers), "negative batch_interval")


def test_continuous_simulation_properties() -> None:
    """Verify properties of continuous book simulation."""
    res = sol.simulate_continuous_book(
        INST["events"],
        INST["initial_price"],
        INST["half_spread"],
        INST["mm_latency"],
        INST["sniper_latencies"],
    )
    for key in (
        "trades",
        "trade_count",
        "latency_arbitrage_count",
        "latency_arbitrage_volume",
        "latency_arbitrage_rents",
        "investor_volume",
        "mm_pnl",
        "investor_pnl",
        "final_price",
    ):
        expect(key in res, f"simulate_continuous_book missing return key '{key}'")

    expect(res["trade_count"] == len(res["trades"]), "trade_count must equal len(trades)")
    expect(res["latency_arbitrage_rents"] >= 0.0, "latency arbitrage rents must be non-negative")
    expect(res["latency_arbitrage_volume"] >= 0, "latency arbitrage volume must be non-negative")
    expect(
        res["trade_count"] == res["latency_arbitrage_volume"] + res["investor_volume"],
        "total trades must equal latency arbitrage volume plus investor volume",
    )


def test_batch_auction_properties() -> None:
    """Verify key invariance: frequent batch auction completely eliminates latency arbitrage."""
    res = sol.simulate_batch_auction(
        INST["events"],
        INST["initial_price"],
        INST["half_spread"],
        INST["batch_interval"],
        INST["mm_latency"],
        INST["sniper_latencies"],
    )
    for key in (
        "trades",
        "trade_count",
        "latency_arbitrage_count",
        "latency_arbitrage_volume",
        "latency_arbitrage_rents",
        "investor_volume",
        "spread_savings",
        "mm_pnl",
        "investor_pnl",
        "final_price",
    ):
        expect(key in res, f"simulate_batch_auction missing return key '{key}'")

    # The defining theorem of Budish, Cramton & Shim (2015):
    expect(
        res["latency_arbitrage_rents"] == 0.0,
        "frequent batch auctions must have zero latency arbitrage rents",
    )
    expect(
        res["latency_arbitrage_count"] == 0,
        "frequent batch auctions must have zero latency arbitrage trades",
    )
    expect(
        res["latency_arbitrage_volume"] == 0,
        "frequent batch auctions must have zero latency arbitrage volume",
    )
    expect(res["spread_savings"] >= 0.0, "spread savings from multilateral crossing must be non-negative")


def test_oracle_agreement() -> None:
    """Verify numerical results match oracle calculation within tolerance."""
    oracle = oracle_clob(
        INST["events"],
        INST["initial_price"],
        INST["half_spread"],
        INST["mm_latency"],
        INST["sniper_latencies"],
    )
    res = sol.simulate_continuous_book(
        INST["events"],
        INST["initial_price"],
        INST["half_spread"],
        INST["mm_latency"],
        INST["sniper_latencies"],
    )

    expect(
        abs(res["latency_arbitrage_rents"] - oracle["rents"]) < 1e-4,
        f"latency arbitrage rents mismatch: solver={res['latency_arbitrage_rents']}, oracle={oracle['rents']}",
    )
    expect(
        res["latency_arbitrage_count"] == oracle["count"],
        f"arbitrage trade count mismatch: solver={res['latency_arbitrage_count']}, oracle={oracle['count']}",
    )
    expect(
        abs(res["final_price"] - oracle["final_price"]) < 1e-4,
        f"final mid-price mismatch: solver={res['final_price']}, oracle={oracle['final_price']}",
    )
    expect(
        abs(res["mm_pnl"] - oracle["mm_pnl"]) < 1e-4,
        f"market maker PnL mismatch: solver={res['mm_pnl']}, oracle={oracle['mm_pnl']}",
    )


def test_counterfactual_summary() -> None:
    """Verify run_counterfactual compares continuous and batch auctions across intervals."""
    cf = sol.run_counterfactual(
        INST["events"],
        INST["initial_price"],
        INST["half_spread"],
        INST["batch_intervals"],
        INST["mm_latency"],
        INST["sniper_latencies"],
    )
    expect("continuous" in cf, "counterfactual must contain 'continuous'")
    expect("batch_auctions" in cf, "counterfactual must contain 'batch_auctions'")
    expect("rent_savings" in cf, "counterfactual must contain 'rent_savings'")

    expect(
        abs(cf["rent_savings"] - cf["continuous"]["latency_arbitrage_rents"]) < 1e-5,
        "rent_savings must equal continuous latency arbitrage rents",
    )
    for delta in INST["batch_intervals"]:
        key = f"delta_{delta:g}"
        expect(key in cf["batch_auctions"], f"missing batch auction result for {key}")
        expect(
            cf["batch_auctions"][key]["latency_arbitrage_rents"] == 0.0,
            f"batch auction {key} must have zero latency rents",
        )


def test_edge_case_slow_snipers() -> None:
    """When snipers are slower than MM, continuous trading has zero latency arbitrage."""
    slow_snipers = [INST["mm_latency"] + 1.0, INST["mm_latency"] + 2.0]
    res = sol.simulate_continuous_book(
        INST["events"],
        INST["initial_price"],
        INST["half_spread"],
        INST["mm_latency"],
        slow_snipers,
    )
    expect(
        res["latency_arbitrage_rents"] == 0.0,
        "slow snipers must earn zero latency arbitrage rents",
    )
    expect(
        res["latency_arbitrage_count"] == 0,
        "slow snipers must generate zero arbitrage trades",
    )


def test_edge_case_small_jumps() -> None:
    """When price jumps are strictly smaller than half-spread, no quote sniping occurs."""
    events = [
        (1.0, "jump", 0.01, 1),
        (2.0, "jump", -0.01, 1),
    ]
    res = sol.simulate_continuous_book(
        events,
        100.0,
        0.05,  # half-spread > jump size
        2.0,
        [0.5],
    )
    expect(
        res["latency_arbitrage_rents"] == 0.0,
        "jumps smaller than half-spread cannot be sniped profitably",
    )
    expect(res["latency_arbitrage_count"] == 0, "no snipe trades should execute")


def test_second_instance() -> None:
    """Verify correctness on second deterministic instance."""
    cf = sol.run_counterfactual(
        INST2["events"],
        INST2["initial_price"],
        INST2["half_spread"],
        INST2["batch_intervals"],
        INST2["mm_latency"],
        INST2["sniper_latencies"],
    )
    expect(cf["rent_savings"] >= 0.0, "rent savings must be non-negative on INST2")
    for key, fba in cf["batch_auctions"].items():
        expect(fba["latency_arbitrage_rents"] == 0.0, f"rents in {key} must be zero")
