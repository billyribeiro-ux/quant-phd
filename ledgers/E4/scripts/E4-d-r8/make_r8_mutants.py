"""Write the round-8 student-error mutants of the E4 solver from reference.py (verifier scratch; not course content)."""
import pathlib
import re

REF = pathlib.Path("course/modules/E/E4/grader/reference.py")
OUT = pathlib.Path("ledgers/E4/mutants")
src = REF.read_text(encoding="utf-8")
first = src.index('"""')
second = src.index('"""', first + 3) + 3

MUTANTS = {
    "mutant_r8_01_cap_100_halvings.py": (
        "Bisection capped at 100 halvings, not the 200 that the page states, so a root below about 1e-18 is not reached.",
        [("MAX_BISECTION_STEPS = 200", "MAX_BISECTION_STEPS = 100")],
    ),
    "mutant_r8_02_noise_above_ten_rejected.py": (
        "Rejects a finite noise volume above 10 with the noise-volume ValueError; the page names no upper bound.",
        [("if not (math.isfinite(sd) and sd > 0.0):", "if not (math.isfinite(sd) and 0.0 < sd <= 10.0):")],
    ),
    "mutant_r8_03_cost_above_five_rejected.py": (
        "Rejects a finite information cost above 5 with the cost ValueError; the page names only negative costs.",
        [("if not (math.isfinite(cost) and cost >= 0.0):", "if not (math.isfinite(cost) and 0.0 <= cost <= 5.0):")],
    ),
    "mutant_r8_04_integer_zero_fraction.py": (
        "Returns the informed fraction as the integer 0 at the boundary, although every output must be a float.",
        [("        lam = 0.0\n    elif gap_1", "        lam = 0\n    elif gap_1")],
    ),
    "mutant_r8_05_informativeness_at_unit_precision.py": (
        "Reports the informativeness from the precision at fraction 1 for every fraction, not the price at the reported fraction.",
        [("    tau_y = price_precision(lam, noise_sd)\n    return tau_y / (PRIOR_PRECISION + tau_y)",
          "    tau_y = price_precision(1.0, noise_sd)\n    return tau_y / (PRIOR_PRECISION + tau_y)")],
    ),
}
for name, (doc, reps) in MUTANTS.items():
    text = src
    for old, new in reps:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    text = f'"""{doc}"""' + text[second:]
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
