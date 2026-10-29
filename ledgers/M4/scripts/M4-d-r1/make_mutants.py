"""Write the verifier's round-1 student-error mutants (m12 to m18) from the project reference (verifier round 1).

Each mutant is the reference with exactly one substitution; the substitution must match exactly once.
Usage: .venv/bin/python ledgers/M4/scripts/M4-d-r1/make_mutants.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/M/M4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M4/mutants"

MUTANTS = {
    "m12_losses_truncated_not_rounded.py": (
        "Losses are truncated toward zero with int() instead of rounded once with round(), so a loss is up to one cent low.",
        "        losses.append(round(-total))",
        "        losses.append(int(-total))",
    ),
    "m13_correlation_ignored.py": (
        "Assets are treated as uncorrelated: the factor keeps only the diagonal of the covariance, so cross terms are lost.",
        "    factor = _cholesky(cov, n)",
        "    factor = [[(cov[i][i] ** 0.5 if i == j else 0.0) for j in range(n)] for i in range(n)]",
    ),
    "m14_chi_square_scale_one.py": (
        "The chi-square draw uses gammavariate scale 1 instead of 2, so W is half the chi-square and the Student-t is too wide.",
        "            chi_square = rng.gammavariate(nu / 2, 2.0)",
        "            chi_square = rng.gammavariate(nu / 2, 1.0)",
    ),
    "m15_float_nu_accepted.py": (
        "matched_scale accepts a whole-valued float such as 3.0 as nu, instead of rejecting every non-int.",
        "    if not _whole(nu):\n        raise ValueError(\"nu must be a whole number of degrees of freedom\")",
        "    if not (_whole(nu) or (type(nu) is float and nu.is_integer())):\n        raise ValueError(\"nu must be a whole number of degrees of freedom\")",
    ),
    "m16_asymmetric_covariance_accepted.py": (
        "The symmetry check is skipped, so an asymmetric covariance is read from its lower triangle without an error.",
        "            if cov[i][j] != cov[j][i]:\n                raise ValueError(\"cov must be symmetric\")",
        "            if False and cov[i][j] != cov[j][i]:\n                raise ValueError(\"cov must be symmetric\")",
    ),
    "m17_student_t_second_seed.py": (
        "The Student-t family draws from seed + 1 while the Gaussian family draws from seed, so the two families do not share a seed.",
        "    rng = random.Random(seed)\n    losses: list[int] = []",
        "    rng = random.Random(seed + 1 if family == \"student_t\" else seed)\n    losses: list[int] = []",
    ),
    "m19_negative_draws_return_empty.py": (
        "Only n_draws = 0 is rejected: a negative draw count is accepted and returns an empty list instead of raising ValueError.",
        "    if not _whole(n_draws) or n_draws < 1:",
        "    if not _whole(n_draws) or n_draws == 0:",
    ),
    "m18_zero_draws_return_empty.py": (
        "n_draws = 0 is accepted and returns an empty list of losses instead of raising ValueError.",
        "    if not _whole(n_draws) or n_draws < 1:",
        "    if not _whole(n_draws) or n_draws < 0:",
    ),
}

if __name__ == "__main__":
    for name, (doc, old, new) in MUTANTS.items():
        assert REF.count(old) == 1, (name, REF.count(old))
        body = REF.replace(old, new, 1)
        header = f'"""{doc}"""\n'
        body = body.replace('"""Reference solution', '"""Reference solution', 1)
        # Put the one-line description first so mutate_graders.py reads it as the docstring.
        body = body.split('"""', 2)[2].lstrip("\n")
        (OUT / name).write_text(header + "\n" + body, encoding="utf-8")
        print("wrote", name)
