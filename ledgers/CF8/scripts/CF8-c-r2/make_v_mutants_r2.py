"""Write the verifier's round-2 student-error mutants (CF8-c r2) from the reference engine, one changed span each.

Usage: .venv/bin/python ledgers/CF8/scripts/CF8-c-r2/make_v_mutants_r2.py
Each mutant is the reference module with one replacement; every replacement must match exactly once.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course" / "modules" / "CF" / "CF8" / "grader" / "reference.py"
OUT = ROOT / "ledgers" / "CF8" / "mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "v06-opex-paid-one-week-late": (
        "Opex is paid one week after its own week, so week w disburses the opex of week w - 1 (none in week 1).",
        [
            (
                '    return purchases + int(case["weekly_opex_cents"][week - 1])',
                '    return purchases + (int(case["weekly_opex_cents"][week - 2]) if week > 1 else 0)',
            )
        ],
    ),
    "v07-required-commitment-excludes-opening": (
        "Required commitment is the largest drawn balance on the free path, leaving out the opening balance.",
        [
            (
                '    required = max([case["opening_drawn_cents"]] + [row["drawn_balance_cents"] for row in uncapped])',
                '    required = max([0] + [row["drawn_balance_cents"] for row in uncapped])',
            )
        ],
    ),
    "v08-pinch-week-zero-based": (
        "Covenant pinch reports the week as a zero-based index, so the week is one less than the true week.",
        [
            (
                'return {"week": best + 1, "headroom_cents": rows[best]["headroom_cents"]}',
                'return {"week": best, "headroom_cents": rows[best]["headroom_cents"]}',
            )
        ],
    ),
    "v09-shortfall-summed-over-weeks": (
        "Shortfall is the sum of the weekly shortfalls below minimum cash, not the largest weekly shortfall.",
        [
            (
                'shortfall = max([0] + [max(0, minimum - row["ending_cash_cents"]) for row in rows])',
                'shortfall = sum([0] + [max(0, minimum - row["ending_cash_cents"]) for row in rows])',
            )
        ],
    ),
    "v10-pre-horizon-negative-index": (
        "Days before day 1 are mapped with Python's floor division and not clamped, so they index the weeks from the end.",
        [
            (
                "    week = 1 if day < 1 else (day - 1) // DAYS_PER_WEEK + 1\n    return Fraction(weekly[week - 1], DAYS_PER_WEEK)",
                "    week = (day - 1) // DAYS_PER_WEEK + 1\n    return Fraction(weekly[week - 1], DAYS_PER_WEEK)",
            )
        ],
    ),
}


def main() -> None:
    source = REF.read_text(encoding="utf-8")
    for name, (description, edits) in MUTANTS.items():
        text = source
        for old, new in edits:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{name}: pattern found {count} times: {old[:60]!r}")
            text = text.replace(old, new)
        text = text.replace('"""Reference solution', f'"""{description}\n\nReference solution', 1)
        (OUT / f"{name}.py").write_text(text, encoding="utf-8")
        print("wrote", OUT / f"{name}.py")


if __name__ == "__main__":
    main()
