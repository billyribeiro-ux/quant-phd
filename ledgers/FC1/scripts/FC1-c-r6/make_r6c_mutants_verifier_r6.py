"""Writes the round-6 verifier mutants from the reference solution by exact string edits (each edit must match once)."""
import pathlib
import sys

REF = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
OUT = pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

HEAD_OLD = '"""Reference solution for the FC1 cash-instrument engine (instruments.py).'

MUTANTS = {
    "r6c_schedule_stops_at_forty_periods.py": (
        "Student error: Bond.events() builds at most forty periods, so a bond longer than forty periods loses its later coupons and its face.",
        [("        out = [(t, coupon) for t in range(1, self.periods + 1)]",
          "        out = [(t, coupon) for t in range(1, min(self.periods, 40) + 1)]")],
    ),
    "r6c_discount_exponent_capped_at_forty.py": (
        "Student error: the discount exponent is capped at forty, so an event after period forty is discounted by (1 + y) ** -40.",
        [("        total += Fraction(amount) / (1 + y) ** period",
          "        total += Fraction(amount) / (1 + y) ** min(period, 40)")],
    ),
    "r6c_coupon_cumulative_rounding.py": (
        "Student error: each period's coupon is the difference of cumulative rounded accruals, so a half cent carried from one period changes the next coupon.",
        [("        out = [(t, coupon) for t in range(1, self.periods + 1)]",
          "        exact = Fraction(self.face_cents * self.coupon_bps, 10_000)\n"
          "        out = [(t, _half_away(exact * t) - _half_away(exact * (t - 1))) for t in range(1, self.periods + 1)]")],
    ),
    "r6c_yield_above_two_hundred_percent_refused.py": (
        "Student error: bond_price_cents refuses a yield above 20000 basis points, a limit the page does not name.",
        [("    if rate <= -10_000:\n        raise ValueError(\"yield_bps must be greater than -10000, so that 1 + y is positive\")",
          "    if rate <= -10_000 or rate > 20_000:\n        raise ValueError(\"yield_bps must be greater than -10000, so that 1 + y is positive\")")],
    ),
    "r6c_settlement_day_above_one_hundred_refused.py": (
        "Student error: CashTrade refuses a settlement period above 100, a limit the page does not name.",
        [("        if day < 1:\n            raise ValueError(\"settlement_day must be at least 1\")",
          "        if day < 1 or day > 100:\n            raise ValueError(\"settlement_day must be at least 1\")")],
    ),
    "r6c_quantity_above_two_thousand_refused.py": (
        "Student error: CashTrade refuses a quantity above 2000 units, a limit the page does not name.",
        [("        if units < 1:\n            raise ValueError(\"quantity must be at least 1\")",
          "        if units < 1 or units > 2000:\n            raise ValueError(\"quantity must be at least 1\")")],
    ),
}

for name, (first_line, edits) in MUTANTS.items():
    text = REF
    assert text.count(HEAD_OLD) == 1, name
    text = text.replace(HEAD_OLD, '"""' + first_line + "\n\nDerived from the reference solution by one edit (verifier round 6).", 1)
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new, 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
