"""Writes three alternative correct budget engines (round 38) for over-constraint checks."""
import pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
ref = (ROOT / "course/modules/AC/AC4/grader/reference.py").read_text(encoding="utf-8")
out = ROOT / "ledgers/AC4/scripts/AC4-e-r38/alts"


def swap(text, old, new):
    assert text.count(old) == 1, old[:60]
    return text.replace(old, new)


# alt a: nearest cent by Decimal quantize, halves up
a = swap(ref, "    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)\n",
         "    from decimal import Decimal, ROUND_HALF_UP\n"
         "    return int((Decimal(amount.numerator) / Decimal(amount.denominator)).quantize(Decimal(1), rounding=ROUND_HALF_UP))\n")
# alt b: total from the ledger of actual profit, not from the sum; mix written as actual contribution less flexed
b = swap(ref, '        "total": actual_profit - master,\n',
         '        "total": (sum(p["actual_units"] * p["actual_price_cents"] for p in products) - input_price * actual_inputs - fixed) - master,\n')
# alt c: type check by type(), flexed revenue via floor(x + 1/2)
import math
c = swap(ref, "    if isinstance(value, bool) or not isinstance(value, numbers.Integral):\n",
         "    if type(value) is bool or not isinstance(value, numbers.Integral):\n")
c = swap(c, "    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units))\n    variable = _nearest_cent(Fraction(total * budget_variable, budget_units))\n",
         "    revenue = math.floor(Fraction(total * budget_revenue, budget_units) + Fraction(1, 2))\n    variable = math.floor(Fraction(total * budget_variable, budget_units) + Fraction(1, 2))\n")
c = swap(c, "import numbers\n", "import math\nimport numbers\n")
for name, text in {"alt38_a_decimal_half_up.py": a, "alt38_b_total_from_ledger.py": b, "alt38_c_floor_half_and_type_check.py": c}.items():
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
