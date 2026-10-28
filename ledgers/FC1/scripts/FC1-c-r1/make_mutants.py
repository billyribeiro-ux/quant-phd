# Generates the verifier's own FC1 project mutants from the reference solution text (scratch tool).
import pathlib, re, sys
REF = pathlib.Path("/tmp/verifyC1-FC1-c/course/modules/FC/FC1/grader/reference.py").read_text()
OUT = pathlib.Path("/tmp/verifyC1-FC1-c/ledgers/FC1/mutants")
MUTANTS = {
 "v01_print_on_refused_quantity.py": (
  "Prints a diagnostic line before refusing a quantity below 1, which the page's silence rule forbids (No function prints).",
  [("        if units < 1:\n            raise ValueError(\"quantity must be at least 1\")",
    "        if units < 1:\n            print(\"quantity refused:\", units)\n            raise ValueError(\"quantity must be at least 1\")")]),
 "v02_price_rounded_half_even.py": (
  "Rounds the exact present value with Python's round(), which sends an exact half to the even cent, not away from zero.",
  [("    return _half_away(total)\n\n\nclass CashTrade",
    "    return round(total)\n\n\nclass CashTrade")]),
 "v03_coupon_rounded_half_even.py": (
  "Rounds each coupon with Python's round() on the exact product, so an exact half cent goes to the even cent.",
  [("        coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))",
    "        coupon = round(Fraction(self.face_cents * self.coupon_bps, 10_000))")]),
 "v04_price_from_float_discounting.py": (
  "Discounts in binary floats and rounds with Python's round() on the float, though the page requires exact fractions.",
  [("    y = Fraction(rate, 10_000)\n    total = Fraction(0)\n    for period, amount in bond.events():\n        total += Fraction(amount) / (1 + y) ** period\n    return _half_away(total)",
    "    v = 1.0 + rate / 10_000\n    total = 0.0\n    for period, amount in bond.events():\n        total += amount / v ** period\n    return round(total)")]),
 "v05_zero_amount_events_dropped.py": (
  "Drops every zero-amount event, although the page says a zero amount is an event and is kept.",
  [("        return out\n\n\ndef bond_price_cents",
    "        return [row for row in out if row[1] != 0]\n\n\ndef bond_price_cents")]),
 "v06_refuses_zero_yield.py": (
  "Refuses a zero yield with the yield message, though the page only refuses yield_bps at or below -10000.",
  [("    if rate <= -10_000:", "    if rate <= 0:")]),
}
for name, (doc, pairs) in MUTANTS.items():
    s = REF
    for a, b in pairs:
        assert s.count(a) == 1, (name, a[:60])
        s = s.replace(a, b)
    # replace the reference module docstring with the one-line mutant docstring
    s = re.sub(r'\A""".*?"""', '"""' + doc + '"""', s, count=1, flags=re.S)
    (OUT / name).write_text(s)
    print("wrote", name)
