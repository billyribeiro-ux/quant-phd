"""Round 5 verifier (FC1-c): write new student-error mutants of the reference grader solution.

Each mutant is reference.py with one change. The docstring's first line names the student error (read by mutate_graders).
"""
import pathlib
import sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD5-FC1-c")
REF = ROOT / "course/modules/FC/FC1/grader/reference.py"
OUT = ROOT / "ledgers/FC1/mutants"
src = REF.read_text(encoding="utf-8")

MUTANTS = {
    "r5c_price_rounded_with_epsilon": (
        "Student error: bond_price_cents adds 1e-9 cent before rounding, so an exact value a hair under a half cent rounds up.",
        "    return _half_away(total)\n",
        "    return _half_away(total + Fraction(1, 10**9))\n",
    ),
    "r5c_yield_above_one_hundred_percent_refused": (
        "Student error: bond_price_cents refuses a yield above 10000 basis points, a limit the page does not name.",
        "    rate = _whole(yield_bps, \"yield_bps\")\n",
        "    rate = _whole(yield_bps, \"yield_bps\")\n    if rate > 10_000:\n        raise ValueError(\"yield_bps above 10000 is not supported\")\n",
    ),
    "r5c_discount_exponent_capped_at_twenty_four": (
        "Student error: the discount exponent is capped at twenty-four, so events after period 24 are discounted too little.",
        "        total += Fraction(amount) / (1 + y) ** period\n",
        "        total += Fraction(amount) / (1 + y) ** min(period, 24)\n",
    ),
    "r5c_settlement_event_one_period_late": (
        "Student error: CashTrade.events() puts the one settlement event one period after the settlement period.",
        "        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]\n",
        "        return [(self.settlement_day + 1, -self.side * self.quantity * self.price_cents)]\n",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    assert src.count(old) == 1, (name, src.count(old))
    head_old = src.split('"""', 2)
    body = src.replace(old, new, 1)
    # Replace the module docstring's first line with the student-error description.
    first, rest = body.split("\n", 1)
    assert first.startswith('"""'), first
    body = '"""' + doc.removeprefix("Student error: ").join(["Student error: ", ""]) + "\n" + rest
    (OUT / f"{name}.py").write_text(body, encoding="utf-8")
    print("wrote", name)
