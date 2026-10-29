# Round-10 verifier: writes four NEW student-error mutants as single-change copies of grader/reference.py.
# Each replacement must match exactly once, or the script stops.
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
src = (root / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/E3/mutants"

CHANGES = {
    "r10n04_probabilities_normalised_instead_of_refused.py": (
        "The probabilities are rescaled to sum to 1 instead of being refused when they do not.",
        [
            (
                "    if any(p < 0 for p in probs) or sum(probs, Fraction(0)) != 1:\n"
                '        raise ValueError("probabilities must sum to 1 (and be non-negative)")\n'
                "    return probs\n",
                "    if any(p < 0 for p in probs) or sum(probs, Fraction(0)) == 0:\n"
                '        raise ValueError("probabilities must sum to 1 (and be non-negative)")\n'
                "    total = sum(probs, Fraction(0))\n"
                "    return [p / total for p in probs]\n",
            )
        ],
    ),
    "r10n05_prospect_gain_inverse_exponent_one_minus_gamma.py": (
        "The prospect inverse for a non-negative lottery value uses the exponent 1 - gamma instead of 1/(1 - gamma).",
        [
            (
                "        return math.pow(total, 1.0 / (1.0 - gamma))\n    return -math.pow(-total / lam, 1.0 / (1.0 - gamma))\n",
                "        return math.pow(total, 1.0 - gamma)\n    return -math.pow(-total / lam, 1.0 / (1.0 - gamma))\n",
            )
        ],
    ),
    "r10n06_logit_log_term_naive_exp_overflow.py": (
        "The logit terms use log(1 + exp(t)) directly instead of the stable form. Large |z| overflows; the page states no "
        "numerical-stability requirement, so this survivor is informational.",
        [
            (
                "    if t > 0.0:\n        return t + math.log1p(math.exp(-t))\n    return math.log1p(math.exp(t))\n",
                "    return math.log(1.0 + math.exp(t))\n",
            )
        ],
    ),
    "r10n07_kappa_standard_error_without_delta_factor.py": (
        "The standard error of kappa omits the delta-method factor kappa (it is the standard error in log kappa).",
        [
            (
                '        "se_kappa": kappa * math.sqrt(cov_diag[2]),\n',
                '        "se_kappa": math.sqrt(cov_diag[2]),\n',
            )
        ],
    ),
}

for name, (doc, pairs) in CHANGES.items():
    text = src
    for old, new in pairs:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"{name}: replacement matched {count} times, expected 1: {old[:60]!r}")
        text = text.replace(old, new)
    header = "".join(f"# {line}\n" for line in (f"Student-error mutant (verifier E3-d, round 10). {doc}", "Single-change copy of the reference solution."))
    body = text.split('"""', 2)[2] if text.startswith('"""') else text
    (out / name).write_text(header + text, encoding="utf-8")
    print("wrote", name)
