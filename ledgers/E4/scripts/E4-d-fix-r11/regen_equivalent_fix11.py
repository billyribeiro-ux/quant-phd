"""Regenerate the equivalent-folder variants and the stop-rule mutant from the CURRENT grader/reference.py (cap 240),
each by one exact string replacement (each must match once). Run: python3 -I regen_equivalent_fix11.py <repo-root>
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
eq = root / "ledgers/E4/equivalent"
mut = root / "ledgers/E4/mutants"

VARIANTS = {
    eq / "literal_price_sign.py": (
        "Variant of the reference: the noise coefficient of the price has the wrong sign (equivalent on the outputs).",
        [("    b_u = -RISK_AVERSION * b_s / (lam * tau_e)", "    b_u = RISK_AVERSION * b_s / (lam * tau_e)")],
    ),
    eq / "mutant_r6_08_reports_lower_end.py": (
        "Variant of the reference: reports the lower end of the final bracket instead of its midpoint (equivalent).",
        [("        lam = 0.5 * (low + high)\n", "        lam = low\n")],
    ),
    eq / "mutant_r7_01_reports_bracket_lower_end.py": (
        "Variant of the reference: reports the lower end of the final bracket instead of its midpoint (equivalent).",
        [("        lam = 0.5 * (low + high)\n", "        lam = low\n")],
    ),
    eq / "mutant_v9_02_stop_rule_relative_to_lower_end.py": (
        "Variant of the reference: the stop test is measured against the lower end of the bracket (equivalent).",
        [("BISECTION_TOLERANCE * high and steps", "BISECTION_TOLERANCE * low and steps")],
    ),
    mut / "mutant_r6_09_always_200_halvings.py": (
        "Never applies the relative stop rule and takes 200 halvings, so a root near 2e-51 misses the accuracy requirement.",
        [("        while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:",
          "        while steps < 200:")],
    ),
}

body_start = ref.index('"""', 3) + 3
body = ref[body_start:]
for path, (desc, edits) in VARIANTS.items():
    text = body
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            sys.exit(f"{path.name}: '{old[:60]}' matches {n} times, expected 1")
        text = text.replace(old, new)
    header = f'"""{desc}\n\nSingle change to grader/reference.py, regenerated for the cap of 240 halvings (round 11).\n"""'
    path.write_text(header + text, encoding="utf-8")
    print("wrote", path.relative_to(root))
