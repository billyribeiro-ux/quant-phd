"""Write the round-4 student-error mutants of grader/reference.py into ledgers/E4/mutants/.

Each mutant is the reference with exactly one edit (the replaced text must occur exactly once); its docstring's first
line describes the error. Usage: python -I ledgers/E4/scripts/E4-d-r4/make_r4_mutants.py <repo-root>
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
ref_doc_end = ref.index('"""', 3) + 3
body = ref[ref_doc_end:]

MUTANTS = {
    "mutant_r4_absolute_bracket_tolerance": (
        "Bisection stops when the bracket is narrower than 1e-12 in absolute terms, not relative to its upper end.",
        "while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:",
        "while high - low > BISECTION_TOLERANCE and steps < MAX_BISECTION_STEPS:",
    ),
    "mutant_r4_informed_precision_signal_only": (
        "Informed posterior precision uses the signal precision alone, dropping the prior precision from tau_v + tau_e.",
        "    precision = tau_v + tau_e\n    slope = tau_e / precision - b_s",
        "    precision = tau_e\n    slope = tau_e / precision - b_s",
    ),
    "EQUIVALENT_price_slope_omits_uninformed_term": (
        "Price slope b_s drops the uninformed term (1 - lam) tau_y from its numerator.",
        "    b_s = (lam * tau_e + (1.0 - lam) * tau_y) / denominator",
        "    b_s = (lam * tau_e) / denominator",
    ),
    "mutant_r4_uninformed_variance_uses_signal_precision": (
        "Uninformed posterior variance factor uses the signal precision tau_e where the price precision tau_y belongs.",
        "    return math.pow(1.0 + r * r * (tau_v + tau_y) * (1.0 / tau_v + 1.0 / tau_y), -0.5)",
        "    return math.pow(1.0 + r * r * (tau_v + SIGNAL_PRECISION) * (1.0 / tau_v + 1.0 / SIGNAL_PRECISION), -0.5)",
    ),
    "mutant_r4_unit_fraction_reports_precision": (
        "Reports the price precision tau_y, not the squared correlation, at the boundary fraction 1.",
        "    return tau_y / (PRIOR_PRECISION + tau_y)",
        "    return tau_y if lam == 1.0 else tau_y / (PRIOR_PRECISION + tau_y)",
    ),
}

for name, (description, old, new) in MUTANTS.items():
    count = body.count(old)
    if count != 1:
        raise SystemExit(f"{name}: the replaced text occurs {count} times, expected 1")
    if name.startswith("EQUIVALENT_"):
        continue
    text = f'"""{description}\n\nSingle edit of grader/reference.py, written by the verifier (slice E4-d, round 4).\n"""'
    out = text + body.replace(old, new)
    (root / "ledgers/E4/mutants" / f"{name}.py").write_text(out, encoding="utf-8")
    print("wrote", name)
