"""Round 4 verifier mutants for FC1 project: each is the reference solution with one student error applied."""
import pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/FC/FC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/FC1/mutants"

EVENTS_OLD = '''        coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))
        out = [(t, coupon) for t in range(1, self.periods + 1)]
'''
EVENTS_CUMULATIVE = '''        out = []
        paid = 0
        for t in range(1, self.periods + 1):
            cumulative = _half_away(Fraction(self.face_cents * self.coupon_bps * t, 10_000))
            out.append((t, cumulative - paid))
            paid = cumulative
'''
PRICE_OLD = "        total += Fraction(amount) / (1 + y) ** period\n"
PRICE_NEW = ("        exponent = 0 if amount > bond.face_cents else period\n"
             "        total += Fraction(amount) / (1 + y) ** exponent\n")

MUTANTS = {
    "d01_zero_face_accepted.py": (
        "Bond accepts face_cents = 0, which the page names as refused (face_cents not positive).",
        [("        if face <= 0:\n", "        if face < 0:\n")]),
    "d02_zero_periods_accepted.py": (
        "Bond accepts periods = 0 and returns no events, though the page names periods < 1 as refused.",
        [("        if count < 1:\n", "        if count < 0:\n")]),
    "d03_price_minus_one_accepted.py": (
        "CashTrade accepts price_cents = -1, an off-by-one on the boundary the page names as refused.",
        [("        if price < 0:\n", "        if price < -1:\n")]),
    "d04_settlement_day_zero_accepted.py": (
        "CashTrade accepts settlement_day = 0 (period 0 is the trade date), which the page names as refused.",
        [("        if day < 1:\n", "        if day < 0:\n")]),
    "d05_sale_booked_as_payment.py": (
        "A sale is booked as a payment, because the side enters the cash flow as an absolute value.",
        [("        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]\n",
          "        return [(self.settlement_day, -abs(self.side) * self.quantity * self.price_cents)]\n")]),
    "d06_coupons_on_cumulative_accrual.py": (
        "Each coupon is the difference of cumulative rounded accruals, so coupons differ by a cent from face times rate.",
        [(EVENTS_OLD, EVENTS_CUMULATIVE)]),
    "d07_final_event_not_discounted.py": (
        "The last event (its coupon and the face together) is priced undiscounted, selected by amount > face.",
        [(PRICE_OLD, PRICE_NEW)]),
}

for name, (doc, edits) in MUTANTS.items():
    src = REF
    for old, new in edits:
        assert src.count(old) == 1, (name, old)
        src = src.replace(old, new)
    # replace the module docstring with a one-line description of the error
    end = src.index('"""', 3) + 3
    src = f'"""{doc}"""' + src[end:]
    (OUT / name).write_text(src, encoding="utf-8")
    print("wrote", name)
