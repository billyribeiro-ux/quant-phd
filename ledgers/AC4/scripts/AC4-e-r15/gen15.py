import pathlib, sys
ROOT = pathlib.Path(sys.argv[1])
R = (ROOT / "course/modules/AC/AC4/grader/reference.py").read_text()
M = ROOT / "ledgers/AC4/mutants"
ALT = ROOT / "ledgers/AC4/scripts/AC4-e-r15/alts"
ALT.mkdir(parents=True, exist_ok=True)

def build(doc, pairs):
    src = R
    for old, new in pairs:
        assert src.count(old) == 1, (doc[:40], old[:70], src.count(old))
        src = src.replace(old, new)
    body = src.split('"""', 2)[2].lstrip("\n")
    return f'"""{doc}"""\n' + body

ALTS = {
 "alt15_a_decimal_half_up": ("Alternative 15a (correct): the nearest cent is taken with decimal ROUND_HALF_UP.",
   [("import numbers\n", "import numbers\nfrom decimal import ROUND_HALF_UP, Decimal\n"),
    ("    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)",
     "    q = (Decimal(amount.numerator) / Decimal(amount.denominator)).quantize(Decimal(1), rounding=ROUND_HALF_UP)\n    return int(q)")]),
 "alt15_b_floor_plus_half": ("Alternative 15b (correct): the nearest cent is floor(x + 1/2) by the floor of an exact fraction, halves up.",
   [("    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)",
     "    import math\n    return math.floor(amount + Fraction(1, 2))")]),
 "alt15_c_type_check_validator": ("Alternative 15c (correct): a whole number is an int by exact type, a bool is refused, and no other int subclass is used.",
   [("    if isinstance(value, bool) or not isinstance(value, numbers.Integral):",
     "    if type(value) is not int:"),
    ("    return int(value)\n\n\ndef _nonnegative", "    return value\n\n\ndef _nonnegative")]),
}
MUTS = {
 "r15e_01_last_product_zero_budget_units_refused": ("Student error: a product that budgets zero units is refused when it is the last product, as if a budget needed every product to sell.",
   [("    if sum(p[\"budget_units\"] for p in products) == 0:",
     "    if products[-1][\"budget_units\"] == 0:\n        raise ValueError(\"a product budgets no units\")\n    if sum(p[\"budget_units\"] for p in products) == 0:")]),
 "r15e_02_flexed_revenue_half_cent_rounds_down": ("Student error: the flexed revenue rounds an exact half cent down, while the flexed variable cost rounds it up.",
   [("    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units))",
     "    revenue = -((budget_units - 2 * total * budget_revenue) // (2 * budget_units))")]),
 "r15e_03_missing_actual_price_defaults_to_budget": ("Student error: a product with no actual price is read as sold at its budgeted price, not refused.",
   [("            if field not in item:\n                raise ValueError(f\"a product has no {field!r} field\")",
     "            if field not in item and field != \"actual_price_cents\":\n                raise ValueError(f\"a product has no {field!r} field\")"),
    ("                \"actual_price_cents\": _nonnegative(item[\"actual_price_cents\"], f\"{name} actual_price_cents\"),",
     "                \"actual_price_cents\": _nonnegative(item.get(\"actual_price_cents\", item[\"budget_price_cents\"]), f\"{name} actual_price_cents\"),")]),
 "r15e_04_last_product_float_budget_price_truncated": ("Student error: a float budgeted price in the last product is truncated to whole cents, not refused.",
   [("                \"budget_price_cents\": _nonnegative(item[\"budget_price_cents\"], f\"{name} budget_price_cents\"),",
     "                \"budget_price_cents\": (int(item[\"budget_price_cents\"]) if item is raw[-1] and isinstance(item[\"budget_price_cents\"], float) else _nonnegative(item[\"budget_price_cents\"], f\"{name} budget_price_cents\")),")]),
}
for name, (doc, pairs) in ALTS.items():
    (ALT / f"{name}.py").write_text(build(doc, pairs))
for name, (doc, pairs) in MUTS.items():
    (M / f"{name}.py").write_text(build(doc, pairs))
    print("wrote mutant", name)
print("wrote", len(ALTS), "alternatives")
