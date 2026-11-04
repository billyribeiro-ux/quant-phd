"""Write three round-5 student-error mutants of the reference solution into ledgers/E3/mutants/ (complete modules)."""
import pathlib
import sys

REF = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
src = REF.read_text(encoding="utf-8")

MUTANTS = {
    "g5_01_wealth_check_message_omits_the_quoted_text.py": (
        "The wealth-plus-prize error message omits the text the exception table quotes.",
        [('raise ValueError("wealth plus prize must stay positive")', 'raise ValueError("wealth must be positive")')],
    ),
    "g5_02_mixed_check_counts_a_zero_prize_as_a_gain.py": (
        "Gain test uses x >= 0, so a zero prize with positive probability counts as a gain for mixed-sign identification.",
        [("    gains = any(x > 0 and p > 0 for x, p in zip(prizes, probs, strict=True))",
          "    gains = any(x >= 0 and p > 0 for x, p in zip(prizes, probs, strict=True))")],
    ),
    "g5_03_crra_change_uses_one_over_gamma_exponent.py": (
        "CRRA certainty equivalent takes the inverse power 1/gamma instead of 1/(1-gamma).",
        [("    return math.pow(expected, 1.0 / (1.0 - gamma)) - wealth",
          "    return math.pow(expected, 1.0 / gamma) - wealth")],
    ),
}

for name, (doc, reps) in MUTANTS.items():
    text = src
    for old, new in reps:
        assert text.count(old) == 1, (name, old, text.count(old))
        text = text.replace(old, new)
    # the first docstring line is the description of the student error
    first = text.index('"""')
    text = text[:first] + '"""' + doc + "\n\n" + text[first + 3:]
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
