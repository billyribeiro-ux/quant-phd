"""Independent recomputation of every number the PC3 project page states (round 1, slice c).

Written apart from the page's labs and the grader's reference. It derives the game from the rules in the page's
Conventions (draws: for each turn one move draw, then one arrival draw from random.Random(seed)), then checks:

1. the seed-0 game of Lab 1 (9 fills, cash flow, inventory, mark, P&L, largest |inventory|) and of Lab 3
   (counterfactual half-spread 15: fills, P&L, change);
2. the rung-2 interpretation claim: marking the ending inventory at the last quote's mid gives a different P&L;
3. that grader/instance.py make_instance(seed) equals the game the labs draw, for seeds 0..49;
4. the exemplars' cited values (Exemplar B: purchases 49910, sales 39960, cash flow -9950);
5. the Rung-3 Exemplar A/B statements that cite turns.

Usage (from the checkout root): .venv/bin/python -I ledgers/PC3/scripts/PC3-c-r1/recompute_project_numbers.py
(The -I flag keeps the script's directory off sys.path; the grader is loaded by path below.)
"""

from __future__ import annotations

import importlib.util
import random
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
INSTANCE_PATH = ROOT / "course/modules/PC/PC3/grader/instance.py"

START = 10_000
MOVE = 5
LIMIT = 10
HORIZON = 20


def game(seed: int, half_spread: int) -> dict[str, object]:
    """Independent game: move draw, then arrival draw, per turn. Maker at the bid buys, at the ask sells."""
    rng = random.Random(seed)
    fair = [START]
    arrivals: list[str] = []
    for _ in range(HORIZON):
        fair.append(fair[-1] + (MOVE if rng.random() < Fraction(1, 2) else -MOVE))
        u = rng.random()
        arrivals.append("uninformed-buy" if u < 0.25 else "uninformed-sell" if u < 0.5 else "informed")
    inventory = 0
    cash = 0
    last_fill: int | None = None
    fills: list[tuple[int, int]] = []  # (side, price): side -1 maker sold at ask, +1 maker bought at bid
    fill_turns: list[int] = []
    quotes: list[tuple[int, int]] = []
    inv_path: list[int] = []
    for t in range(1, HORIZON + 1):
        mid = START if last_fill is None else last_fill
        bid, ask = mid - half_spread, mid + half_spread
        quotes.append((bid, ask))
        arr = arrivals[t - 1]
        if arr == "uninformed-buy":
            side = -1
        elif arr == "uninformed-sell":
            side = 1
        elif fair[t] > ask:
            side = -1
        elif fair[t] < bid:
            side = 1
        else:
            side = 0
        if side != 0 and abs(inventory + side) <= LIMIT:
            price = ask if side < 0 else bid
            fills.append((side, price))
            fill_turns.append(t)
            inventory += side
            cash += -side * price
            last_fill = price
        inv_path.append(inventory)
    return {
        "fair": fair,
        "arrivals": arrivals,
        "fills": fills,
        "cash": cash,
        "inventory": inventory,
        "settlement": fair[HORIZON],
        "quotes": quotes,
        "inv_path": inv_path,
        "fill_turns": fill_turns,
    }


def lab_draws(seed: int) -> tuple[list[int], list[str]]:
    """The draw order of the lab twins (draw_game), copied here for the comparison in check 3."""
    rng = random.Random(seed)
    path = [START]
    arrivals: list[str] = []
    for _ in range(HORIZON):
        move = MOVE if rng.random() < 0.5 else -MOVE
        path.append(path[-1] + move)
        draw = rng.random()
        if draw < 0.25:
            arrivals.append("uninformed-buy")
        elif draw < 0.5:
            arrivals.append("uninformed-sell")
        else:
            arrivals.append("informed")
    return path, arrivals


def load_instance():  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location("pc3c_instance", INSTANCE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    ref = game(0, 10)
    print(f"check1 Lab1 seed0 fills={len(ref['fills'])} cash={ref['cash']} inventory={ref['inventory']} "
          f"settlement={ref['settlement']} mark={ref['inventory'] * ref['settlement']} "  # type: ignore[operator]
          f"pnl={ref['cash'] + ref['inventory'] * ref['settlement']} "  # type: ignore[operator]
          f"largest|inv|={max(abs(x) for x in ref['inv_path'])}")  # type: ignore[union-attr]
    wide = game(0, 15)
    wide_pnl = wide["cash"] + wide["inventory"] * wide["settlement"]  # type: ignore[operator]
    ref_pnl = ref["cash"] + ref["inventory"] * ref["settlement"]  # type: ignore[operator]
    print(f"check1 Lab3 counterfactual half-spread 15: fills={len(wide['fills'])} pnl={wide_pnl} "  # type: ignore[arg-type]
          f"change={wide_pnl - ref_pnl}")  # type: ignore[operator]

    last_quote_mid = sum(ref["quotes"][-1]) // 2  # type: ignore[index]
    at_mid_pnl = ref["cash"] + ref["inventory"] * last_quote_mid  # type: ignore[operator]
    print(f"check2 last quote (turn 20) bid,ask={ref['quotes'][-1]} mid={last_quote_mid} "  # type: ignore[index]
          f"P&L if marked at that mid={at_mid_pnl} vs settlement P&L={ref_pnl}")

    module = load_instance()
    mismatches = []
    for seed in range(50):
        path, arrivals = lab_draws(seed)
        inst = module.make_instance(seed)
        if inst["fair_path_cents"] != path or inst["arrivals"] != arrivals:
            mismatches.append(seed)
        g = game(seed, 10)
        if g["fair"] != path or g["arrivals"] != arrivals:
            mismatches.append(("independent", seed))
    print(f"check3 make_instance vs lab draw order, seeds 0..49: mismatches={mismatches}")

    buys = [price for side, price in ref["fills"] if side == 1]  # type: ignore[union-attr]
    sells = [price for side, price in ref["fills"] if side == -1]  # type: ignore[union-attr]
    print(f"check4 Exemplar B: maker purchases at bid={buys} total={sum(buys)}; "
          f"sales at ask={sells} total={sum(sells)}; cash flow={sum(sells) - sum(buys)}")

    print(f"check5 fill turns={ref['fill_turns']} (Exemplar B and Lab 1 list 2,3,4,5,7,8,13,18,19)")
    print(f"check5 quotes turn 18 bid,ask={ref['quotes'][17]}; turn 2 bid,ask={ref['quotes'][1]}; "  # type: ignore[index]
          f"turn 5 bid,ask={ref['quotes'][4]}")  # type: ignore[index]


if __name__ == "__main__":
    main()


def instance_spread() -> None:
    """Check 6: the reference answers differ across seeds 0..19 (not only the labels), per the BUILDER rule of 2.6."""
    pnls = []
    for seed in range(20):
        g = game(seed, 10)
        pnls.append((seed, g["cash"] + g["inventory"] * g["settlement"], len(g["fills"])))  # type: ignore[operator]
    distinct = len({p for _, p, _ in pnls})
    print(f"check6 reference P&L seeds 0..19: distinct P&L values={distinct} of 20; "
          f"sample={pnls[:6]}")


if __name__ == "__main__":
    instance_spread()
