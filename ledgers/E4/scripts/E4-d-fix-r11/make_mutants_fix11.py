"""Write ten student-error mutants of grader/reference.py, each a single exact string replacement (each must match once).

Run: python3 -I make_mutants_fix11.py <repo-root>
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref_path = root / "course/modules/E/E4/grader/reference.py"
ref = ref_path.read_text(encoding="utf-8")
out_dir = root / "ledgers/E4/mutants"

MUTANTS = {
    "mutant_f11_01_cap_200_halvings_misses_the_domain_edge.py": (
        "Stops after 200 halvings, so a root near 2e-51 keeps a bracket wider than 1e-10 times the root.",
        [("MAX_BISECTION_STEPS = 240", "MAX_BISECTION_STEPS = 200")],
    ),
    "mutant_f11_02_cap_150_halvings_stops_early_at_small_roots.py": (
        "Stops after 150 halvings, which leaves a bracket far wider than the relative tolerance at small roots.",
        [("MAX_BISECTION_STEPS = 240", "MAX_BISECTION_STEPS = 150")],
    ),
    "mutant_f11_03_stop_tolerance_1e-9_relative.py": (
        "Stops when the bracket is narrower than 1e-9 times its upper end, a looser stop than the documented 1e-12.",
        [("BISECTION_TOLERANCE = 1e-12", "BISECTION_TOLERANCE = 1e-9")],
    ),
    "mutant_f11_04_absolute_bracket_stop_1e-12.py": (
        "Stops when the bracket is narrower than 1e-12 in absolute terms, so a root near 1e-51 is never resolved.",
        [("while high - low > BISECTION_TOLERANCE * high and steps", "while high - low > BISECTION_TOLERANCE and steps")],
    ),
    "mutant_f11_05_informativeness_is_tau_y_over_prior_precision.py": (
        "Reports the informativeness as tau_y / tau_v, not tau_y / (tau_v + tau_y), the posterior share of the price.",
        [("    return tau_y / (PRIOR_PRECISION + tau_y)", "    return tau_y / PRIOR_PRECISION")],
    ),
    "mutant_f11_06_interior_gap_at_a_nudged_fraction.py": (
        "Reports the interior gap at a fraction nudged by a relative 1e-9 rather than at the reported fraction.",
        [(
            "    gap = indifference_gap(lam, sd, cost) if 0.0 < lam < 1.0 else",
            "    gap = indifference_gap(lam * (1.0 + 1e-9), sd, cost) if 0.0 < lam < 1.0 else",
        )],
    ),
    "mutant_f11_07_interior_cost_factor_relative_error_1e-9.py": (
        "Scales the cost in the interior gap by (1 + 1e-9), a relative error at every interior fraction.",
        [(
            "    return uninformed_term(lam, noise_sd) - math.exp(RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)",
            "    return uninformed_term(lam, noise_sd) - math.exp(RISK_AVERSION * info_cost * (1.0 + 1e-9)) * informed_term(lam, noise_sd)",
        )],
    ),
    "mutant_f11_08_zero_fraction_cost_factor_relative_error_1e-9.py": (
        "Scales the cost in the limit of the gap at fraction 0 by (1 + 1e-9), so the reported limit is off.",
        [(
            "    return uninformed - math.exp(RISK_AVERSION * info_cost) * informed",
            "    return uninformed - math.exp(RISK_AVERSION * info_cost * (1.0 + 1e-9)) * informed",
        )],
    ),
    "mutant_f11_09_gap_at_zero_uses_a_not_a_squared.py": (
        "Uses the risk aversion a, not a squared, in the variance term of the limit of the gap at fraction 0.",
        [("    a2 = RISK_AVERSION * RISK_AVERSION * noise_sd * noise_sd", "    a2 = RISK_AVERSION * noise_sd * noise_sd")],
    ),
    "mutant_f11_10_interior_gap_reported_as_the_gap_at_one.py": (
        "Reports the gap at fraction 1 for every interior root, not the gap at the reported fraction.",
        [(
            "    gap = indifference_gap(lam, sd, cost) if 0.0 < lam < 1.0 else (gap_0 if lam == 0.0 else gap_1)",
            "    gap = gap_1",
        )],
    ),
}

# The module docstring of the reference runs from the first triple quote to the next one.
body_start = ref.index('"""', 3) + 3
body = ref[body_start:]
for name, (desc, edits) in MUTANTS.items():
    text = body
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            sys.exit(f"{name}: '{old[:60]}' matches {n} times, expected 1")
        text = text.replace(old, new)
    header = f'"""{desc}\n\nSingle change to grader/reference.py: a student error, not the reference solution.\n"""'
    (out_dir / name).write_text(header + text, encoding="utf-8")
    print("wrote", name)
