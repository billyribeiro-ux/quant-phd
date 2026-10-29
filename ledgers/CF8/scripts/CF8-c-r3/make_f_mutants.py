"""Write the fixer's own ten student-error mutants (CF8-c, round 3) from the reference engine, one changed span each.

Each mutant is an error a student could make in a named condition or boundary of the specification (horizon, commitment,
action name, DSO and DPO windows, availability, shortfall, run-rate). Every replacement must match exactly once.

Usage: .venv/bin/python ledgers/CF8/scripts/CF8-c-r3/make_f_mutants.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course" / "modules" / "CF" / "CF8" / "grader" / "reference.py"
OUT = ROOT / "ledgers" / "CF8" / "mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "f01-horizon-rejects-only-above-13": (
        "The horizon check rejects only a horizon above 13, so a 12-week or 0-week case is accepted.",
        [('    if case["horizon_weeks"] != HORIZON:', '    if case["horizon_weeks"] > HORIZON:')],
    ),
    "f02-horizon-rejects-only-below-13": (
        "The horizon check rejects only a horizon below 13, so a 14-week case is accepted.",
        [('    if case["horizon_weeks"] != HORIZON:', '    if case["horizon_weeks"] < HORIZON:')],
    ),
    "f03-zero-commitment-rejected": (
        "The commitment check rejects zero as well as negative values, so a zero commitment raises.",
        [('    if case["revolver_commitment_cents"] < 0:', '    if case["revolver_commitment_cents"] <= 0:')],
    ),
    "f04-minus-one-cent-commitment-accepted": (
        "The commitment check rejects only commitments below minus one cent, so a minus-one-cent commitment is accepted.",
        [('    if case["revolver_commitment_cents"] < 0:', '    if case["revolver_commitment_cents"] < -1:')],
    ),
    "f05-action-name-case-folded": (
        "The action is lower-cased before the check, so the upper-case name DSO is accepted.",
        [('    if action == "dso":', '    action = action.lower()\n    if action == "dso":')],
    ),
    "f06-any-non-dso-action-is-dpo": (
        "Any action other than dso is treated as dpo, so the name dio returns a DPO impact and no error is raised.",
        [('    if action == "dpo":', '    if action != "dso":')],
    ),
    "f07-dso-window-one-day-short": (
        "The DSO window ends one day early, so shortening by d days counts only d - 1 days of sales.",
        [("DAYS_PER_WEEK * HORIZON - lag + days + 1)", "DAYS_PER_WEEK * HORIZON - lag + days)")],
    ),
    "f08-dpo-window-drops-first-day": (
        "The DPO window starts one day late, so the earliest purchase day that moves is dropped.",
        [
            (
                "window = range(DAYS_PER_WEEK * HORIZON - lag - days + 1, DAYS_PER_WEEK * HORIZON - lag + 1)",
                "window = range(DAYS_PER_WEEK * HORIZON - lag - days + 2, DAYS_PER_WEEK * HORIZON - lag + 1)",
            )
        ],
    ),
    "f09-availability-uses-opening-balance": (
        "The revolver's availability is the commitment less the opening drawn balance in every week, not the balance at the start of the week.",
        [
            (
                "draw = min(need, commitment - drawn) if capped else need",
                'draw = min(need, commitment - case["opening_drawn_cents"]) if capped else need',
            )
        ],
    ),
    "f10-dso-impact-at-first-week-rate": (
        "The DSO impact multiplies the window's day count by the rate of its first day, which is right only for steady sales.",
        [
            (
                "return _half_up(sum((_daily_rate(sales, k) for k in window), Fraction(0)))",
                "return _half_up(len(window) * _daily_rate(sales, window[0]))",
            )
        ],
    ),
}


def main() -> None:
    source = REF.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (description, replacements) in MUTANTS.items():
        text = source
        for old, new in replacements:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{name}: expected exactly one match, found {count}: {old!r}")
            text = text.replace(old, new)
        body = text.replace('"""Reference solution', f'"""{description}\n\nReference solution', 1)
        (OUT / f"{name}.py").write_text(body, encoding="utf-8")
        print(f"wrote {name}.py")


if __name__ == "__main__":
    main()
