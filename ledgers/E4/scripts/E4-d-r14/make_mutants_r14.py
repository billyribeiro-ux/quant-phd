"""Round-14 verifier: write five student-error mutants of grader/reference.py into ledgers/E4/mutants/.

Each mutant is the reference with one exact string replacement (each old string must match exactly once), and its
module docstring is replaced by a one-line description of the student error.
Run: python3 -I make_mutants_r14.py <repo-root>
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
out_dir = root / "ledgers/E4/mutants"

MUTANTS = {
    "mutant_r14_01_unit_fraction_gap_read_at_1_minus_1e12.py": (
        "Reports the gap at fraction 1 read at the nearby fraction 1 - 1e-12 instead of at 1.",
        "    gap = indifference_gap(lam, sd, cost) if 0.0 < lam < 1.0 else (gap_0 if lam == 0.0 else gap_1)",
        "    gap = indifference_gap(lam, sd, cost) if 0.0 < lam < 1.0 else (\n"
        "        gap_0 if lam == 0.0 else indifference_gap(1.0 - 1e-12, sd, cost)\n"
        "    )",
    ),
    "mutant_r14_02_accepts_nan_noise_volume.py": (
        "Accepts a NaN noise volume, because the positivity check is written as a rejection on sd <= 0.",
        '    if not (math.isfinite(sd) and sd > 0.0):\n        raise ValueError("noise volume must be positive")',
        '    if sd <= 0.0 or sd == math.inf:\n        raise ValueError("noise volume must be positive")',
    ),
    "mutant_r14_03_uninformed_posterior_uses_prior_precision_twice.py": (
        "Writes the uninformed posterior variance with 1/tau_v in place of 1/(tau_v + tau_y) inside F_U.",
        "    return math.pow(1.0 + r * r * (tau_v + tau_y) * (1.0 / tau_v + 1.0 / tau_y), -0.5)",
        "    return math.pow(1.0 + r * r * (tau_v + tau_y) * (1.0 / tau_v + 1.0 / tau_v), -0.5)",
    ),
    "mutant_r14_04_boundary_rule_inverted_at_fraction_one.py": (
        "Returns the unit fraction whenever the gap at 1 is negative, which inverts the boundary rule at 1.",
        "    elif gap_1 >= 0.0:\n        lam = 1.0",
        "    elif gap_1 < 0.0:\n        lam = 1.0",
    ),
    "mutant_r14_05_unit_fraction_informativeness_reported_as_zero.py": (
        "Reports zero informativeness at fraction 1, as if the price carried no signal when every investor is informed.",
        '        "price_informativeness": price_informativeness(lam, sd),',
        '        "price_informativeness": 0.0 if lam == 1.0 else price_informativeness(lam, sd),',
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    count = ref.count(old)
    if count != 1:
        raise SystemExit(f"{name}: old string matches {count} times, expected 1")
    text = ref.replace(old, new, 1)
    end = text.index('"""', 3) + 3  # the reference's module docstring ends here
    text = f'"""{doc}"""' + text[end:]
    (out_dir / name).write_text(text, encoding="utf-8")
    print("wrote", name)
