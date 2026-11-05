"""Round-11 student-error mutants of the E3 reference, written as complete elicit.py modules into ledgers/E3/mutants/.

Each mutant is reference.py with one replacement; every replacement must match exactly once (asserted)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E3/mutants"

MUTANTS = {
    "r11d_01_identification_reads_only_the_a_lotteries.py": (
        '"""Student error: loss aversion is accepted only when a lottery of A mixes a gain and a loss, so a set whose only mixed lottery is on the B side is refused.\n"""\n',
        [("    if not any(_mixed(a, pa) or _mixed(b, pb) for a, pa, b, pb, _ in parsed):",
          "    if not any(_mixed(a, pa) for a, pa, b, pb, _ in parsed):")],
    ),
    "r11d_02_newton_stops_when_the_likelihood_gain_is_below_1e9.py": (
        '"""Student error: the maximiser stops once one Newton step raises the log-likelihood by less than 1e-9, a function-value rule that stops before the gradient is near zero.\n"""\n',
        [("        xi, value = trial, new_value\n",
          "        if new_value - value < 1e-9:\n            return trial\n        xi, value = trial, new_value\n")],
    ),
    "r11d_03_crra_final_wealth_is_wealth_minus_each_prize.py": (
        '"""Student error: the CRRA model takes final wealth as wealth minus each prize, so a gain lowers final wealth.\n"""\n',
        [("    finals = [wealth + x for x in prizes]\n", "    finals = [wealth - x for x in prizes]\n")],
    ),
    "r11d_04_twelve_response_questionnaire_returns_the_lab3_table.py": (
        '"""Student error: estimate returns the printed Lab 3 numbers for any questionnaire of twelve responses, without maximising.\n"""\n',
        [("    if not responses:\n        raise ValueError(\"need at least one response, and mixed-sign lotteries, to identify loss aversion\")\n",
          "    if not responses:\n        raise ValueError(\"need at least one response, and mixed-sign lotteries, to identify loss aversion\")\n"
          "    if len(responses) == 12:\n        return {\"gamma_hat\": 0.6352, \"lambda_hat\": 6.1503, \"kappa_hat\": 2.0201, \"se_gamma\": 0.32, \"se_lambda\": 9.59, \"se_kappa\": 1.86, \"log_likelihood\": -7.1445}\n")],
    ),
}

for name, (doc, reps) in MUTANTS.items():
    text = REF
    for old, new in reps:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    # the docstring replaces the module docstring so the first line names the error
    head_end = text.index('"""', 3) + 3
    text = doc + text[head_end:].lstrip("\n")
    text = text.replace('\n"""', '"""', 0)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name, len(text))
