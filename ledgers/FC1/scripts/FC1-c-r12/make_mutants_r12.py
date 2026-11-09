"""Write the verifier's round-12 student-error mutants (FC1 slice c) from reference.py by single edits."""
from __future__ import annotations

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD12-FC1-c")
REF = (ROOT / "course/modules/FC/FC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/FC1/mutants"
HEADER = "Written by the verifier for FC1 slice c, round 12: a student-error mutant of reference.py.\n"


def mutate(name: str, description: str, old: str, new: str) -> None:
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new)
    text = f'"""{description}\n\n{HEADER}"""\n' + body.split('"""', 2)[2]
    (OUT / f"{name}.py").write_text(text, encoding="utf-8")


mutate(
    "r12c_face_discounted_one_period_short",
    "bond_price_cents discounts the face one period short (by t - 1), though the coupons use their own period t.",
    "    for period, amount in bond.events():\n        total += Fraction(amount) / (1 + y) ** period\n",
    "    for period, amount in bond.events():\n"
    "        if amount == bond.events()[-1][1] and period == bond.periods:\n"
    "            total += Fraction(amount - bond.face_cents) / (1 + y) ** period\n"
    "            total += Fraction(bond.face_cents) / (1 + y) ** (period - 1)\n"
    "        else:\n"
    "            total += Fraction(amount) / (1 + y) ** period\n",
)
mutate(
    "r12c_trade_fee_one_cent",
    "CashTrade.events() adds a one-cent fee to the buyer's payment, which the page does not state.",
    "        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]",
    "        return [(self.settlement_day, -self.side * self.quantity * self.price_cents - (1 if self.side == 1 else 0))]",
)
mutate(
    "r12c_discount_base_from_float",
    "bond_price_cents builds the discount base 1 + y from a binary float, so the exact yield is not used.",
    "    y = Fraction(rate, 10_000)\n",
    "    y = Fraction(1 + rate / 10_000) - 1\n",
)
mutate(
    "r12c_price_limit_denominator",
    "bond_price_cents cleans the exact sum with limit_denominator(10**9) before rounding, which moves a near-half price.",
    "    return _half_away(total)\n",
    "    return _half_away(total.limit_denominator(10**9))\n",
)
print("wrote 4 mutants")
