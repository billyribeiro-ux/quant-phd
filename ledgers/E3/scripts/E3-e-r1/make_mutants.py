"""Write three new student-error mutants of the E3 reference solution (E3-e round 1). Each edit must match exactly once."""
import sys

REF = "/Users/billyribeiro/.fanout/wt/verifyD1-E3-e/course/modules/E/E3/grader/reference.py"
OUT = "/Users/billyribeiro/.fanout/wt/verifyD1-E3-e/ledgers/E3/mutants/"

src = open(REF, encoding="utf-8").read()

MUTANTS = {
    "e01_observed_information_cross_term_sign_flipped.py": (
        "Observed information with the sign of every mixed second derivative flipped, so the cross-parameter covariances are wrong.",
        [("            hess[i][j] = value\n            hess[j][i] = value\n",
          "            hess[i][j] = -value\n            hess[j][i] = -value\n")],
    ),
    "e02_reported_loglik_at_search_start.py": (
        "Reported log_likelihood is the value at the start point of the search, not at the estimate.",
        [('        "log_likelihood": _objective(theta, parsed),\n',
          '        "log_likelihood": _objective([0.0, 0.0, 0.0], parsed),\n')],
    ),
    "e03_prospect_loss_inverse_drops_minus_sign.py": (
        "Prospect certainty equivalent of a negative lottery value returns a positive amount: the minus sign of the loss-branch inverse is dropped.",
        [("    return -math.pow(-total / lam, 1.0 / (1.0 - gamma))\n",
          "    return math.pow(-total / lam, 1.0 / (1.0 - gamma))\n")],
    ),
}

for name, (desc, edits) in MUTANTS.items():
    text = src
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            sys.exit(f"{name}: pattern found {n} times")
        text = text.replace(old, new)
    body = f'"""{desc}\n\nAn E3 student-error mutant (verifier-written, E3-e round 1) of the reference solution. Standard library only.\n"""\n'
    # drop the reference's own module docstring (first triple-quoted block) and prepend the mutant's
    first_end = text.index('"""', text.index('"""') + 3) + 3
    text = body + text[first_end:]
    open(OUT + name, "w", encoding="utf-8").write(text)
    print("wrote", name)
