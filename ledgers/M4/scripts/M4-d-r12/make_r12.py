"""Round-12 verifier: write 4 student-error mutants (ledgers/M4/mutants/r12_*.py) and 4 correct alternatives
(ledgers/M4/scripts/M4-d-r12/alts/alt_r12_*.py). Each edit must match the reference exactly once."""
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD12-M4-d")
REF = (ROOT / "course/modules/M/M4/grader/reference.py").read_text(encoding="utf-8")
MUT = ROOT / "ledgers/M4/mutants"
ALT = ROOT / "ledgers/M4/scripts/M4-d-r12/alts"
ALT.mkdir(parents=True, exist_ok=True)
DOC_END = REF.index('"""', 3) + 3  # end of the module docstring


def build(doc: str, edits: list[tuple[str, str]]) -> str:
    src = REF[DOC_END:]
    for old, new in edits:
        n = src.count(old)
        if n != 1:
            raise SystemExit(f"edit target found {n} times: {old[:70]!r}")
        src = src.replace(old, new)
    return f'"""{doc}"""' + src


MUTANTS = {
    "r12_01_student_t_chi_square_has_nu_minus_two_degrees_of_freedom.py": build(
        "Round-12 verifier student-error mutant: the Student-t chi-square variable is drawn with nu - 2 degrees of "
        "freedom, so every Student-t return is scaled too large.",
        [("chi_square = rng.gammavariate(nu / 2, 2.0)", "chi_square = rng.gammavariate((nu - 2) / 2, 2.0)")],
    ),
    "r12_02_returns_scaled_by_the_asset_volatility_a_second_time.py": build(
        "Round-12 verifier student-error mutant: each asset's return is multiplied by its volatility sqrt(cov_ii) on top "
        "of the factor L, so the loss variance is wrong whenever a volatility is not 1.",
        [("            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))",
          "            ret = scale * math.sqrt(cov[i][i]) * sum(factor[i][k] * z[k] for k in range(i + 1))")],
    ),
    "r12_03_gaussian_stream_seeded_with_seed_plus_one.py": build(
        "Round-12 verifier student-error mutant: the random stream is seeded with seed + 1, an off-by-one in the seed, "
        "so the frozen Gaussian stream of the page is not reproduced.",
        [("    rng = random.Random(seed)\n", "    rng = random.Random(seed + 1)\n")],
    ),
    "r12_04_factor_built_from_the_correlation_matrix.py": build(
        "Round-12 verifier student-error mutant: the Cholesky factor is taken of the correlation matrix (cov divided by "
        "the volatilities), so every asset is simulated with unit variance.",
        [("    factor = _cholesky(cov, n)\n",
          "    corr = [[cov[i][j] / math.sqrt(cov[i][i] * cov[j][j]) for j in range(n)] for i in range(n)]\n"
          "    factor = _cholesky(corr, n)\n")],
    ),
}
for name, text in MUTANTS.items():
    (MUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)

ALTS = {
    "alt_r12_1_float_ceiling_quantile_index.py": [
        ("    index = (99 * len(losses_cents) + 99) // 100\n", "    index = math.ceil(0.99 * len(losses_cents))\n"),
    ],
    "alt_r12_2_student_t_chi_square_as_sum_of_squares.py": [
        ("            chi_square = rng.gammavariate(nu / 2, 2.0)\n",
         "            chi_square = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu))\n"),
    ],
    "alt_r12_3_exact_ldl_pivot_test.py": [
        ("    factor = [[0.0] * n for _ in range(n)]\n    for i in range(n):\n        for j in range(i + 1):\n"
         "            inner = sum(factor[i][k] * factor[j][k] for k in range(j))\n"
         "            if i == j:\n                pivot = cov[i][i] - inner\n                if not pivot > 0.0:\n"
         "                    raise ValueError(\"cov must be positive definite: every Cholesky pivot must be above zero\")\n"
         "                factor[i][i] = math.sqrt(pivot)\n"
         "            else:\n                factor[i][j] = (cov[i][j] - inner) / factor[j][j]\n    return factor\n",
         "    exact = _exact_pivots(cov, n)\n"
         "    factor = [[0.0] * n for _ in range(n)]\n    for i in range(n):\n        for j in range(i + 1):\n"
         "            inner = sum(factor[i][k] * factor[j][k] for k in range(j))\n"
         "            if i == j:\n                factor[i][i] = math.sqrt(max(exact[i], 0.0))\n"
         "            else:\n                factor[i][j] = (cov[i][j] - inner) / factor[j][j]\n    return factor\n\n\n"
         "def _exact_pivots(cov, n):\n"
         "    from fractions import Fraction\n"
         "    a = [[Fraction(cov[i][j]) for j in range(n)] for i in range(n)]\n"
         "    d = [Fraction(0)] * n\n"
         "    l = [[Fraction(0)] * n for _ in range(n)]\n"
         "    for j in range(n):\n"
         "        d[j] = a[j][j] - sum(l[j][k] * l[j][k] * d[k] for k in range(j))\n"
         "        if not d[j] > 0:\n"
         "            raise ValueError(\"cov must be positive definite: every Cholesky pivot must be above zero\")\n"
         "        for i in range(j + 1, n):\n"
         "            l[i][j] = (a[i][j] - sum(l[i][k] * l[j][k] * d[k] for k in range(j))) / d[j]\n"
         "    return [float(x) for x in d]\n"),
    ],
    "alt_r12_4_reversed_position_sum.py": [
        ("        total = 0.0\n        for i in range(n):\n", "        total = 0.0\n        for i in reversed(range(n)):\n"),
    ],
}
for name, edits in ALTS.items():
    text = build("Round-12 verifier correct alternative.", edits)
    (ALT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
