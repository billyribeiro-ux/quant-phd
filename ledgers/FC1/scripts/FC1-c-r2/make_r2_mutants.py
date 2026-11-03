"""Write this round's four student-error mutants from grader/reference.py, one asserted replacement each.

Each mutant opens with a one-line docstring that names the student error (VERIFIER rule 9 / FINAL-ARCHITECT-RULINGS 9).
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REF = (ROOT / "course/modules/FC/FC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/FC1/mutants"

MUTANTS = {
    "r2c_events_change_on_second_call.py": (
        "        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]\n",
        "        self._calls = getattr(self, \"_calls\", 0) + 1\n"
        "        return [(self.settlement_day, -self.side * self.quantity * self.price_cents + (self._calls - 1))]\n",
        "Trade events() depends on hidden state: the second call differs from the first (pure-function rule, page Conventions)",
    ),
    "r2c_bond_periods_capped_at_twelve.py": (
        "        coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))\n"
        "        out = [(t, coupon) for t in range(1, self.periods + 1)]\n",
        "        coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))\n"
        "        out = [(t, coupon) for t in range(1, min(self.periods, 12) + 1)]\n",
        "Bond schedule silently stops after twelve periods, so a 13-to-15-period bond loses its later coupons and its face",
    ),
    "r2c_trade_settles_one_period_early.py": (
        "        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]\n",
        "        early = self.settlement_day - 1 if self.settlement_day >= 2 else self.settlement_day\n"
        "        return [(early, -self.side * self.quantity * self.price_cents)]\n",
        "Settlement event booked one period before the settlement period, an off-by-one in the period index",
    ),
    "r2c_price_cached_on_first_yield.py": (
        "    rate = _whole(yield_bps, \"yield_bps\")\n",
        "    cached = getattr(bond, \"_price_cache\", None)\n"
        "    if cached is not None:\n"
        "        return cached\n"
        "    rate = _whole(yield_bps, \"yield_bps\")\n",
        "Price is cached on the bond at its first yield and returned unchanged for every later yield",
    ),
}

for name, (old, new, doc) in MUTANTS.items():
    assert REF.count(old) == 1, f"{name}: anchor not unique or missing"
    text = REF.replace(old, new, 1)
    # the mutant's first line is the error it makes (the reference docstring is replaced by the one-liner)
    head_end = text.index('"""', 3) + 3
    body = text[head_end:]
    text = f'"""{doc}."""' + body
    if name.startswith("r2c_price_cached"):
        text = text.replace("    return _half_away(total)\n", "    bond._price_cache = _half_away(total)\n    return bond._price_cache\n", 1)
        assert "bond._price_cache = _half_away(total)" in text
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", OUT / name)
