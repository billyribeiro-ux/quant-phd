"""Round-10 verifier D: writes five new student-error mutants of the M4 reference into ledgers/M4/mutants/.

Each mutant is the reference module with one textual change. The script asserts that every replacement applies exactly once.
"""
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD10-M4-d")
REF = (ROOT / "course/modules/M/M4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M4/mutants"

MUTANTS = {
    "d10_01_gaussian_returns_scaled_by_the_matched_factor_of_nu_five.py": (
        "Gaussian returns are multiplied by the nu-5 matched factor 0.6, as if the t scale leaked into the Gaussian family.",
        [("        scale = 1.0\n", "        scale = 0.6 ** 0.5 if not student else 1.0\n")],
    ),
    "d10_02_chi_square_drawn_as_gamma_with_shape_nu_and_scale_one.py": (
        "The chi-square variate is drawn as Gamma(shape nu, scale 1), which has mean nu but the wrong variance and 1/W law.",
        [("rng.gammavariate(nu / 2, 2.0)", "rng.gammavariate(float(nu), 1.0)")],
    ),
    "d10_03_draw_count_batched_down_to_a_multiple_of_100.py": (
        "Draws are generated in whole batches of 100, so any draw count that is not a multiple of 100 returns fewer losses.",
        [("    for _ in range(n_draws):\n", "    for _ in range(n_draws // 100 * 100):\n")],
    ),
    "d10_04_quantile_reads_the_zero_based_position_of_the_one_based_index.py": (
        "The quantile reads the sorted list at the 1-based index, one order statistic too high.",
        [("    return sorted(losses_cents)[index - 1]", "    return sorted(losses_cents)[index]")],
    ),
    "d10_05_matched_scale_guard_rejects_nu_equal_to_three.py": (
        "The guard is written as nu <= 3, so matched_scale rejects the valid nu = 3 that the page says it accepts.",
        [("    if nu <= 2:\n        raise ValueError(\"nu must be greater than 2 for the matched covariance to exist\")",
          "    if nu <= 3:\n        raise ValueError(\"nu must be greater than 2 for the matched covariance to exist\")")],
    ),
}

for name, (description, replacements) in MUTANTS.items():
    text = REF
    for old, new in replacements:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    module_doc = text.split('"""', 2)
    assert module_doc[0] == "" and len(module_doc) >= 3, name
    text = '"""' + description + "\n\n" + module_doc[1].split("\n", 1)[1].lstrip("\n") + '"""' + module_doc[2]
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
