"""Round-10 verifier mutants for AC4-e (m47-m50), each the reference with one plausible student error.

Each replacement must match exactly once, or the script stops. The docstring of each mutant names the error.
"""
from pathlib import Path

ROOT = Path("/tmp/verify10-AC4-e")
REF = (ROOT / "course/modules/AC/AC4/grader/reference.py").read_text(encoding="utf-8")
MUT = ROOT / "ledgers/AC4/mutants"
DOC_OLD = REF[: REF.index('"""', 3) + 3]

MUTANTS = {
    "m47_mix_omits_fixed_overhead.py": (
        "The actual-mix contribution forgets to deduct fixed overhead, so the mix line is off by the fixed overhead.",
        ("        - fixed\n    )\n    actual_profit", "    )\n    actual_profit"),
    ),
    "m48_efficiency_against_budgeted_output.py": (
        "The efficiency standard is taken for the budgeted units, not the units actually sold.",
        (
            'standard_inputs = sum(p["standard_inputs_per_unit"] * p["actual_units"] for p in products)',
            'standard_inputs = sum(p["standard_inputs_per_unit"] * p["budget_units"] for p in products)',
        ),
    ),
    "m49_exact_halves_round_down.py": (
        "Flexed amounts with an exact half cent are rounded down, not halves up.",
        (
            "    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)\n",
            "    return (2 * amount.numerator + amount.denominator - 1) // (2 * amount.denominator)\n",
        ),
    ),
    "m50_flexed_units_is_budget_total.py": (
        "flexible_budget reports the budgeted unit total in its units field, not the actual total it was flexed to.",
        ('        "units": total,\n', '        "units": budget_units,\n'),
    ),
}

for name, (doc, (old, new)) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    text = REF.replace(old, new, 1).replace(DOC_OLD, f'"""{doc}"""', 1)
    assert text != REF
    (MUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
