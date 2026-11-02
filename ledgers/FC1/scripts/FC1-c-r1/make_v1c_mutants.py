"""Writes five student-error mutants (v1c_*) of the FC1 reference into ledgers/FC1/mutants/.

Each mutant is reference.py with one replacement. The script asserts that every search string occurs exactly once,
so a mutant cannot silently equal the reference.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REF = ROOT / "course/modules/FC/FC1/grader/reference.py"
OUT = ROOT / "ledgers/FC1/mutants"

MUTANTS: dict[str, tuple[str, str, str]] = {
    "v1c_simple_discount_not_compound": (
        "Discounts each event by simple interest 1 / (1 + y * t) instead of the compound factor (1 + y) ** -t.",
        "total += Fraction(amount) / (1 + y) ** period",
        "total += Fraction(amount) / (1 + y * period)",
    ),
    "v1c_yield_guard_missing": (
        "Omits the yield guard, so yield_bps = -10000 divides by zero (ZeroDivisionError) instead of raising ValueError.",
        '    if rate <= -10_000:\n        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")\n',
        "",
    ),
    "v1c_seller_side_refused": (
        "Refuses the sell side: accepts only side +1, so a valid side -1 trade raises ValueError.",
        "if direction not in (1, -1):",
        "if direction != 1:",
    ),
    "v1c_price_discounted_at_coupon_rate": (
        "Discounts the price at the bond's coupon rate instead of the yield passed to bond_price_cents.",
        "    y = Fraction(rate, 10_000)\n",
        "    y = Fraction(bond.coupon_bps, 10_000)\n",
    ),
    "v1c_trade_rounded_to_dollars": (
        "Books the trade in whole dollars: rounds quantity * price to the nearest 100 cents before signing it.",
        "return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]",
        "return [(self.settlement_day, -self.side * round(self.quantity * self.price_cents, -2))]",
    ),
}

ref_text = REF.read_text(encoding="utf-8")
for name, (description, old, new) in MUTANTS.items():
    assert ref_text.count(old) == 1, (name, ref_text.count(old))
    head, sep, rest = ref_text.partition('"""')
    _doc_old, end, tail = rest.partition('"""')
    assert sep and end
    text = head + '"""' + description + '"""' + tail
    text = text.replace(old, new)
    assert text != ref_text
    (OUT / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", name)
