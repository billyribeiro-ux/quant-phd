import pathlib
ref = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyC6-FC1-c/course/modules/FC/FC1/grader/reference.py").read_text()
out = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyC6-FC1-c/ledgers/FC1/mutants")

def make(name, doc, old, new, count=1):
    assert ref.count(old) == count, (name, ref.count(old))
    text = ref.replace(old, new)
    text = text.replace('"""Reference solution', f'"""{doc}\n\n"""Reference solution', 1) if False else text
    body = text.split('"""', 2)[2].lstrip("\n")
    (out / f"{name}.py").write_text(f'"""{doc}"""\n' + body)

make("c6n01_prints_on_negative_yield",
     "Student error: bond_price_cents prints a diagnostic line for every valid negative yield, which the page's silence rule forbids.",
     '    y = Fraction(rate, 10_000)\n    total = Fraction(0)',
     '    if rate < 0:\n        print("discounting at a negative yield")\n    y = Fraction(rate, 10_000)\n    total = Fraction(0)')
make("c6n02_prints_on_zero_coupon",
     "Student error: Bond.events prints a line when the coupon is zero, a valid input, which the page's silence rule forbids.",
     '        coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))\n',
     '        coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))\n        if self.coupon_bps == 0:\n            print("zero coupon")\n')
make("c6n03_prints_on_sell_side",
     "Student error: CashTrade.events prints a line for a sell, side -1, a valid input, which the page's silence rule forbids.",
     '        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]',
     '        if self.side == -1:\n            print("sell")\n        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]')
make("c6n04_settlement_day_capped_at_twelve",
     "Student error: CashTrade refuses a settlement_day above 12 with ValueError, a limit the page does not name.",
     '        if day < 1:\n            raise ValueError("settlement_day must be at least 1")',
     '        if day < 1 or day > 12:\n            raise ValueError("settlement_day must be at least 1")')
make("c6n05_discount_exponent_one_short",
     "Student error: bond_price_cents discounts each event by (1 + y) ** -(t - 1), one period short of the page's rule.",
     '        total += Fraction(amount) / (1 + y) ** period',
     '        total += Fraction(amount) / (1 + y) ** (period - 1)')
print("ok")
