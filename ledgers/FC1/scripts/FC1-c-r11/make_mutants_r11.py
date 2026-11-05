"""Write the round-11 student-error mutants of grader/reference.py into ledgers/FC1/mutants/ (verifier, FC1 slice c, r11).

Each mutant is reference.py with one replacement; every replacement must match exactly once or the script fails.
Run from the checkout root: python -I ledgers/FC1/scripts/FC1-c-r11/make_mutants_r11.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course" / "modules" / "FC" / "FC1" / "grader" / "reference.py"
OUT = ROOT / "ledgers" / "FC1" / "mutants"

SETTLE = '        if day < 1:\n            raise ValueError("settlement_day must be at least 1")\n'
YIELD = '    if rate <= -10_000:\n        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")\n'
QTY = '        if units < 1:\n            raise ValueError("quantity must be at least 1")\n'
PRICE_RETURN = "    return _half_away(total)\n"
COUPON = "        coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))\n"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "r11c_settlement_refused_above_ten_million": (
        "CashTrade refuses a settlement period above 10000000, a bound the page does not state; the largest settlement "
        "period the suite accepts is 10**7 itself.",
        [(SETTLE, SETTLE + '        if day > 10_000_000:\n            raise ValueError("settlement_day above 10**7")\n')],
    ),
    "r11c_yield_refused_above_hundred_thousand_percent": (
        "bond_price_cents refuses a yield above 10000000 bps (100000 percent per period), a bound the page does not "
        "state; the largest yield the suite accepts is 10**7 bps itself.",
        [(YIELD, YIELD + '    if rate > 10_000_000:\n        raise ValueError("yield_bps above 10**7 is refused")\n')],
    ),
    "r11c_quantity_refused_above_ten_to_the_thirtieth": (
        "CashTrade refuses a quantity above 10**30 units, a bound the page does not state; the largest quantity the "
        "suite accepts is 10**30 itself.",
        [(QTY, QTY + '        if units > 10**30:\n            raise ValueError("quantity above 10**30 is refused")\n')],
    ),
    "r11c_coupon_rounded_half_even": (
        "Bond.events() rounds the coupon with Python round(), which sends an exact half cent to the even cent, although "
        "the page says a half goes away from zero.",
        [(COUPON, "        coupon = round(Fraction(self.face_cents * self.coupon_bps, 10_000))\n")],
    ),
    "r11c_zero_yield_price_drops_last_event": (
        "bond_price_cents drops the last event when the yield is zero, so a zero-yield bond is priced without its face.",
        [
            (
                "    y = Fraction(rate, 10_000)\n    total = Fraction(0)\n    for period, amount in bond.events():\n",
                "    y = Fraction(rate, 10_000)\n    total = Fraction(0)\n    events = bond.events()\n"
                "    if rate == 0:\n        events = events[:-1]\n    for period, amount in events:\n",
            )
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
        header = (
            f'"""{summary}\n\nWritten by the verifier for FC1 slice c, round 11: a student-error mutant of reference.py.\n"""\n\n'
        )
        (OUT / f"{name}.py").write_text(header + text, encoding="utf-8")
        print(f"wrote {name}.py")


if __name__ == "__main__":
    main()
