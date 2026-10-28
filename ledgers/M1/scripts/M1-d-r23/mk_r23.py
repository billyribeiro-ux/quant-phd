"""Round 23: builds three alternative correct engines and three new student-error mutants from the reference.

Each edit is a literal replacement that must match exactly once; the script fails otherwise.
"""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/M/M1/grader/reference.py").read_text()
OUT = ROOT / "ledgers/M1/scripts/M1-d-r23"
ALTS = OUT / "alts"
MUT = ROOT / "ledgers/M1/mutants"


def edit(src: str, old: str, new: str) -> str:
    assert src.count(old) == 1, (old, src.count(old))
    return src.replace(old, new)


ALT = {
    "alt_r23_a_integer_nearest_cent.py": [(
        "    return math.floor(amount + Fraction(1, 2))",
        "    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)",
    )],
    "alt_r23_b_expm1_log1p_all_rates.py": [(
        "    return (1 - (1 + r) ** -n) / r",
        "    return -math.expm1(-n * math.log1p(r)) / r",
    )],
    "alt_r23_c_fraction_cutoff_1e30.py": [(
        "    if i == 0:\n        return _nearest_cent(Fraction(principal, n))",
        "    if abs(i) < Fraction(1, 10**30):\n        return _nearest_cent(Fraction(principal, n))",
    )],
}

MUTANTS = {
    "r23v_01_growing_perpetuity_adds_growth.py": (
        "    return 1 / (r - g)",
        "    return 1 / (r + g)",
        "Student mutant: the growing perpetuity divides by (rate + growth), a sign slip on the growth term.",
    ),
    "r23v_02_annuity_one_period_short.py": (
        "    return (1 - (1 + r) ** -n) / r",
        "    return (1 - (1 + r) ** -(n - 1)) / r",
        "Student mutant: the ordinary annuity counts one period too few, (1 - (1 + r)^-(n-1)) / r.",
    ),
    "r23v_03_last_payment_clipped_not_paid.py": (
        "        paid = payment if period < n else opening + interest\n        principal_paid = paid - interest\n        closing = opening - principal_paid",
        "        paid = payment\n        principal_paid = paid - interest\n        closing = max(0, opening - principal_paid)",
        "Student mutant: every month pays the level payment and the balance is clipped at zero, so the last month leaves a short payment instead of settling the balance.",
    ),
}

for name, edits in ALT.items():
    src = REF
    for old, new in edits:
        src = edit(src, old, new)
    (ALTS / name).write_text(src)

for name, (old, new, why) in MUTANTS.items():
    src = edit(REF, old, new)
    (MUT / name).write_text(f"# {why}\n" + src)
print("built", len(ALT), "alternatives and", len(MUTANTS), "mutants")
