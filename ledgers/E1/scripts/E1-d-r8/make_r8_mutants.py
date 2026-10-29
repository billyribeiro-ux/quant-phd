"""Write five new student-error mutants of the E1 reference into ledgers/E1/mutants (round 8, slice d)."""

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB8-E1-d")
REF = (ROOT / "course/modules/E/E1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E1/mutants"

MUTANTS = {
    "r8d_m01_half_up_uses_builtin_round_ties_to_even.py": (
        "Mutant: half_up uses Python's built-in round(), which sends exact halves to the even neighbour, so 70.5 prints 70.",
        [("    return math.floor(x + Fraction(1, 2))", "    return round(x)")],
    ),
    "r8d_m02_deadweight_measured_from_monopoly_volume.py": (
        "Mutant: the deadweight loss measures the shortfall from the monopoly volume d/2 instead of the competitive volume d.",
        [("    deadweight = (d - volume) ** 2 / (2 * b)", "    deadweight = (d / 2 - volume) ** 2 / (2 * b)")],
    ),
    "r8d_m03_monopoly_fee_uses_a_plus_c.py": (
        "Mutant: the monopoly fee is (a + c) / (2b), with c where the closed form has b*c.",
        [("        fee = Fraction(a + b * c, 2 * b)", "        fee = Fraction(a + c, 2 * b)")],
    ),
    "r8d_m04_consumer_surplus_is_Q_times_gap_minus_Q.py": (
        "Mutant: consumer surplus is Q(d - Q)/(2b) instead of Q^2/(2b), which agrees only at the monopoly volume.",
        [("    consumer = volume * volume / (2 * b)", "    consumer = volume * (d - volume) / (2 * b)")],
    ),
    "r8d_m05_gap_forgets_the_factor_b.py": (
        "Mutant: the gap is d = a - c, forgetting the factor b in b*c, so every volume uses the wrong gap.",
        [("    d = Fraction(a - b * c)\n    if structure", "    d = Fraction(a - c)\n    if structure")],
    ),
}

for name, (doc, reps) in MUTANTS.items():
    src = REF
    for old, new in reps:
        assert src.count(old) == 1, (name, old)
        src = src.replace(old, new)
    # one-line docstring at the top, as the mutate tool expects; replace the module docstring's first line
    first_end = src.index('"""')
    body = src[src.index('"""', first_end + 3) + 3 :]
    (OUT / name).write_text(f'"""{doc}"""\n' + body, encoding="utf-8")
    print("wrote", name)
