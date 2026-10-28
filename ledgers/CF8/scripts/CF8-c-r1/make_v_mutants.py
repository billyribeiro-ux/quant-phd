"""Write the verifier's student-error mutants (CF8-c r1) from the reference engine, one changed line each.

Usage: .venv/bin/python ledgers/CF8/scripts/CF8-c-r1/make_v_mutants.py
Each mutant is the reference module with one replacement; every replacement must match exactly once.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course" / "modules" / "CF" / "CF8" / "grader" / "reference.py"
OUT = ROOT / "ledgers" / "CF8" / "mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "v01-dso-window-one-day-early": (
        "DSO shortening counts the window one day early: it moves in the sales of the day already collected at day 91 - lag.",
        [
            (
                "window = range(DAYS_PER_WEEK * HORIZON - lag + 1, DAYS_PER_WEEK * HORIZON - lag + days + 1)",
                "window = range(DAYS_PER_WEEK * HORIZON - lag, DAYS_PER_WEEK * HORIZON - lag + days)",
            )
        ],
    ),
    "v02-pinch-reports-liquidity-not-headroom": (
        "Covenant pinch reports the week's liquidity in place of its headroom, so the threshold is never subtracted.",
        [
            (
                'return {"week": best + 1, "headroom_cents": rows[best]["headroom_cents"]}',
                'return {"week": best + 1, "headroom_cents": rows[best]["liquidity_cents"]}',
            )
        ],
    ),
    "v03-required-commitment-is-capped-peak": (
        "Required commitment is read from the capped path (the peak drawn balance), not from the uncapped free path.",
        [
            (
                'required = max([case["opening_drawn_cents"]] + [row["drawn_balance_cents"] for row in uncapped])',
                'required = max([case["opening_drawn_cents"]] + [row["drawn_balance_cents"] for row in rows])',
            )
        ],
    ),
    "v04-no-pre-horizon-run-rate": (
        "Days before day 1 carry no sales or purchases, so lagged receipts in the first weeks are understated.",
        [
            (
                "    week = 1 if day < 1 else (day - 1) // DAYS_PER_WEEK + 1\n    return Fraction(weekly[week - 1], DAYS_PER_WEEK)",
                "    if day < 1:\n        return Fraction(0)\n    week = (day - 1) // DAYS_PER_WEEK + 1\n    return Fraction(weekly[week - 1], DAYS_PER_WEEK)",
            )
        ],
    ),
    "v05-daily-rounding-before-summing": (
        "Each day's amount is rounded to whole cents before the week is summed, so seven rounded days replace one exact week.",
        [
            (
                "    return sum((_daily_rate(weekly, day - lag_days) for day in range(first, first + DAYS_PER_WEEK)), Fraction(0))",
                "    return sum((Fraction(_half_up(_daily_rate(weekly, day - lag_days))) for day in range(first, first + DAYS_PER_WEEK)), Fraction(0))",
            )
        ],
    ),
}


def main() -> None:
    source = REF.read_text(encoding="utf-8")
    head, sep, rest = source.partition('"""')
    _, _, body = rest.partition('"""')
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
