"""Write round-4 student-error mutants of the FC1 reference (verifier r4). Each is a complete module; the first docstring line names the error."""
import pathlib

REF = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD4-FC1-c/course/modules/FC/FC1/grader/reference.py")
OUT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD4-FC1-c/ledgers/FC1/mutants")
base = REF.read_text(encoding="utf-8")

MUTANTS = {
    "r4c_schedule_stops_at_thirty_periods.py": (
        "Student error: the schedule loop stops at thirty periods, so a bond longer than thirty periods loses its later coupons and its face.",
        [("        out = [(t, coupon) for t in range(1, self.periods + 1)]",
          "        out = [(t, coupon) for t in range(1, min(self.periods, 30) + 1)]")],
    ),
    "r4c_discount_exponent_capped_at_thirty.py": (
        "Student error: the discount exponent is capped at thirty, so an event after period thirty is discounted by (1 + y) ** -30.",
        [("        total += Fraction(amount) / (1 + y) ** period",
          "        total += Fraction(amount) / (1 + y) ** min(period, 30)")],
    ),
    "r4c_trade_amount_through_float.py": (
        "Student error: the trade cash flow goes through a float, so a product above 2**53 loses its last digits.",
        [("        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]",
          "        return [(self.settlement_day, int(-self.side * self.quantity * self.price_cents * 1.0))]")],
    ),
    "r4c_price_python_round_half_even.py": (
        "Student error: the price is rounded with Python's round(), which sends an exact half to the even cent.",
        [("    return _half_away(total)\n",
          "    return round(total)\n")],
    ),
    "r4c_yield_bound_at_minus_nine_thousand.py": (
        "Student error: bond_price_cents refuses a yield at or below -9000 basis points, a bound it invents rather than the page's -10000.",
        [("    if rate <= -10_000:\n        raise ValueError(\"yield_bps must be greater than -10000, so that 1 + y is positive\")",
          "    if rate <= -9_000:\n        raise ValueError(\"yield_bps must be greater than -9000\")")],
    ),
}

for name, (doc, edits) in MUTANTS.items():
    text = base
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    # Replace the module docstring's first line with the student-error description, keeping the rest.
    head, sep, rest = text.partition('"""')
    assert sep, name
    text = '"""' + doc + "\n\n" + rest
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
