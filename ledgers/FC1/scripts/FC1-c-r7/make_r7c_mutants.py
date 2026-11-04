"""Write round-7 student-error mutants (FC1-c) as complete solution modules, derived from reference.py by one edit each.

Each edit must match exactly once in reference.py, so a mutant is never a silent no-op. Output: ledgers/FC1/mutants/r7c_*.py
"""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/FC/FC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/FC1/mutants"

MUTANTS = {
    "r7c_coupon_rounded_half_even.py": (
        "Student error: the coupon is rounded to the nearest cent with Python round() (half to even), not half away from zero.",
        "        coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))\n",
        "        coupon = round(Fraction(self.face_cents * self.coupon_bps, 10_000))\n",
    ),
    "r7c_price_refused_above_one_million_cents.py": (
        "Student error: bond_price_cents refuses a trade-sized or bond-sized price above one million cents as too large.",
        "    rate = _whole(yield_bps, \"yield_bps\")\n",
        "    rate = _whole(yield_bps, \"yield_bps\")\n    if sum(a for _, a in bond.events()) > 1_000_000:\n        raise ValueError(\"the price is too large\")\n",
    ),
    "r7c_periods_refused_above_one_thousand.py": (
        "Student error: Bond refuses more than one thousand coupon periods, a limit the page does not state.",
        "        if count < 1:\n            raise ValueError(\"periods must be at least 1\")\n",
        "        if count < 1 or count > 1_000:\n            raise ValueError(\"periods must be at least 1\")\n",
    ),
    "r7c_price_is_seed_zero_answer_constant.py": (
        "Student error: bond_price_cents returns the seed-zero answer, 4281937 cents, for every bond and yield (a hard-coded answer).",
        "    rate = _whole(yield_bps, \"yield_bps\")\n",
        "    rate = _whole(yield_bps, \"yield_bps\")\n    return 4_281_937\n",
    ),
    "r7c_discount_factor_float_then_exact.py": (
        "Student error: each discount factor is a float, (1 + yield_bps / 10000) ** -period, converted to an exact Fraction before the sum.",
        "        total += Fraction(amount) / (1 + y) ** period\n",
        "        total += Fraction(amount) * Fraction((1 + rate / 10_000) ** -period)\n",
    ),
}

for name, (description, old, new) in MUTANTS.items():
    count = REF.count(old)
    if count != 1:
        raise SystemExit(f"{name}: anchor found {count} times, expected exactly 1")
    body = REF.replace(old, new)
    # the docstring's first line describes the error; the module is otherwise the reference solution
    text = f'"""{description}"""\n' + body.split('"""', 2)[2]
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
