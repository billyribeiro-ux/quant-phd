"""Write the round-9 verifier's student-error mutants as complete solver modules, derived from reference.py by exact
string replacement (each replacement must match exactly once, or the script stops).

Run: python3 -I make_v9_mutants.py <repo-root>
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
out_dir = root / "ledgers/E4/mutants"

MUTANTS = {
    "mutant_v9_01_informed_variance_uses_sd_once.py": (
        "Informed-term variance uses the noise volume once, not squared, in the price-noise term of the gap.",
        [("var_gap = slope * slope * var_signal + b_u * b_u * noise_sd * noise_sd",
          "var_gap = slope * slope * var_signal + b_u * b_u * noise_sd")],
    ),
    "mutant_v9_02_stop_rule_relative_to_lower_end.py": (
        "Bisection stop rule measured against the lower end of the bracket instead of its upper end.",
        [("while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:",
          "while high - low > BISECTION_TOLERANCE * low and steps < MAX_BISECTION_STEPS:")],
    ),
    "mutant_v9_03_stops_when_gap_is_small.py": (
        "Bisection stops when the absolute gap at the midpoint is below 1e-9, not when the bracket is narrow.",
        [("while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:",
          "while abs(indifference_gap(0.5 * (low + high), sd, cost)) > 1e-9 and steps < MAX_BISECTION_STEPS:")],
    ),
    # mutant_v9_04 (interior gap reported as 0.0) is a correct alternative: alternatives/alt_v9_1_interior_gap_zero.py
    "mutant_v9_06_gap_at_zero_from_tiny_fraction.py": (
        "Gap at fraction 0 is taken as the gap at fraction 1e-12 instead of the limit of Proposition 3.",
        [("    if lam == 0.0:\n        return gap_at_zero(noise_sd, info_cost)",
          "    if lam == 0.0:\n        return indifference_gap(1e-12, noise_sd, info_cost)")],
    ),
    "mutant_v9_07_bisection_sixty_steps.py": (
        "Bisection stops after sixty halvings, so a root near 1e-40 is found with an absolute error near 1e-18.",
        [("while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:",
          "while steps < 60:")],
    ),
}

MUTANTS["mutant_v9_05_informativeness_interior_formula_everywhere.py"] = (
    "Price informativeness uses the interior closed form 1 - exp(2ac) tau_v/(tau_v+tau_e) at every fraction, including 1.",
    [
        ('        "price_informativeness": price_informativeness(lam, sd),',
         '        "price_informativeness": (0.0 if lam == 0.0 else 1.0 - math.exp(2.0 * RISK_AVERSION * cost) * PRIOR_PRECISION / (PRIOR_PRECISION + SIGNAL_PRECISION)),'),
    ],
)

for name, (doc, reps) in MUTANTS.items():
    text = ref
    for old, new in reps:
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"{name}: pattern found {n} times: {old[:60]!r}")
        text = text.replace(old, new)
    body = f'"""{doc}\n\nRound-9 verifier mutant (E4 slice d). Derived from grader/reference.py by one edit.\n"""\n' + text.split('"""', 2)[2]
    (out_dir / name).write_text(body, encoding="utf-8")
    print("wrote", name)
