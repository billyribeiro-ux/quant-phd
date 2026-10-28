"""Round-9 verifier mutants for AC4-e (m41-m46) and one alternative correct implementation (alt_k).

Each mutant is the reference solution with one plausible student error applied by exact string replacement.
Every replacement must match exactly once, or the script stops.
"""
from pathlib import Path

ROOT = Path("/tmp/verify9-AC4-e")
REF = (ROOT / "course/modules/AC/AC4/grader/reference.py").read_text(encoding="utf-8")
MUT = ROOT / "ledgers/AC4/mutants"
ALT = ROOT / "ledgers/AC4/scripts/AC4-e-r9"

DOC_OLD = REF[: REF.index('"""', 3) + 3]

MUTANTS = {
    "m41_mix_uses_budgeted_units.py": (
        "Mix contribution priced at the budgeted units, not the actual units, so the mix line uses the budget mix twice.",
        ('p["actual_units"] * (p["budget_price_cents"] - p["standard_inputs_per_unit"] * input_price)',
         'p["budget_units"] * (p["budget_price_cents"] - p["standard_inputs_per_unit"] * input_price)'),
    ),
    "m42_zero_actual_units_refused.py": (
        "flexible_budget refuses a zero actual unit count, although zero is a whole, non-negative count the spec accepts.",
        ('    total = _nonnegative(actual_units, "actual_units")\n',
         '    total = _nonnegative(actual_units, "actual_units")\n    if total == 0:\n        raise ValueError("actual units must be positive")\n'),
    ),
    "m43_flexed_revenue_at_actual_price.py": (
        "Flexed revenue priced at the actual selling prices instead of the budgeted prices.",
        ('budget_revenue = sum(p["budget_units"] * p["budget_price_cents"] for p in products)',
         'budget_revenue = sum(p["budget_units"] * p["actual_price_cents"] for p in products)'),
    ),
    "m44_total_is_flexed_minus_master.py": (
        "The total variance is set to the sales volume variance (flexed profit less master profit), not actual profit less master profit.",
        ('"total": actual_profit - master,', '"total": flexed - master,'),
    ),
    "m45_fixed_overhead_twice_in_flexed.py": (
        "flexible_budget subtracts fixed overhead twice from the flexed profit.",
        ('"profit_cents": revenue - variable - fixed,', '"profit_cents": revenue - variable - 2 * fixed,'),
    ),
    "m46_half_even_rounding.py": (
        "Flexed amounts rounded with Python's round(), which sends exact halves to the even cent, not halves up.",
        ("    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)\n",
         "    return round(amount)\n"),
    ),
}

for name, (doc, (old, new)) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    text = REF.replace(old, new, 1).replace(DOC_OLD, f'"""{doc}"""', 1)
    (MUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)

# Alternative correct implementation: exact half-up rounding by Decimal instead of integer arithmetic.
old_round = REF[REF.index("def _nearest_cent"): REF.index("def _case")]
new_round = '''def _nearest_cent(amount: Fraction) -> int:
    """The nearest whole cent, halves up, computed with Decimal at 60 digits."""
    from decimal import ROUND_HALF_UP, Decimal, localcontext

    if amount < 0:
        raise ValueError("a flexed amount cannot be negative")
    with localcontext() as ctx:
        ctx.prec = 60
        value = Decimal(amount.numerator) / Decimal(amount.denominator)
        return int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP))


'''
alt = REF.replace(old_round, new_round, 1)
assert alt != REF
(ALT / "alt_k.py").write_text(alt.replace(DOC_OLD, '"""Alternative: Decimal half-up rounding."""', 1), encoding="utf-8")
print("wrote alt_k.py")
