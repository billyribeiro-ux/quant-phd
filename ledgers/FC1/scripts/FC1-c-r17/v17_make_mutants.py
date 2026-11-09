"""FC1-c round 17: write three new student-error grader mutants from the reference (complete modules). Read-only on the course."""

import sys

root = sys.argv[1]
ref = open(f"{root}/course/modules/FC/FC1/grader/reference.py", encoding="utf-8").read()
header_end = ref.index('"""', 3) + 3  # end of the module docstring
body = ref[header_end:]


def write(name: str, first_line: str, replacements: list[tuple[str, str]]) -> None:
    text = body
    for old, new in replacements:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    doc = (
        f'"""{first_line}\n\n'
        "The grader copies this file to instruments.py in a scratch directory and runs the whole suite on it. It is not an\n"
        "answer shown to learners; BLUEPRINT requires that deployment exclude it, and no file in this repository enforces that.\n"
        '"""\n'
    )
    open(f"{root}/ledgers/FC1/mutants/{name}", "w", encoding="utf-8").write(doc + text)


write(
    "r17n01_trade_price_rounded_to_ten_cents.py",
    "Student error: CashTrade rounds price_cents to the nearest 10 cents before multiplying, so a trade at 9851 cents books as 9850; the page says a trade amount is an exact integer product.",
    [
        (
            "        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]",
            "        tens = _half_away(Fraction(self.price_cents, 10)) * 10\n"
            "        return [(self.settlement_day, -self.side * self.quantity * tens)]",
        )
    ],
)
write(
    "r17n02_zero_coupon_face_paid_in_first_period.py",
    "Student error: Bond with coupon_bps 0 pays its face in period 1 (the first period) instead of the last, so a zero-coupon bond's events are misdated; the page says the face is paid at maturity.",
    [
        (
            "        coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))\n"
            "        out = [(t, coupon) for t in range(1, self.periods + 1)]\n"
            "        last_period, last_amount = out[-1]\n"
            "        out[-1] = (last_period, last_amount + self.face_cents)\n"
            "        return out",
            "        coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))\n"
            "        out = [(t, coupon) for t in range(1, self.periods + 1)]\n"
            "        if self.coupon_bps == 0:\n"
            "            return [(1, self.face_cents)] + out[1:]\n"
            "        last_period, last_amount = out[-1]\n"
            "        out[-1] = (last_period, last_amount + self.face_cents)\n"
            "        return out",
        )
    ],
)
write(
    "r17n03_coupons_discounted_as_paid_at_period_start.py",
    "Student error: bond_price_cents discounts each coupon one period short (the coupon of period t is paid at the start of period t), while the face and the final coupon use period t; the page discounts an event in period t by (1 + y) ** -t.",
    [
        (
            "    for period, amount in bond.events():\n        total += Fraction(amount) / (1 + y) ** period",
            "    for period, amount in bond.events():\n        exponent = period - 1 if period < bond.periods else period\n        total += Fraction(amount) / (1 + y) ** exponent",
        )
    ],
)
print("written")
