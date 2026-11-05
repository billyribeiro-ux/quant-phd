"""Write the round-10 student-error mutants of grader/reference.py into ledgers/FC1/mutants/ (verifier, FC1 slice c).

Each mutant is reference.py with one replacement; every replacement must match exactly once or the script fails.
Run from the checkout root: python -I ledgers/FC1/scripts/FC1-c-r10/make_mutants_r10.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course" / "modules" / "FC" / "FC1" / "grader" / "reference.py"
OUT = ROOT / "ledgers" / "FC1" / "mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "r10c_yield_refused_above_ten_thousand_percent": (
        "bond_price_cents refuses a yield above 10000 percent per period (yield_bps > 1000000), which the page does not "
        "refuse.",
        [
            (
                '    if rate <= -10_000:\n        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")\n',
                '    if rate <= -10_000:\n        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")\n'
                '    if rate > 1_000_000:\n        raise ValueError("yield_bps above 1000000 is refused")\n',
            ),
        ],
    ),
    "r10c_settlement_refused_above_one_million": (
        "CashTrade refuses a settlement period above 1000000, although the page says trades settling later are not "
        "bounded.",
        [
            (
                '        if day < 1:\n            raise ValueError("settlement_day must be at least 1")\n',
                '        if day < 1:\n            raise ValueError("settlement_day must be at least 1")\n'
                '        if day > 1_000_000:\n            raise ValueError("settlement_day above 1000000 is refused")\n',
            ),
        ],
    ),
    "r10c_price_ignores_events_after_period_one_thousand": (
        "bond_price_cents discards the events after period 1000 when it sums the present value, so a bond longer than "
        "1000 periods is priced without its tail.",
        [
            (
                "    for period, amount in bond.events():\n        total += Fraction(amount) / (1 + y) ** period\n",
                "    for period, amount in bond.events():\n        if period > 1_000:\n            continue\n"
                "        total += Fraction(amount) / (1 + y) ** period\n",
            ),
        ],
    ),
}


def main() -> None:
    source = REF.read_text(encoding="utf-8")
    body_start = source.index("from __future__ import annotations")
    for name, (summary, replacements) in MUTANTS.items():
        text = source[body_start:]
        for old, new in replacements:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{name}: replacement matched {count} times, expected 1: {old[:60]!r}")
            text = text.replace(old, new)
        header = f'"""{summary}\n\nWritten by the verifier for FC1 slice c, round 10: a student-error mutant of reference.py.\n"""\n\n'
        (OUT / f"{name}.py").write_text(header + text, encoding="utf-8")
        print(f"wrote {name}.py")


if __name__ == "__main__":
    main()
