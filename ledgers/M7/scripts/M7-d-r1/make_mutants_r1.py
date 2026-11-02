"""Write the verifier's round-1 student-error mutants as complete modules derived from grader/reference.py.

Each replacement must match exactly once, or the script stops. Run from the checkout root:
    python3 -I ledgers/M7/scripts/M7-d-r1/make_mutants_r1.py
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
REF = (ROOT / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M7/mutants"
OLD_DOC = REF[: REF.index('"""', 3) + 3]

MUTANTS = {
    "d1_01_weights_shifted_by_1e-7_budget_kept.py": (
        "Student error d1_01: the returned weights are 1e-7 away from the optimum (an iteration stopped too early), so the "
        "stationarity residual is about 1e-7, above the 1e-8 tolerance.",
        [('        "w": x,\n', '        "w": [x[0] + Fraction(1, 10**7), x[1] - Fraction(1, 10**7), *x[2:]],\n')],
    ),
    "d1_02_turnover_multipliers_by_sign_of_displacement.py": (
        "Student error d1_02: the turnover multipliers are assigned by the sign of each displacement (plus if w_i is above "
        "w0_i, minus if below), not by the sign constraint the solver used, so the stationarity in the turnover variables "
        "fails at zero displacement.",
        [
            ("        plus[i] = (kappa + net) / 2\n        minus[i] = (kappa - net) / 2\n",
             "        plus[i] = kappa if x[i] > problem.w0[i] else Fraction(0)\n"
             "        minus[i] = kappa if x[i] < problem.w0[i] else Fraction(0)\n"),
        ],
    ),
    "d1_03_primal_residual_reported_as_zero_with_budget_gap.py": (
        "Student error d1_03: the weights sum to one plus 5e-9 (inside the 1e-8 tolerance), and the certificate reports a "
        "primal residual of exactly zero instead of recomputing it from the weights.",
        [
            ('        "w": x,\n', '        "w": [x[0] + Fraction(5, 10**9), *x[1:]],\n'),
            ("    primal = max([Fraction(0), abs(sum(w, Fraction(0)) - 1), *gaps])\n", "    primal = Fraction(0)\n"),
        ],
    ),
    "d1_04_turnover_stationarity_reports_kappa_alone.py": (
        "Student error d1_04: the certificate's turnover-variable stationarity is reported as the total multiplier kappa "
        "alone, dropping the plus and minus multipliers, so it is non-zero whenever the turnover limit binds.",
        [("        r_t = sol[\"kappa\"] - sol[\"plus\"][i] - sol[\"minus\"][i]\n", "        r_t = sol[\"kappa\"]\n")],
    ),
}

for name, (doc, replacements) in MUTANTS.items():
    text = REF.replace(OLD_DOC, f'"""{doc}"""', 1)
    for old, new in replacements:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"{name}: pattern found {count} times: {old!r}")
        text = text.replace(old, new, 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
