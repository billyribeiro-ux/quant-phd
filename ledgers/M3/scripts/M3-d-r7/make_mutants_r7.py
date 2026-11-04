"""Round-7 verifier (slice d): writes three new student-error mutants of grader/reference.py into ledgers/M3/mutants/.
Each replacement is asserted to occur exactly once, so a mutant is never silently the unmodified reference."""

from pathlib import Path

ROOT = Path.cwd()
SRC = (ROOT / "course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M3/mutants"


def mutate(name: str, description: str, pairs: list[tuple[str, str]]) -> None:
    text = SRC
    for old, new in pairs:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    body = text.split('"""', 2)
    assert len(body) == 3, name
    head_end = text.index('"""', 3) + 3
    text = f'"""{description}\n\nRound-7 student-error mutant of grader/reference.py (verifier-written).\n"""\n' + text[head_end:].lstrip("\n")
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)


mutate(
    "r7d_m01_projection_correction_uses_new_iterate.py",
    "projection_repair updates the PSD correction from the new iterate instead of the previous one.",
    [
        (
            "        corr_s = [[x[i][j] + corr_s[i][j] - y[i][j] for j in range(n)] for i in range(n)]\n"
            "        new_x = [[y[i][j] + corr_u[i][j] for j in range(n)] for i in range(n)]\n"
            "        for i in range(n):\n"
            "            new_x[i][i] = 1.0\n",
            "        new_x = [[y[i][j] + corr_u[i][j] for j in range(n)] for i in range(n)]\n"
            "        for i in range(n):\n"
            "            new_x[i][i] = 1.0\n"
            "        corr_s = [[new_x[i][j] + corr_s[i][j] - y[i][j] for j in range(n)] for i in range(n)]\n",
        ),
    ],
)

mutate(
    "r7d_m02_clip_floors_the_diagonal_not_the_eigenvalues.py",
    "clip_repair applies the floor to the diagonal of the rebuilt matrix instead of to its eigenvalues.",
    [
        (
            "    x = _rebuild([max(value, floor) for value in values], vectors)\n",
            "    x = _rebuild(values, vectors)\n"
            "    x = [[max(x[i][j], floor) if i == j else x[i][j] for j in range(len(x))] for i in range(len(x))]\n",
        ),
    ],
)

mutate(
    "r7d_m03_min_eigenvalue_bisection_ten_steps.py",
    "min_eigenvalue locates the smallest eigenvalue by ten bisection steps on the Cholesky sign, not by the eigensolver.",
    [
        (
            "    values, _ = _eigh(_as_matrix(matrix))\n    return min(values)\n",
            "    a = _as_matrix(matrix)\n"
            "    n = len(a)\n"
            "    radius = max(sum(abs(x) for x in row) for row in a) + 1.0\n"
            "    lo, hi = -radius, radius\n"
            "    for _ in range(10):\n"
            "        mid = (lo + hi) / 2.0\n"
            "        shifted = [[a[i][j] - (mid if i == j else 0.0) for j in range(n)] for i in range(n)]\n"
            "        try:\n"
            "            _chol_pd(shifted)\n"
            "            lo = mid\n"
            "        except ValueError:\n"
            "            hi = mid\n"
            "    return lo\n\n\n"
            "def _chol_pd(m: Matrix) -> None:\n"
            "    n = len(m)\n"
            "    low = [[0.0] * n for _ in range(n)]\n"
            "    for i in range(n):\n"
            "        for j in range(i + 1):\n"
            "            total = sum(low[i][k] * low[j][k] for k in range(j))\n"
            "            if i == j:\n"
            "                pivot = m[i][i] - total\n"
            "                if not pivot > 0.0:\n"
            "                    raise ValueError(\"not positive definite\")\n"
            "                low[i][i] = math.sqrt(pivot)\n"
            "            else:\n"
            "                low[i][j] = (m[i][j] - total) / low[j][j]\n",
        ),
    ],
)
