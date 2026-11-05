"""LX2-c r12: writes the round-12 lab-2 student-error mutants and alternatives as complete modules.

Base: the completed solution of project lab 2 (tests/labs/LX2/lab-LX2-project-2.py). Each mutant replaces the two
blanked expressions (the hit-rate line and the bias line) with a student-style expression, and opens with a one-line
docstring that names the error. Alternatives are correct solutions written with other valid expressions.
Run from the checkout root: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r12/make_r12_mutants.py
"""
from pathlib import Path

root = Path.cwd()
base = (root / "tests/labs/LX2/lab-LX2-project-2.py").read_text(encoding="utf-8")
HIT_LINE = "    hit_rate = Fraction(hits, horizon)\n"
BIAS_LINE = "    bias = Fraction(sum(errors), horizon)\n"
assert base.count(HIT_LINE) == 1 and base.count(BIAS_LINE) == 1
body = base.split('"""', 2)[2]  # everything after the module docstring

MUTANTS = {
    "r12_lab2_hit_count_counts_only_upper_side.py": (
        "Student error (hit rate): the hit count tests only e <= 2, so a month with e = -5 counts as a hit.",
        "    hit_rate = Fraction(sum(1 for e in errors if e <= HIT_BAND), horizon)\n",
        BIAS_LINE,
    ),
    "r12_lab2_hit_count_adds_edge_months.py": (
        "Student error (hit rate): the edge months are counted twice, once as hits and again as extra hits.",
        "    hit_rate = Fraction(hits + len([e for e in errors if abs(e) == HIT_BAND]), horizon)\n",
        BIAS_LINE,
    ),
    "r12_lab2_hit_rate_denominator_excludes_edge_months.py": (
        "Student error (hit rate): the denominator drops the edge months, so H is taken as 4 instead of 6.",
        "    hit_rate = Fraction(hits, horizon - len([e for e in errors if abs(e) == HIT_BAND]))\n",
        BIAS_LINE,
    ),
    "r12_lab2_bias_uses_mean_realised_value.py": (
        "Student error (bias): the bias is the mean of the realised values rather than the mean error.",
        HIT_LINE,
        "    bias = Fraction(sum(REALISED), horizon)\n",
    ),
    "alt_r12_lab2_statistics_fmean_bias.py": (
        "Alternative (correct): the bias is statistics.fmean of the error list, a float; the print is unchanged.",
        HIT_LINE,
        "    bias = statistics.fmean(errors)\n",
    ),
    "alt_r12_lab2_hit_rate_generator_sum.py": (
        "Alternative (correct): the hit rate is the count from a generator divided by H, a float with the same print.",
        "    hit_rate = sum(1 for e in errors if abs(e) <= HIT_BAND) / horizon\n",
        BIAS_LINE,
    ),
    "alt_r12_lab2_bias_sum_over_len.py": (
        "Alternative (correct): the bias divides the error sum by len(errors), which is H for this window.",
        HIT_LINE,
        "    bias = Fraction(sum(errors), len(errors))\n",
    ),
}

for name, (doc, hit_line, bias_line) in MUTANTS.items():
    text = body
    text = text.replace(HIT_LINE, hit_line, 1).replace(BIAS_LINE, bias_line, 1)
    if name.startswith("alt_r12_lab2_statistics"):
        text = text.replace("from fractions import Fraction\n", "import statistics\nfrom fractions import Fraction\n", 1)
    out = f'"""{doc}"""\n' + text
    (root / "ledgers/LX2/mutants" / name).write_text(out, encoding="utf-8")
    print("wrote", name)
