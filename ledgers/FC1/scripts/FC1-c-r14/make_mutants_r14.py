"""Round 14, FC1-c: write four new student-error mutants of the reference solution into ledgers/FC1/mutants/.

Each mutant is grader/reference.py with one replaced block (the block must occur exactly once in the reference).
The first docstring line of each mutant names the student error.
Usage: python -I ledgers/FC1/scripts/FC1-c-r14/make_mutants_r14.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/FC/FC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/FC1/mutants"
HEAD_OLD = '"""Reference solution for the FC1 cash-instrument engine (instruments.py).'

PRICE_OLD = '''def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    """The present value of the bond's events at a per-period yield, summed exactly and rounded once."""
    rate = _whole(yield_bps, "yield_bps")
    if rate <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    y = Fraction(rate, 10_000)
    total = Fraction(0)
    for period, amount in bond.events():
        total += Fraction(amount) / (1 + y) ** period
    return _half_away(total)
'''

PRICE_MEMO = '''_PRICE_MEMO: dict[int, int] = {}


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    """The present value of the bond's events at a per-period yield, summed exactly and rounded once."""
    rate = _whole(yield_bps, "yield_bps")
    if rate <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    if rate in _PRICE_MEMO:
        return _PRICE_MEMO[rate]
    y = Fraction(rate, 10_000)
    total = Fraction(0)
    for period, amount in bond.events():
        total += Fraction(amount) / (1 + y) ** period
    _PRICE_MEMO[rate] = _half_away(total)
    return _PRICE_MEMO[rate]
'''

PRICE_ABS = PRICE_OLD.replace("y = Fraction(rate, 10_000)", "y = Fraction(abs(rate), 10_000)")

CASH_OLD = '''        if units < 1:
            raise ValueError("quantity must be at least 1")
        if price < 0:
            raise ValueError("price_cents must not be negative")
        if direction not in (1, -1):
            raise ValueError("side must be +1 (buy) or -1 (sell)")
        if day < 1:
            raise ValueError("settlement_day must be at least 1")
'''

CASH_BUY_ONLY = '''        if direction not in (1, -1):
            raise ValueError("side must be +1 (buy) or -1 (sell)")
        if direction == 1:
            if units < 1:
                raise ValueError("quantity must be at least 1")
            if price < 0:
                raise ValueError("price_cents must not be negative")
            if day < 1:
                raise ValueError("settlement_day must be at least 1")
'''

FACE_OLD = '''        last_period, last_amount = out[-1]
        out[-1] = (last_period, last_amount + self.face_cents)
'''

FACE_FIRST = '''        first_period, first_amount = out[0]
        out[0] = (first_period, first_amount + self.face_cents)
'''

MUTANTS = {
    "r14n01_sale_skips_quantity_and_settlement_checks.py": (
        "Student error: CashTrade checks quantity, price and settlement_day only for a buy, so a sale of zero units is accepted.",
        [(CASH_OLD, CASH_BUY_ONLY)],
    ),
    "r14n02_price_memo_keyed_by_yield_alone.py": (
        "Student error: bond_price_cents memoises by yield_bps alone, so a second bond priced at the same yield gets the first bond's price.",
        [(PRICE_OLD, PRICE_MEMO)],
    ),
    "r14n03_negative_yield_read_as_its_magnitude.py": (
        "Student error: bond_price_cents discounts with the magnitude of the yield, so a negative yield is priced as its positive twin.",
        [(PRICE_OLD, PRICE_ABS)],
    ),
    "r14n04_face_paid_with_the_first_coupon.py": (
        "Student error: Bond.events() adds the face to the first period instead of the last, so the principal is paid at the start.",
        [(FACE_OLD, FACE_FIRST)],
    ),
}

for name, (first_line, edits) in MUTANTS.items():
    text = REF
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:40])
        text = text.replace(old, new, 1)
    assert text.count(HEAD_OLD) == 1
    text = text.replace(HEAD_OLD, f'"""{first_line}\n\n' + HEAD_OLD[3:], 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)

# Probe added after the first run (round 14): the named Bond refusals are tested only with a non-zero coupon.
BOND_OLD = '''        if count < 1:
            raise ValueError("periods must be at least 1")
        if face <= 0:
            raise ValueError("face_cents must be positive")
        if coupon < 0:
            raise ValueError("coupon_bps must not be negative")
'''
BOND_ZERO_COUPON_ONLY = '''        if coupon < 0:
            raise ValueError("coupon_bps must not be negative")
        if coupon != 0:
            if count < 1:
                raise ValueError("periods must be at least 1")
            if face <= 0:
                raise ValueError("face_cents must be positive")
'''
name = "r14n05_bond_periods_and_face_checked_only_with_a_coupon.py"
text = REF
assert text.count(BOND_OLD) == 1
text = text.replace(BOND_OLD, BOND_ZERO_COUPON_ONLY, 1)
text = text.replace(HEAD_OLD, '"""Student error: Bond refuses periods below 1 and a non-positive face only when the coupon is non-zero, so a zero-coupon bond with no face is accepted.\n\n' + HEAD_OLD[3:], 1)
(OUT / name).write_text(text, encoding="utf-8")
print("wrote", name)
