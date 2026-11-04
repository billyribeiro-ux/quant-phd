"""Write the verifier's own student-error mutants of the PC3 reference solution (round 1, slice c).

Each mutant is the reference solution (course/modules/PC/PC3/grader/reference.py) with exactly one replacement.
The script asserts that each `old` string occurs exactly once, so every mutant is a single, reviewable change.
Run from the checkout root:  .venv/bin/python ledgers/PC3/scripts/PC3-c-r1/make_verifier_mutants.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REFERENCE = ROOT / "course/modules/PC/PC3/grader/reference.py"
OUT = ROOT / "ledgers/PC3/mutants"

# (file name, first docstring line, old text, new text)
MUTANTS: list[tuple[str, str, str, str]] = [
    (
        "v01_quote_swaps_bid_and_ask_after_a_fill.py",
        "Student error: after the first fill the bid and the ask are swapped, so every later quote is crossed.",
        "    return mid - HALF_SPREAD, mid + HALF_SPREAD, SIZE\n",
        "    if mid == START_CENTS:\n"
        "        return mid - HALF_SPREAD, mid + HALF_SPREAD, SIZE\n"
        "    return mid + HALF_SPREAD, mid - HALF_SPREAD, SIZE\n",
    ),
    (
        "v02_quote_size_by_true_division.py",
        "Student error: the quoted size uses true division, so it is the float 1.0 and not the integer 1.",
        "    return mid - HALF_SPREAD, mid + HALF_SPREAD, SIZE\n",
        "    return mid - HALF_SPREAD, mid + HALF_SPREAD, SIZE / 1\n",
    ),
    (
        "v03_replay_marks_at_last_fill_price.py",
        "Student error: the inventory is marked at the price of the last fill, not at the settlement value.",
        "    mark = inventory * settlement\n",
        "    last_prices = [record['fill_price_cents'] for record in turns if record['filled'] is True]\n"
        "    mark = inventory * (int(last_prices[-1]) if last_prices else settlement)\n",
    ),
    (
        "v04_replay_copies_last_running_totals.py",
        "Student error: replay copies the last turn's running cash and inventory instead of summing the fills.",
        "    mark = inventory * settlement\n    return {\n",
        "    cash_flow = int(turns[-1]['cash_after_cents'])\n"
        "    inventory = int(turns[-1]['inventory_after'])\n"
        "    mark = inventory * settlement\n    return {\n",
    ),
    (
        "v05_replay_side_from_arrival_name.py",
        "Student error: replay takes the side of each fill from the arrival name, so an informed sale is booked as a buy.",
        '        side = -1 if price == record["ask_cents"] else 1  # -1: the maker sold at the ask; +1: it bought at the bid\n',
        "        side = -1 if record['arrival'] == 'uninformed-buy' else 1\n",
    ),
    (
        "v06_replay_mark_by_true_division.py",
        "Student error: the inventory mark uses true division, so it is a float and not an integer number of cents.",
        "    mark = inventory * settlement\n",
        "    mark = inventory * settlement / 1\n",
    ),
    (
        "v07_replay_int_of_none_not_refused.py",
        "Student error: a filled turn with no fill price crashes with a TypeError instead of the named ValueError.",
        '        if record["fill_price_cents"] is None:\n'
        '            raise ValueError("a filled turn needs a fill price")\n'
        '        price = cast(int, record["fill_price_cents"])\n',
        "        price = int(record['fill_price_cents'])\n",
    ),
    (
        "v08_replay_leaves_a_debug_print.py",
        "Student error: a debugging print is left in replay, so the function prints while it runs (the spec says no function prints).",
        "    mark = inventory * settlement\n",
        "    mark = inventory * settlement\n    print('replay done', cash_flow, inventory)\n",
    ),
]


def main() -> None:
    source = REFERENCE.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    for name, description, old, new in MUTANTS:
        count = source.count(old)
        if count != 1:
            raise SystemExit(f"{name}: the target text occurs {count} times, expected exactly once")
        text = source.replace(old, new, 1)
        text = text.replace(source.splitlines()[0], f'"""{description}', 1)
        target = OUT / name
        target.write_text(text, encoding="utf-8")
        print(f"wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
