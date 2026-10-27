import pathlib, re
ref = pathlib.Path("/tmp/verify-ap1-r6-d/course/modules/AP/AP1/grader/reference.py").read_text(encoding="utf-8")
out = pathlib.Path("/tmp/verify-ap1-r6-d/ledgers/AP1/mutants")
HEADER_OLD = ref.split('"""', 2)[1]  # the reference docstring body
def rebuild(first_line: str, body_edits, name: str) -> None:
    text = ref
    # replace the module docstring with the mutant's description
    head, rest = text.split('"""', 2)[0], text.split('"""', 2)[2]
    doc = (f'"""{first_line}\n\n'
           "Verifier mutant of course/modules/AP/AP1/grader/reference.py at 653fcee: one realistic\n"
           "student error, otherwise identical to the reference.\n"
           '"""')
    text = head + doc + rest
    for old, new in body_edits:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)

rebuild(
    "sdf_values warns when a value of x' b is negative, reading a negative SDF as a sign of arbitrage.",
    [
        ("import math\nfrom dataclasses import dataclass\n", "import math\nimport warnings\nfrom dataclasses import dataclass\n"),
        ('    b = _vector(weights, "weights", x.shape[1])\n    return np.asarray(x @ b, dtype=np.float64)\n',
         '    b = _vector(weights, "weights", x.shape[1])\n'
         '    values = np.asarray(x @ b, dtype=np.float64)\n'
         '    if np.any(values < 0.0):\n'
         '        warnings.warn("an SDF must be positive: this one is negative in some state", RuntimeWarning, stacklevel=2)\n'
         '    return values\n'),
    ],
    "m52_sdf_values_warns_on_negative_value.py",
)
rebuild(
    "pricing_errors warns when some SDF value is negative, because a negative SDF must signal arbitrage.",
    [
        ("import math\nfrom dataclasses import dataclass\n", "import math\nimport warnings\nfrom dataclasses import dataclass\n"),
        ('    return np.asarray(x.T @ m / x.shape[0] - p, dtype=np.float64)\n',
         '    if np.any(m < 0.0):\n'
         '        warnings.warn("pricing_errors: a negative SDF value is a sign of arbitrage", RuntimeWarning, stacklevel=2)\n'
         '    return np.asarray(x.T @ m / x.shape[0] - p, dtype=np.float64)\n'),
    ],
    "m53_pricing_errors_warns_on_negative_sdf.py",
)
rebuild(
    "_full_rank rejects redundant payoffs with an absolute singular-value tolerance (1e-10), not a relative one.",
    [
        ("    if s[-1] <= _RANK_TOL * s[0]:\n", "    if s[-1] <= 1e-10:\n"),
    ],
    "m54_full_rank_absolute_singular_value_tolerance.py",
)
rebuild(
    "population_x_star accepts state probabilities whose sum is within 1e-3 of one, not within 1e-9.",
    [
        ("    if abs(float(pi.sum()) - 1.0) > 1e-9:\n", "    if abs(float(pi.sum()) - 1.0) > 1e-3:\n"),
    ],
    "m55_population_probs_sum_tolerance_1e3.py",
)
