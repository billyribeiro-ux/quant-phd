"""Writes the round-5 verifier's student-error mutants of the E3 engine (stdlib only).

Each mutant is the reference solution with one change; the first docstring line names the error. Run from the checkout:
python3 -I ledgers/E3/scripts/E3-d-r5/v5_make_mutants.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E3/mutants"

MUTANTS = {
    "e3d5_01_zero_prize_counts_as_a_gain_in_the_mixed_test.py": (
        "A zero prize with positive probability counts as a gain in the mixed-sign test, so a set whose only "
        "'gain' is a sure zero passes the mixed-sign condition.",
        [("    gains = any(x > 0 and p > 0 for x, p in zip(prizes, probs, strict=True))",
          "    gains = any(x >= 0 and p > 0 for x, p in zip(prizes, probs, strict=True))")],
    ),
    "e3d5_02_gamma_standard_error_without_the_coordinate_factor.py": (
        "The gamma standard error omits the factor gamma (1 - gamma) that carries zeta to gamma, so it is the "
        "standard error in the logit coordinate.",
        [('        "se_gamma": gamma * (1.0 - gamma) * math.sqrt(cov_diag[0]),',
          '        "se_gamma": math.sqrt(cov_diag[0]),')],
    ),
    "e3d5_03_choice_precision_scaled_per_dollar_not_per_hundred_dollars.py": (
        "The logit reads the certainty-equivalent difference in dollars, not in units of $100, so every kappa is "
        "off by a factor of 100.",
        [("CENTS_PER_UNIT = 10_000.0", "CENTS_PER_UNIT = 100.0")],
    ),
    "e3d5_04_search_stops_once_the_gradient_is_below_one_thousandth.py": (
        "The Newton search stops once the largest gradient component is below 1e-3, so the estimate is returned "
        "before it is a stationary point.",
        [("        if max(abs(g) for g in grad) < 1e-7:\n            return xi",
          "        if max(abs(g) for g in grad) < 1e-3:\n            return xi")],
    ),
}

HEAD_END = REF.index('"""', REF.index('"""') + 3) + 3
for name, (described, edits) in MUTANTS.items():
    body = REF[HEAD_END:]
    for old, new in edits:
        assert body.count(old) == 1, (name, old, body.count(old))
        body = body.replace(old, new)
    header = (
        '"""' + described + "\n\n"
        "Round-5 verifier (E3-d) student-error mutant: the reference solution with the single change above. "
        "Standard library only.\n"
        '"""'
    )
    (OUT / name).write_text(header + body, encoding="utf-8")
    print("wrote", name)
