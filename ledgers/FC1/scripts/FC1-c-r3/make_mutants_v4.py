"""Write the verifier's round-3 student-error mutants (v4c_*) into ledgers/FC1/mutants/ from the reference solution and the float alternative."""
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD3-FC1-c")
ref = (ROOT / "course/modules/FC/FC1/grader/reference.py").read_text()
mut = ROOT / "ledgers/FC1/mutants"
specs = {
    "v4c_zero_amount_events_dropped.py": (
        "Student error: Bond.events() drops every zero-amount event, although the page keeps a zero amount as an event.",
        ("        out = [(t, coupon) for t in range(1, self.periods + 1)]\n        last_period, last_amount = out[-1]\n"
         "        out[-1] = (last_period, last_amount + self.face_cents)\n        return out",
         "        out = [(t, coupon) for t in range(1, self.periods + 1)]\n        last_period, last_amount = out[-1]\n"
         "        out[-1] = (last_period, last_amount + self.face_cents)\n        return [(t, a) for t, a in out if a != 0]")),
    "v4c_trade_sign_not_flipped.py": (
        "Student error: CashTrade.events() uses side as the sign, so the buyer (side +1) receives the cash.",
        ("return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]",
         "return [(self.settlement_day, self.side * self.quantity * self.price_cents)]")),
    "v4c_coupon_truncated_not_rounded.py": (
        "Student error: the coupon is truncated toward zero to whole cents instead of rounded half away from zero.",
        ("coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))",
         "coupon = (self.face_cents * self.coupon_bps) // 10_000")),
    "v4c_discount_exponent_one_short.py": (
        "Student error: each event is discounted by one period too few, (1 + y) ** -(t - 1), so period 1 is undiscounted.",
        ("total += Fraction(amount) / (1 + y) ** period", "total += Fraction(amount) / (1 + y) ** (period - 1)")),
}
for name, (doc, (old, new)) in specs.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    text = ref.replace(old, new)
    text = '"""' + doc + '"""\n\n' + text.split('"""', 2)[2].lstrip("\n")
    (mut / name).write_text(text)
    print("wrote", name)
alt = (ROOT / "ledgers/FC1/scripts/FC1-c-r3/alt_v4/alt_float_half_up.py").read_text()
body = alt.split('"""', 2)[2].lstrip("\n")
doc = ('"""Student error: bond_price_cents discounts with binary floats and rounds the float sum, so an exact half cent is decided '
       'by float error (13 * (1 + 0.04) ** -1 gives 12.499999999999998 and rounds to 12)."""\n\n')
(mut / "v4c_float_discount_half_up.py").write_text(doc + body)
print("wrote v4c_float_discount_half_up.py")
