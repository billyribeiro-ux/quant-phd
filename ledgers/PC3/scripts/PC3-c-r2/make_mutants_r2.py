"""Round 2, slice c: write four new student-error mutants of the reference market_maker module (single change each).

Each mutant is the reference module (course grader/reference.py) with one change and a docstring whose first line names
the student error. Written into ledgers/PC3/mutants/. Run from the checkout root with the venv python.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path.cwd()
REF = (ROOT / "course/modules/PC/PC3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/PC3/mutants"

MUTANTS = {
    "v09_quote_warns_on_turn_one.py": (
        "Student error: quote calls warnings.warn on turn one, a debugging warning that the specification forbids "
        "(No function prints or warns).",
        [
            ("from typing import cast\n", "import warnings\nfrom typing import cast\n"),
            (
                '    mid = START_CENTS\n    for record in cast(list[dict[str, object]], state["history"]):',
                '    if not state["history"]:\n        warnings.warn("debug: first turn", stacklevel=2)\n'
                '    mid = START_CENTS\n    for record in cast(list[dict[str, object]], state["history"]):',
            ),
        ],
    ),
    "v10_replay_accepts_more_than_twenty_turns.py": (
        "Student error: replay refuses a log with fewer than 20 turns but accepts a log with more (the length check "
        "is one-sided).",
        [("    if len(turns) != HORIZON:\n", "    if len(turns) < HORIZON:\n")],
    ),
    "v11_replay_books_every_fill_at_the_bid.py": (
        "Student error: replay books the cash of every fill at the bid, so a sale at the ask is booked short by the spread.",
        [("        cash_flow += -side * price\n", "        cash_flow += -side * record[\"bid_cents\"]\n")],
    ),
    "v12_replay_skips_filled_turn_without_price.py": (
        "Student error: replay skips a filled turn that has no fill price instead of refusing it with the named "
        "ValueError.",
        [
            (
                '        if record["fill_price_cents"] is None:\n            raise ValueError("a filled turn needs a fill price")\n',
                '        if record["fill_price_cents"] is None:\n            continue\n',
            )
        ],
    ),
}


def main() -> None:
    for name, (doc, edits) in MUTANTS.items():
        text = REF
        for old, new in edits:
            assert text.count(old) == 1, (name, old)
            text = text.replace(old, new)
        first_doc_end = text.index('"""', text.index('"""') + 3) + 3
        header = f'"""{doc}\n\nExcluded from deployment (BLUEPRINT section 7): the suites are public, the reference solutions are not.\n"""'
        body = text[first_doc_end:]
        (OUT / name).write_text(header + body, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
