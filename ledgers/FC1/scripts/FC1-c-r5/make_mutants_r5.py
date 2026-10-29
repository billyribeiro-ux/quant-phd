"""Writes the verifier's new student-error mutants (round 5) as complete modules from reference.py."""
import pathlib, sys
ref = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2])
def sub(src, old, new):
    assert src.count(old) == 1, (old, src.count(old))
    return src.replace(old, new)
specs = {
 "c5n01_events_sorted_descending.py": (
   "Bond.events returns the periods in descending order, although the page says the list is sorted by period.",
   [("        return out\n\n\ndef bond_price_cents", "        return out[::-1]\n\n\ndef bond_price_cents")]),
 "c5n02_period_zero_event.py": (
   "Bond.events adds a zero-amount event in period 0 (the trade date), which the page says no event falls in.",
   [("        out = [(t, coupon) for t in range(1, self.periods + 1)]",
     "        out = [(0, 0)] + [(t, coupon) for t in range(1, self.periods + 1)]")]),
 "c5n03_events_mutates_schedule.py": (
   "Bond.events adds the face to the stored last event each time it is called, so a second call differs from the first.",
   [("        coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))\n        out = [(t, coupon) for t in range(1, self.periods + 1)]\n        last_period, last_amount = out[-1]\n        out[-1] = (last_period, last_amount + self.face_cents)\n        return out",
     "        if not hasattr(self, '_schedule'):\n            coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))\n            self._schedule = [(t, coupon) for t in range(1, self.periods + 1)]\n        last_period, last_amount = self._schedule[-1]\n        self._schedule[-1] = (last_period, last_amount + self.face_cents)\n        return list(self._schedule)")]),
 "c5n04_price_truncated_not_rounded.py": (
   "bond_price_cents truncates the exact present value toward zero instead of rounding it half away from zero.",
   [("    return _half_away(total)\n\n\nclass CashTrade", "    return int(total)\n\n\nclass CashTrade")]),
 "c5n05_zero_price_refused.py": (
   "CashTrade refuses a zero price with the price message, though the page allows a price of 0 and names only negative prices.",
   [('        if price < 0:\n            raise ValueError("price_cents must not be negative")',
     '        if price <= 0:\n            raise ValueError("price_cents must not be negative")')]),
}
for name, (doc, reps) in specs.items():
    src = ref
    for old, new in reps:
        src = sub(src, old, new)
    src = src.replace('"""Reference solution', '"""' + doc + ' Reference solution', 1) if False else src
    _, _, rest = src.partition('"""')
    _, _, rest = rest.partition('"""')
    body = '"""' + doc + '"""' + rest
    (out / name).write_text(body, encoding="utf-8")
    print("wrote", name)
